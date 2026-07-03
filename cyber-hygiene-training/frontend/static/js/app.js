/**
 * Cyber Hygiene Training — Client-side security utilities.
 * All sensitive validation happens locally; nothing is transmitted to servers.
 */

const SESSION_KEY = 'cht_session';
const PII_KEY = 'cht_pii';
const TRAINING_CODE_KEY = 'cht_training_code';
const QUIZ_RESULT_KEY = 'cht_quiz_result';

/**
 * Parse URL parameters and fragment for session token and local PII.
 * PII from URL fragment is moved to sessionStorage and stripped from URL.
 */
function initSessionFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');
  if (token) {
    sessionStorage.setItem(SESSION_KEY, token);
  }

  const hash = window.location.hash.slice(1);
  if (hash) {
    const fragmentParams = new URLSearchParams(hash);
    const name = fragmentParams.get('name');
    const phone = fragmentParams.get('phone');
    if (name || phone) {
      sessionStorage.setItem(PII_KEY, JSON.stringify({
        name: name ? decodeURIComponent(name) : 'Trainee',
        phone: phone ? decodeURIComponent(phone) : '',
      }));
      history.replaceState(null, '', window.location.pathname + window.location.search);
    }
  }

  return sessionStorage.getItem(SESSION_KEY);
}

function getSessionToken() {
  return sessionStorage.getItem(SESSION_KEY);
}

function getDisplayName() {
  try {
    const pii = JSON.parse(sessionStorage.getItem(PII_KEY) || '{}');
    return pii.name || 'Trainee';
  } catch {
    return 'Trainee';
  }
}

/**
 * Luhn algorithm — detects real payment card numbers to block them.
 */
function luhnCheck(cardNumber) {
  const digits = cardNumber.replace(/\D/g, '');
  if (digits.length < 13 || digits.length > 19) return false;

  let sum = 0;
  let alternate = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let n = parseInt(digits[i], 10);
    if (alternate) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    sum += n;
    alternate = !alternate;
  }
  return sum % 10 === 0;
}

/**
 * Check if input looks like a real card number pattern.
 */
function isRealCardPattern(value) {
  const digits = value.replace(/\D/g, '');
  if (digits.length < 13) return false;

  const knownPrefixes = /^(4|5[1-5]|3[47]|6(?:011|5))/;
  if (knownPrefixes.test(digits) && luhnCheck(digits)) {
    return true;
  }
  if (digits.length === 16 && luhnCheck(digits)) {
    return true;
  }
  return false;
}

/**
 * Generate a random 6-digit training OTP code — never a real banking code.
 */
function generateTrainingCode() {
  const code = String(Math.floor(100000 + Math.random() * 900000));
  sessionStorage.setItem(TRAINING_CODE_KEY, code);
  return code;
}

function getTrainingCode() {
  return sessionStorage.getItem(TRAINING_CODE_KEY);
}

/**
 * Update non-sensitive progress flags on the server.
 */
async function updateProgress(flags) {
  const token = getSessionToken();
  if (!token) return;
  try {
    await fetch(`/api/sessions/${token}/progress`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(flags),
    });
  } catch (e) {
    console.warn('Progress update failed (non-critical):', e);
  }
}

/**
 * Format card input with spaces (display only).
 */
function formatCardInput(value) {
  const digits = value.replace(/\D/g, '').slice(0, 16);
  return digits.replace(/(.{4})/g, '$1 ').trim();
}

function saveQuizResult(result) {
  sessionStorage.setItem(QUIZ_RESULT_KEY, JSON.stringify(result));
}

function getQuizResult() {
  try {
    return JSON.parse(sessionStorage.getItem(QUIZ_RESULT_KEY) || 'null');
  } catch {
    return null;
  }
}

/**
 * Countdown timer for scam landing page urgency effect.
 */
function startCountdown(elementId, seconds) {
  const el = document.getElementById(elementId);
  if (!el) return;

  let remaining = seconds;
  const tick = () => {
    const mins = Math.floor(remaining / 60);
    const secs = remaining % 60;
    el.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    if (remaining <= 0) {
      el.textContent = '00:00';
      el.style.animation = 'blink 0.5s infinite';
      return;
    }
    remaining--;
    setTimeout(tick, 1000);
  };
  tick();
}

/**
 * Animated winner ticker for fake lottery page.
 */
function initWinnerTicker() {
  const names = [
    'Akmal T. won BYD Champion!',
    'Dilnoza K. won iPhone 17!',
    'Jasur M. won 5,000,000 UZS!',
    'Nodira S. won Apartment!',
    'Bobur R. won Luxury Car!',
    'Malika H. won iPhone 17!',
    'Sardor A. won 5,000,000 UZS!',
  ];
  const ticker = document.getElementById('winner-ticker-text');
  if (ticker) {
    ticker.textContent = names.join('  ★  ') + '  ★  ';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initSessionFromUrl();
});
