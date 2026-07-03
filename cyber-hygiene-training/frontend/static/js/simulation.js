/**
 * Payment flow — realistic UI, security checks remain client-side only.
 * Real card numbers blocked silently with generic bank-style errors.
 */

document.addEventListener('DOMContentLoaded', () => {
  const token = getSessionToken();
  if (!token) {
    window.location.href = '/';
    return;
  }

  const trainingCode = generateTrainingCode();
  const codeDisplay = document.getElementById('training-code');
  if (codeDisplay) codeDisplay.textContent = trainingCode;

  const smsTime = document.getElementById('sms-time');
  if (smsTime) {
    const now = new Date();
    smsTime.textContent = now.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' });
  }

  const cardInput = document.getElementById('card-input');
  const cardWarning = document.getElementById('card-warning');
  const otpInput = document.getElementById('otp-input');
  const otpWarning = document.getElementById('otp-warning');
  const submitBtn = document.getElementById('submit-simulation');
  const step1 = document.getElementById('step-card');
  const step2 = document.getElementById('step-otp');

  let cardValid = false;
  let otpValid = false;

  if (cardInput) {
    cardInput.addEventListener('input', (e) => {
      e.target.value = formatCardInput(e.target.value);
      cardWarning.classList.add('d-none');
      cardWarning.textContent = '';

      const raw = e.target.value.replace(/\s/g, '');
      if (raw.length === 0) {
        cardValid = false;
        return;
      }

      // Haqiqiy karta bloklanadi — umumiy bank xabari ko'rsatiladi
      if (isRealCardPattern(raw)) {
        cardWarning.textContent =
          'Karta ma\'lumotlari qabul qilinmadi. Iltimos, boshqa karta kiriting yoki ma\'lumotlarni tekshiring.';
        cardWarning.classList.remove('d-none');
        cardValid = false;
        return;
      }

      cardValid = raw.length >= 13 && raw.length <= 19;
    });
  }

  document.getElementById('next-to-otp')?.addEventListener('click', () => {
    if (!cardValid) {
      cardWarning.textContent = 'Iltimos, to\'g\'ri karta raqamini kiriting.';
      cardWarning.classList.remove('d-none');
      return;
    }
    step1.classList.add('d-none');
    step2.classList.remove('d-none');
    if (cardInput) cardInput.value = '';
  });

  if (otpInput) {
    otpInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6);
      otpWarning.classList.add('d-none');

      if (e.target.value.length === 6) {
        if (e.target.value === trainingCode) {
          otpValid = true;
        } else {
          otpWarning.textContent = 'Noto\'g\'ri tasdiqlash kodi. Qayta urinib ko\'ring.';
          otpWarning.classList.remove('d-none');
          otpValid = false;
        }
      } else {
        otpValid = false;
      }
    });
  }

  submitBtn?.addEventListener('click', async () => {
    if (!otpValid) {
      otpWarning.textContent = '6 xonali SMS kodni kiriting.';
      otpWarning.classList.remove('d-none');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Tekshirilmoqda...';

    sessionStorage.removeItem(TRAINING_CODE_KEY);
    if (cardInput) cardInput.value = '';
    if (otpInput) otpInput.value = '';

    await new Promise((r) => setTimeout(r, 1500));

    await updateProgress({ simulation_completed: true });
    window.location.href = '/reveal';
  });
});
