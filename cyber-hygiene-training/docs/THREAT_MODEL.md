# Threat Model

## System Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Telegram   │────▶│  FastAPI     │────▶│  SQLite DB      │
│  Bot        │     │  Backend     │     │  (metadata only)│
│  (Aiogram)  │     │              │     └─────────────────┘
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Browser     │
                    │  (Frontend)  │
                    │  LOCAL ONLY: │
                    │  cards, OTP  │
                    └──────────────┘
```

## Assets

| Asset | Value | Protection Level |
|-------|-------|-----------------|
| User financial credentials | Critical | Never collected |
| User identity (name/phone) | High | Client-only, not persisted |
| Session tokens | Medium | UUID, time-limited |
| Quiz results | Low | Anonymous aggregates |
| Admin credentials | High | Environment variables, JWT |
| Platform reputation | High | Educational disclaimers |

## Threat Actors

### 1. External Attacker
- **Goal:** Steal data, compromise platform, misuse for phishing
- **Capability:** Network access, automated scanning
- **Mitigation:** HTTPS, input validation, no sensitive data storage

### 2. Malicious Insider (Admin)
- **Goal:** Access training analytics, modify platform
- **Capability:** Admin credentials
- **Mitigation:** Audit logging, least privilege, strong passwords

### 3. Accidental User
- **Goal:** N/A (unintentional real data entry)
- **Capability:** Enters real card/OTP despite warnings
- **Mitigation:** Luhn rejection, training-only OTP, client-side only processing

### 4. Platform Misuser
- **Goal:** Repurpose educational simulation for actual phishing
- **Capability:** Deploy modified copy
- **Mitigation:** License terms, educational framing, organizational governance

## STRIDE Analysis

### Spoofing
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| Fake admin login | High | Low | JWT auth, strong passwords |
| Session token guessing | Medium | Very Low | 256-bit URL-safe tokens |
| Telegram bot impersonation | Medium | Medium | Official bot verification by users |

### Tampering
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| Quiz answer manipulation | Low | Medium | Server-side grading |
| Progress flag spoofing | Low | Medium | Token-required endpoints |
| Database modification | Medium | Low | File permissions, backups |

### Repudiation
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| Admin action denial | Low | Low | Audit log with timestamps and IPs |

### Information Disclosure
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| Real card data leaked | Critical | Very Low | Never transmitted to server |
| PII in server logs | High | Low | No PII logged; fragment not sent to server |
| Quiz answers in transit | Low | Low | HTTPS, no correct answers in GET |

### Denial of Service
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| Session creation flood | Medium | Medium | Rate limiting (recommended) |
| Bot message flood | Medium | Medium | Telegram rate limits |

### Elevation of Privilege
| Threat | Impact | Likelihood | Control |
|--------|--------|------------|---------|
| User → Admin escalation | High | Low | Separate JWT auth, role check |
| API abuse for data extraction | Medium | Low | No sensitive data to extract |

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────┐
│ TRUSTED: Organization-controlled infrastructure          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ Backend API │  │ SQLite DB   │  │ Admin Panel │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────┘
         ▲                              ▲
         │ HTTPS (metadata only)        │ Local only
         │                              │
┌────────┴────────┐            ┌────────┴────────┐
│ UNTRUSTED:      │            │ UNTRUSTED:      │
│ Telegram Client │            │ User Browser    │
│ (bot messages)  │            │ (sensitive sim) │
└─────────────────┘            └─────────────────┘
```

**Critical trust boundary:** The browser is untrusted for sensitive input. Card numbers and OTP codes never cross the browser→server boundary.

## Attack Scenarios

### Scenario 1: User Enters Real Card Number
1. User types real Visa card on simulation page
2. Client-side Luhn check detects valid card pattern
3. **Blocked** with safety warning
4. Value never leaves browser
5. **Residual risk:** User ignores warning and enters non-Luhn fake pattern — still not transmitted

### Scenario 2: Man-in-the-Middle on API
1. Attacker intercepts HTTPS traffic
2. Only session tokens and quiz indices visible
3. No financial data in transit
4. **Control:** TLS 1.2+ required in production

### Scenario 3: SQL Injection
1. Attacker sends malicious input to API
2. SQLAlchemy ORM parameterizes all queries
3. **Control:** Pydantic validation on all inputs

### Scenario 4: XSS on Landing Page
1. Attacker injects script via URL parameters
2. Token in query string is UUID only
3. PII in fragment not accessible server-side
4. **Control:** No innerHTML with user input; Jinja2 auto-escaping

## Data Flow Diagram (Sensitive Data)

```
Bot collects name/phone
        │
        ▼
  URL Fragment (#name=...&phone=...)
        │  ◄── NOT sent to server (browser security)
        ▼
  sessionStorage (browser)
        │
        ▼
  Certificate display ONLY

Card/OTP input
        │
        ▼
  Client-side validation
        │
        ▼
  DISCARDED (fields cleared)
        │
        ✕ ──► NEVER reaches server
```

## Risk Matrix Summary

| Category | Pre-Mitigation | Post-Mitigation |
|----------|---------------|-----------------|
| Data theft | Critical | Low |
| Phishing misuse | High | Medium |
| Service disruption | Medium | Low |
| Privacy violation | High | Low |

## Review Schedule

- Threat model review: Annually or after major changes
- Dependency audit: Monthly
- Penetration test: Before organizational rollout
