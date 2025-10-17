document.getElementById('forumForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const data = {
    name: e.target.name.value,
    message: e.target.message.value
  };

  const text = `${data.name}: ${data.message}`;

  if (navigator.onLine) {
    // Online: post to server
    fetch('http://localhost:5000/forum', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(() => {
        loadPosts();
        e.target.reset();
        showToast('Post submitted successfully!', 'success');
      })
      .catch(() => {
        // If fetch fails, save offline
        saveComplaintOffline(text);
        e.target.reset();
      });
  } else {
    // Offline: save to localStorage
    saveComplaintOffline(text);
    e.target.reset();
  }
});


function loadPosts() {
  fetch('http://localhost:5000/forum')
    .then(res => res.json())
    .then(posts => {
      const container = document.getElementById('forumPosts');
      container.innerHTML = '';
      posts.forEach(post => {
        const el = document.createElement('div');
        el.className = 'forum-post';
        el.innerHTML = `<strong>${post.name}</strong>: ${post.message}`;
        container.appendChild(el);
      });
    });
}


document.addEventListener('DOMContentLoaded', loadPosts);

// Save complaint offline in localStorage
function saveComplaintOffline(text) {
  if (!text) return;

  let complaints = JSON.parse(localStorage.getItem('offlineComplaints')) || [];
  complaints.push({ text: text, timestamp: new Date().toISOString() });
  localStorage.setItem('offlineComplaints', JSON.stringify(complaints));

  showToast('Complaint saved offline. It will be submitted when you are back online.', 'warning');
}

// Toast notification function
function showToast(message, type) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = 'toast show';

  if (type === 'success') {
    toast.style.backgroundColor = '#4BB543'; // green
  } else if (type === 'warning') {
    toast.style.backgroundColor = '#ff9800'; // orange
  } else {
    toast.style.backgroundColor = '#333'; // default
  }

  setTimeout(() => {
    toast.className = toast.className.replace('show', '');
  }, 3000);
}



