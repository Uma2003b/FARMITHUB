// Shared Footer Loader
document.addEventListener('DOMContentLoaded', function() {
  // Create footer if it doesn't exist
  if (!document.querySelector('.site-footer')) {
    const footerHTML = `
      <style>
        .site-footer {
          background: linear-gradient(135deg, #2e7d32, #66bb6a);
          color: #fff;
          margin-top: auto;
          padding: 1.5rem;
          text-align: center;
          font-size: 0.9rem;
        }
        .site-footer a {
          color: #fff;
          text-decoration: none;
        }
        .site-footer a:hover {
          text-decoration: underline;
        }
      </style>
      <footer class="site-footer">

      </footer>
    `;
    
    // Insert footer before closing body tag
    document.body.insertAdjacentHTML('beforeend', footerHTML);
  }
});
