// Only run on protected pages, not on main.html
if (!window.location.pathname.includes('main.html') && !window.location.pathname.endsWith('/main')) {
  if (!localStorage.getItem('currentUser')) {
    window.location.href = '/login.html';
  }
}
