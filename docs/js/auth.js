if (localStorage.getItem('token')) {
  redirectByRole(localStorage.getItem('role'));
}

function redirectByRole(role) {
  if (role === 'superadmin') location.href = 'pages/superadmin.html';
  else if (role === 'admin') location.href = 'pages/admin.html';
  else location.href = 'pages/member.html';
}

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const res = await API.login({ email, password });

  if (res.token) {
    localStorage.setItem('token', res.token);
    localStorage.setItem('role', res.role);
    localStorage.setItem('name', res.name);
    redirectByRole(res.role);
  } else {
    document.getElementById('error').textContent=res.message;
  }
});