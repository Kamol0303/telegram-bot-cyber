/**
 * Payment simulation — all card/OTP validation is client-side only.
 * Real card numbers and OTP codes are rejected and never transmitted.
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

      if (isRealCardPattern(raw)) {
        cardWarning.textContent =
          'For your safety, please do not enter a real payment card. This is only a simulation.';
        cardWarning.classList.remove('d-none');
        cardValid = false;
        return;
      }

      if (raw.length >= 13 && raw.length <= 19) {
        cardValid = true;
      } else {
        cardValid = false;
      }
    });
  }

  document.getElementById('next-to-otp')?.addEventListener('click', () => {
    if (!cardValid) {
      cardWarning.textContent = 'Please enter a simulated card number (not a real one).';
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
          otpWarning.textContent =
            'Incorrect training code. Use the code shown above — do NOT enter a real banking SMS code.';
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
      otpWarning.textContent = 'Enter the 6-digit training code displayed on this page.';
      otpWarning.classList.remove('d-none');
      return;
    }

    sessionStorage.removeItem(TRAINING_CODE_KEY);
    if (cardInput) cardInput.value = '';
    if (otpInput) otpInput.value = '';

    await updateProgress({ simulation_completed: true });
    window.location.href = '/reveal';
  });
});
