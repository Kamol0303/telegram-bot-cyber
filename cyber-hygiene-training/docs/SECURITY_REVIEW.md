# Security Review

**Platform:** Cyber Hygiene Awareness Training  
**Classification:** Educational Simulation  
**Review Date:** 2026  
**Status:** Approved for educational deployment with documented controls

## Executive Summary

This platform intentionally simulates phishing and scam patterns for cybersecurity education. Security controls ensure that no real sensitive data is collected, stored, or transmitted. This review documents implemented controls and residual risks.

## Data Classification

| Data Type | Collected? | Stored? | Transmitted? |
|-----------|-----------|---------|--------------|
| Payment card numbers | Simulated input only | **Never** | **Never** |
| CVV / PIN | **Never** | **Never** | **Never** |
| Real OTP/SMS codes | **Never** | **Never** | **Never** |
| Passwords | **Never** | **Never** | **Never** |
| Full name | Bot conversation only | **Never** (URL fragment → sessionStorage) | **Never** |
| Phone number | Bot conversation only | **Never** (URL fragment → sessionStorage) | **Never** |
| Telegram user ID | Hashed | Yes (SHA-256 hash) | Bot → API only |
| Session token | Yes | Yes (anonymous UUID) | Yes |
| Quiz scores | Yes | Yes (numeric only) | Yes |

## Implemented Security Controls

### 1. Client-Side Sensitive Data Protection

- **Luhn algorithm validation** rejects real payment card patterns before any processing
- **Training OTP codes** are randomly generated in the browser; only the generated code is accepted
- **Input fields cleared** immediately after simulation step completion
- **sessionStorage** used for local-only PII (name for certificate); cleared on tab close

### 2. Server-Side Protections

- API endpoints **explicitly reject** requests containing sensitive field names (card, cvv, otp, password, pin)
- Session model stores **no PII** — only anonymous tokens and progress flags
- Telegram user IDs stored as **one-way SHA-256 hashes** with application salt
- Quiz submission accepts only **question IDs and option indices**

### 3. Authentication & Authorization

- Admin panel protected by **JWT tokens** (8-hour expiry)
- Admin credentials configured via environment variables
- Admin audit log tracks login events with IP addresses

### 4. Transport Security

- Production deployment requires **HTTPS** (documented in deployment guide)
- CORS restricted to configured origins
- No sensitive data in URL query parameters (PII uses URL fragments)

### 5. Educational Safeguards

- Disclaimers displayed on every page
- Bot messages clearly label content as educational simulation
- Reveal page explicitly states the activity was a simulation
- Certificate notes educational purpose

## API Security Review

| Endpoint | Method | Auth | Sensitive Data Risk |
|----------|--------|------|---------------------|
| `/api/sessions` | POST | None | Low — only hashed Telegram ID |
| `/api/sessions/{token}` | GET | Token | None |
| `/api/sessions/{token}/progress` | PATCH | Token | None — boolean flags only |
| `/api/quiz/questions` | GET | None | None — no answers exposed |
| `/api/quiz/submit` | POST | Token | Low — option indices only |
| `/api/admin/login` | POST | None | Medium — rate limiting recommended |
| `/api/admin/stats` | GET | JWT | None — aggregate stats only |

## Recommendations for Production

1. **Rate limiting** on `/api/admin/login` and `/api/sessions` (e.g., slowapi)
2. **WAF/CDN** in front of public endpoints
3. **Regular dependency updates** (`pip audit`, Dependabot)
4. **Log monitoring** for unusual session creation patterns
5. **Penetration test** before organizational-wide rollout

## Residual Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| User enters real card despite warnings | Low | Luhn rejection + client-side only |
| Admin credential brute force | Medium | Strong password + rate limiting |
| Misuse as actual phishing tool | Medium | Educational disclaimers; deploy only in controlled training environments |
| SQLite file access on server | Low | File permissions, encrypted volumes |

## Compliance Notes

This platform is designed for **voluntary cybersecurity awareness training**. Organizations deploying it should:

- Obtain informed consent from participants
- Clearly communicate the educational purpose before training
- Not deploy without organizational authorization
- Comply with local data protection regulations for any analytics data

## Conclusion

The platform implements defense-in-depth controls appropriate for an educational simulation. No real financial credentials are collected or transmitted. Deployment in production requires HTTPS, strong admin credentials, and organizational governance.
