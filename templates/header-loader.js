document.addEventListener('DOMContentLoaded', function() {
  // Load header
  if (!document.querySelector('.uniform-header')) {
    fetch('header.html')
      .then(response => response.text())
      .then(html => {
        const wrapper = document.createElement('div');
        wrapper.className = 'header-nav-wrapper';
        wrapper.innerHTML = html;
        document.body.insertBefore(wrapper, document.body.firstChild);
      })
      .catch(err => console.error('Failed to load header:', err));
  }

  // Load footer
  if (!document.querySelector('.site-footer')) {
    fetch('footer.html')
      .then(response => response.text())
      .then(html => {
        document.body.insertAdjacentHTML('beforeend', html);
      })
      .catch(err => console.error('Failed to load footer:', err));
  }
});
