/**
 * Interactive cybersecurity quiz — submits only question IDs and option indices.
 */

let questions = [];
let currentIndex = 0;
let answers = {};

document.addEventListener('DOMContentLoaded', async () => {
  const token = getSessionToken();
  if (!token) {
    window.location.href = '/';
    return;
  }

  try {
    const res = await fetch('/api/quiz/questions');
    const data = await res.json();
    questions = data.questions;
    renderQuestion();
  } catch (e) {
    document.getElementById('quiz-container').innerHTML =
      '<div class="alert alert-danger">Failed to load quiz. Please refresh.</div>';
  }

  document.getElementById('quiz-next')?.addEventListener('click', nextQuestion);
  document.getElementById('quiz-prev')?.addEventListener('click', prevQuestion);
  document.getElementById('quiz-submit')?.addEventListener('click', submitQuiz);
});

function renderQuestion() {
  const q = questions[currentIndex];
  if (!q) return;

  document.getElementById('quiz-progress').textContent =
    `Question ${currentIndex + 1} of ${questions.length}`;
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
    alert('Please select an answer before continuing.');
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
    alert('Please select an answer before submitting.');
    return;
  }

  const token = getSessionToken();
  const submitBtn = document.getElementById('quiz-submit');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';

  try {
    const res = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_token: token,
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
    alert('Failed to submit quiz. Please try again.');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit Quiz';
  }
}

function showResults(result) {
  document.getElementById('quiz-form').classList.add('d-none');
  const resultsEl = document.getElementById('quiz-results');
  resultsEl.classList.remove('d-none');

  document.getElementById('quiz-score').textContent =
    `${result.score} / ${result.total} (${result.percentage}%)`;

  const explanationsEl = document.getElementById('quiz-explanations');
  explanationsEl.innerHTML = '';

  result.explanations.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'learn-card mb-3';
    div.innerHTML = `
      <h5>Q${idx + 1}: ${item.is_correct ? '✅' : '❌'} ${item.question}</h5>
      <p><strong>Your answer:</strong> ${item.your_answer}</p>
      <p><strong>Correct answer:</strong> ${item.correct_answer}</p>
      <p class="text-info">${item.explanation}</p>
    `;
    explanationsEl.appendChild(div);
  });

  document.getElementById('cert-link').href =
    `/certificate?id=${result.certificate_id}&score=${result.percentage}`;
}
