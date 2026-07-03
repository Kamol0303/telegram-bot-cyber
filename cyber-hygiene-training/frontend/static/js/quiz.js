/**
 * Interactive cybersecurity quiz — multilingual UI and questions.
 */

let questions = [];
let currentIndex = 0;
let answers = {};

async function loadQuestions() {
  const lang = typeof getLang === 'function' ? getLang() : 'uz';
  const res = await fetch(`/api/quiz/questions?lang=${lang}`);
  const data = await res.json();
  questions = data.questions;
  currentIndex = 0;
  renderQuestion();
}

document.addEventListener('DOMContentLoaded', async () => {
  const token = getSessionToken();
  if (!token) {
    window.location.href = '/';
    return;
  }

  try {
    await loadQuestions();
  } catch (e) {
    const progress = document.getElementById('quiz-progress');
    if (progress) progress.textContent = t('quiz.load_fail');
  }

  document.getElementById('quiz-next')?.addEventListener('click', nextQuestion);
  document.getElementById('quiz-prev')?.addEventListener('click', prevQuestion);
  document.getElementById('quiz-submit')?.addEventListener('click', submitQuiz);

  window.addEventListener('languageChanged', async () => {
    const resultsVisible = !document.getElementById('quiz-results').classList.contains('d-none');
    if (resultsVisible) return;
    try {
      await loadQuestions();
    } catch (e) {
      /* keep current questions */
    }
  });
});

function renderQuestion() {
  const q = questions[currentIndex];
  if (!q) return;

  document.getElementById('quiz-progress').textContent = t('quiz.progress', {
    current: currentIndex + 1,
    total: questions.length,
  });
  document.getElementById('quiz-question').textContent = q.question;

  const optionsEl = document.getElementById('quiz-options');
  optionsEl.innerHTML = '';

  q.options.forEach((opt, idx) => {
    const div = document.createElement('div');
    div.className = 'quiz-option' + (answers[q.id] === idx ? ' selected' : '');
    div.textContent = opt;
    div.dataset.index = idx;
    div.addEventListener('click', () => selectOption(q.id, idx));
    optionsEl.appendChild(div);
  });

  document.getElementById('quiz-prev').style.display = currentIndex > 0 ? 'inline-block' : 'none';
  document.getElementById('quiz-next').style.display =
    currentIndex < questions.length - 1 ? 'inline-block' : 'none';
  document.getElementById('quiz-submit').style.display =
    currentIndex === questions.length - 1 ? 'inline-block' : 'none';
}

function selectOption(questionId, optionIndex) {
  answers[questionId] = optionIndex;
  renderQuestion();
}

function nextQuestion() {
  if (answers[questions[currentIndex].id] === undefined) {
    alert(t('quiz.select_answer'));
    return;
  }
  if (currentIndex < questions.length - 1) {
    currentIndex++;
    renderQuestion();
  }
}

function prevQuestion() {
  if (currentIndex > 0) {
    currentIndex--;
    renderQuestion();
  }
}

async function submitQuiz() {
  const q = questions[currentIndex];
  if (answers[q.id] === undefined) {
    alert(t('quiz.select_answer'));
    return;
  }

  const token = getSessionToken();
  const submitBtn = document.getElementById('quiz-submit');
  submitBtn.disabled = true;
  submitBtn.textContent = t('quiz.submitting');

  const lang = typeof getLang === 'function' ? getLang() : 'uz';

  try {
    const res = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_token: token,
        lang,
        answers: Object.fromEntries(
          Object.entries(answers).map(([k, v]) => [String(k), v])
        ),
      }),
    });

    if (!res.ok) throw new Error('Submit failed');
    const result = await res.json();
    saveQuizResult(result);
    showResults(result);
  } catch (e) {
    alert(t('quiz.submit_fail'));
    submitBtn.disabled = false;
    submitBtn.textContent = t('quiz.submit');
  }
}

function showResults(result) {
  document.getElementById('quiz-form').classList.add('d-none');
  const resultsEl = document.getElementById('quiz-results');
  resultsEl.classList.remove('d-none');

  document.getElementById('quiz-score').textContent = t('quiz.score', {
    score: result.score,
    total: result.total,
    percent: result.percentage,
  });

  const explanationsEl = document.getElementById('quiz-explanations');
  explanationsEl.innerHTML = '';

  result.explanations.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'learn-card mb-3';
    div.innerHTML = `
      <h5>Q${idx + 1}: ${item.is_correct ? '✅' : '❌'} ${item.question}</h5>
      <p><strong>${t('quiz.your_answer')}</strong> ${item.your_answer}</p>
      <p><strong>${t('quiz.correct_answer')}</strong> ${item.correct_answer}</p>
      <p class="text-info">${item.explanation}</p>
    `;
    explanationsEl.appendChild(div);
  });

  document.getElementById('cert-link').href =
    `/certificate?id=${result.certificate_id}&score=${result.percentage}`;
}
