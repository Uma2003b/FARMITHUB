document.addEventListener('DOMContentLoaded', () => {
  const headerButtons = document.querySelector('.header-buttons');
  if (!headerButtons) return;

  const appsDropdownHTML = `
    <div class="apps-dropdown">
      <button class="apps-btn" id="appsBtn">📱 Apps</button>
      <div class="dropdown-menu" id="appsMenu">
        <div class="dropdown-category">🌾 Farming Tools</div>
        <a href="/crop_recommendation/"><span>🌱</span> Crop Recommendation</a>
        <a href="/crop_yield/"><span>📊</span> Yield Prediction</a>
        <a href="disease.html"><span>🔬</span> Disease Detection</a>
        <a href="weather.html"><span>⛅</span> Weather Check</a>
        <a href="/crop_planning/"><span>📅</span> Crop Planning</a>
        <a href="organic.html"><span>🌿</span> Organic Farming</a>
        <a href="plantation.html"><span>🌳</span> Plantation Guide</a>
        <div class="dropdown-category">💼 Market & Trade</div>
        <a href="/crop_price_tracker/crop_price_tracker"><span>💰</span> Price Tracker</a>
        <a href="farmer.html"><span>👥</span> Farmer Network</a>
        <a href="shopkeeper.html"><span>🏪</span> Shop Listings</a>
        <div class="dropdown-category">📢 Community</div>
        <a href="chat.html"><span>🤖</span> AI Assistant</a>
        <a href="Forum/forum.html"><span>💬</span> Farmer Forum</a>
        <a href="./Labour_Alerts/templates/labour.html"><span>⚠️</span> Labour Alerts</a>
      </div>
    </div>
  `;

  const appsDropdownCSS = `
    <style>
      .apps-dropdown { position: relative; }
      .apps-btn { background: rgba(255,255,255,0.15); color: white; padding: 0.6rem 1.2rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; transition: all 0.3s; font-weight: 500; }
      .apps-btn:hover { background: rgba(255,255,255,0.25); transform: translateY(-2px); }
      .dropdown-menu { position: fixed; top: 85px; right: 2rem; background: white; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); min-width: 300px; max-height: 450px; overflow-y: auto; z-index: 1005; display: none; }
      .dropdown-menu.show { display: block; }
      .dropdown-menu a { display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem 1rem; color: #333; text-decoration: none; transition: all 0.2s; border-bottom: 1px solid #f0f0f0; }
      .dropdown-menu a:last-child { border-bottom: none; }
      .dropdown-menu a:hover { background: #f5f5f5; padding-left: 1.2rem; }
      .dropdown-menu a span { font-size: 1.2rem; min-width: 1.5rem; }
      .dropdown-category { padding: 0.8rem 1rem; font-weight: 600; font-size: 0.8rem; color: #666; text-transform: uppercase; background: #f9f9f9; border-bottom: 1px solid #e0e0e0; }
    </style>
  `;

  document.head.insertAdjacentHTML('beforeend', appsDropdownCSS);
  headerButtons.insertAdjacentHTML('afterbegin', appsDropdownHTML);

  const appsBtn = document.getElementById('appsBtn');
  const appsMenu = document.getElementById('appsMenu');
  
  appsBtn.onclick = (e) => { 
    e.stopPropagation(); 
    appsMenu.classList.toggle('show'); 
  };
  
  appsMenu.querySelectorAll('a').forEach(a => {
    a.onclick = () => appsMenu.classList.remove('show');
  });
  
  document.onclick = () => appsMenu.classList.remove('show');
});
