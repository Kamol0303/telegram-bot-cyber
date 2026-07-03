/**
 * Payment flow — realistic UI, security checks remain client-side only.
 */

let trainingCodeGlobal = '';

document.addEventListener('DOMContentLoaded', () => {
  const token = getSessionToken();
  if (!token) {
    window.location.href = '/';
    return;
  }

  trainingCodeGlobal = generateTrainingCode();
  updateTrainingCodeDisplay();

  const smsTime = document.getElementById('sms-time');
  if (smsTime) {
    const now = new Date();
    smsTime.textContent = now.toLocaleTimeString(getLocaleForDate(), {
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  const cardInput = document.getElementById('card-input');
  const expiryInput = document.getElementById('expiry-input');
  const cvvInput = document.getElementById('cvv-input');
  const cardWarning = document.getElementById('card-warning');
  const otpInput = document.getElementById('otp-input');
  const otpWarning = document.getElementById('otp-warning');
  const submitBtn = document.getElementById('submit-simulation');
  const step1 = document.getElementById('step-card');
  const step2 = document.getElementById('step-otp');

  let cardValid = false;
  let expiryValid = false;
  let cvvValid = false;
  let otpValid = false;

  function showCardError(key) {
    cardWarning.textContent = t(key);
    cardWarning.classList.remove('d-none');
  }

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
        showCardError('simulation.err_card_rejected');
        cardValid = false;
        return;
      }

      cardValid = raw.length >= 13 && raw.length <= 19;
    });
  }

  if (expiryInput) {
    expiryInput.addEventListener('keydown', (e) => {
      if (e.key.length === 1 && !/\d/.test(e.key)) {
        e.preventDefault();
      }
    });

    expiryInput.addEventListener('input', (e) => {
      e.target.value = formatExpiryInput(e.target.value);
      cardWarning.classList.add('d-none');
      expiryValid = isValidExpiry(e.target.value);
    });

    expiryInput.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasted = (e.clipboardData || window.clipboardData).getData('text');
      e.target.value = formatExpiryInput(pasted);
      expiryValid = isValidExpiry(e.target.value);
    });
  }

  if (cvvInput) {
    cvvInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
      cardWarning.classList.add('d-none');
      cvvValid = e.target.value.length === 3;
    });
  }

  document.getElementById('next-to-otp')?.addEventListener('click', () => {
    if (!cardValid) {
      showCardError('simulation.err_card_invalid');
      return;
    }
    if (!expiryValid) {
      showCardError('simulation.err_expiry_invalid');
      return;
    }
    if (!cvvValid) {
      showCardError('simulation.err_cvv_invalid');
      return;
    }

    step1.classList.add('d-none');
    step2.classList.remove('d-none');
    if (cardInput) cardInput.value = '';
    if (expiryInput) expiryInput.value = '';
    if (cvvInput) cvvInput.value = '';
    cardValid = false;
    expiryValid = false;
    cvvValid = false;
  });

  if (otpInput) {
    otpInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6);
      otpWarning.classList.add('d-none');

      if (e.target.value.length === 6) {
        if (e.target.value === trainingCodeGlobal) {
          otpValid = true;
        } else {
          otpWarning.textContent = t('simulation.err_otp_wrong');
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
      otpWarning.textContent = t('simulation.err_otp_empty');
      otpWarning.classList.remove('d-none');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = t('simulation.checking');

    sessionStorage.removeItem(TRAINING_CODE_KEY);
    if (otpInput) otpInput.value = '';

    await new Promise((r) => setTimeout(r, 1500));

    await updateProgress({ simulation_completed: true });
    window.location.href = '/reveal';
  });

  window.addEventListener('languageChanged', () => {
    updateTrainingCodeDisplay();
    if (smsTime) {
      const now = new Date();
      smsTime.textContent = now.toLocaleTimeString(getLocaleForDate(), {
        hour: '2-digit',
        minute: '2-digit',
      });
    }
    if (submitBtn && !submitBtn.disabled) {
      submitBtn.textContent = t('simulation.submit_btn');
    }
  });
});

function updateTrainingCodeDisplay() {
  const codeDisplay = document.getElementById('training-code');
  if (codeDisplay && trainingCodeGlobal) {
    codeDisplay.textContent = trainingCodeGlobal;
  }
}
