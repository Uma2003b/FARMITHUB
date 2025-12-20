// Strict Session Management - Prevent unauthorized back button access
(function() {
  const publicPages = ['index.html', 'login.html', 'about.html'];
  
  function isPublicPage() {
    return publicPages.some(page => window.location.pathname.includes(page) || window.location.href.includes(page));
  }

  function isLoggedIn() {
    return !!localStorage.getItem('currentUser');
  }

  function redirectToLogin() {
    window.location.replace('/login.html');
  }

  // Check session on page load - redirect to login if not logged in and not on public page
  window.addEventListener('load', function() {
    if (!isLoggedIn() && !isPublicPage() && window.location.pathname.includes('/main')) {
      redirectToLogin();
    }
  });

  // Clear history and logout
  window.logout = function() {
    localStorage.removeItem('currentUser');
    sessionStorage.clear();
    window.onpopstate = null;
    window.history.pushState(null, null, window.location.href);
    window.history.pushState(null, null, window.location.href);
    window.location.replace('/index.html');
  };

  // Block back on index page
  window.blockBackOnIndex = function() {
    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function() {
      window.history.pushState(null, null, window.location.href);
    };
  };

  // Block back button on main.html - redirect to logout
  window.blockBackOnMain = function() {
    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function() {
      window.logout();
    };
  };
})();
