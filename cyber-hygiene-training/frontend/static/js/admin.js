/**
 * Admin panel client — JWT auth for platform statistics.
 */

document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('cht_admin_token');
  if (token) {
    showDashboard(token);
  }

  document.getElementById('admin-login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('admin-user').value;
    const password = document.getElementById('admin-pass').value;
    const errorEl = document.getElementById('login-error');

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) throw new Error('Invalid credentials');
      const data = await res.json();
      localStorage.setItem('cht_admin_token', data.access_token);
      errorEl.classList.add('d-none');
      showDashboard(data.access_token);
    } catch {
      errorEl.textContent = 'Invalid username or password.';
      errorEl.classList.remove('d-none');
    }
  });

  document.getElementById('admin-logout')?.addEventListener('click', () => {
    localStorage.removeItem('cht_admin_token');
    document.getElementById('admin-dashboard').classList.add('d-none');
    document.getElementById('admin-login').classList.remove('d-none');
  });
});

async function showDashboard(token) {
  document.getElementById('admin-login').classList.add('d-none');
  document.getElementById('admin-dashboard').classList.remove('d-none');

  try {
    const res = await fetch('/api/admin/stats', {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Unauthorized');
    const stats = await res.json();

    document.getElementById('stat-sessions').textContent = stats.total_sessions;
    document.getElementById('stat-simulations').textContent = stats.completed_simulations;
    document.getElementById('stat-quizzes').textContent = stats.completed_quizzes;
    document.getElementById('stat-avg-score').textContent = `${stats.average_quiz_score}%`;

    const tbody = document.getElementById('recent-sessions-body');
    tbody.innerHTML = '';
    stats.recent_sessions.forEach((s) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${s.id}...</td>
        <td>${s.landing ? '✅' : '—'}</td>
        <td>${s.simulation ? '✅' : '—'}</td>
        <td>${s.quiz ? '✅' : '—'}</td>
        <td>${s.created ? new Date(s.created).toLocaleString() : '—'}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch {
    localStorage.removeItem('cht_admin_token');
    document.getElementById('admin-dashboard').classList.add('d-none');
    document.getElementById('admin-login').classList.remove('d-none');
  }
}
