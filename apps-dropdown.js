document.addEventListener("DOMContentLoaded", function () {
  const style = document.createElement('style');
  style.textContent = `.apps-dropdown{position:relative}.apps-btn{background:rgba(255,255,255,.15);color:#fff;padding:.6rem 1.2rem;border-radius:8px;border:1px solid rgba(255,255,255,.2);cursor:pointer;font-size:.9rem;display:flex;align-items:center;gap:.5rem;transition:all .3s;font-weight:500}.apps-btn:hover{background:rgba(255,255,255,.25);transform:translateY(-2px)}.dropdown-menu{position:fixed;top:85px;right:2rem;background:#fff;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.2);min-width:300px;max-height:450px;overflow-y:auto;z-index:1005;display:none}.dropdown-menu.show{display:block}.dropdown-menu a{display:flex;align-items:center;gap:.8rem;padding:.8rem 1rem;color:#333;text-decoration:none;transition:all .2s;border-bottom:1px solid #f0f0f0}.dropdown-menu a:hover{background:#f5f5f5;padding-left:1.2rem}.dropdown-menu a span{font-size:1.2rem;min-width:1.5rem}.dropdown-category{padding:.8rem 1rem;font-weight:600;font-size:.8rem;color:#666;text-transform:uppercase;background:#f9f9f9;border-bottom:1px solid #e0e0e0}`;
  document.head.appendChild(style);

  const hdrBtns = document.querySelector('.header-buttons');
  if (hdrBtns && !document.getElementById('appsBtn')) {
    const dropdownDiv = document.createElement('div');
    dropdownDiv.className = 'apps-dropdown';
    
    const btn = document.createElement('button');
    btn.className = 'apps-btn';
    btn.id = 'appsBtn';
    btn.innerHTML = '&#128241; Apps';
    
    const menu = document.createElement('div');
    menu.className = 'dropdown-menu';
    menu.id = 'appsMenu';
    
    const categories = [
      { title: '&#127807; Farming Tools', items: [
        { emoji: '&#127793;', text: 'Crop Recommendation', href: '/crop_recommendation/' },
        { emoji: '&#128202;', text: 'Yield Prediction', href: '/crop_yield/' },
        { emoji: '&#128300;', text: 'Disease Detection', href: 'disease.html' },
        { emoji: '&#9925;', text: 'Weather Check', href: 'weather.html' },
        { emoji: '&#128197;', text: 'Crop Planning', href: '/crop_planning/' },
        { emoji: '&#127807;', text: 'Organic Farming', href: 'organic.html' },
        { emoji: '&#127795;', text: 'Plantation Guide', href: 'plantation.html' }
      ]},
      { title: '&#128188; Market & Trade', items: [
        { emoji: '&#128176;', text: 'Price Tracker', href: '/crop_price_tracker/crop_price_tracker' },
        { emoji: '&#128101;', text: 'Farmer Network', href: 'farmer.html' },
        { emoji: '&#127978;', text: 'Shop Listings', href: 'shopkeeper.html' }
      ]},
      { title: '&#128242; Community', items: [
        { emoji: '&#129302;', text: 'AI Assistant', href: 'chat.html' },
        { emoji: '&#128172;', text: 'Farmer Forum', href: 'Forum/forum.html' },
        { emoji: '&#9888;', text: 'Labour Alerts', href: './Labour_Alerts/templates/labour.html' }
      ]}
    ];
    
    categories.forEach(cat => {
      const catDiv = document.createElement('div');
      catDiv.className = 'dropdown-category';
      catDiv.innerHTML = cat.title;
      menu.appendChild(catDiv);
      
      cat.items.forEach(item => {
        const link = document.createElement('a');
        link.href = item.href;
        const span = document.createElement('span');
        span.innerHTML = item.emoji;
        link.appendChild(span);
        link.appendChild(document.createTextNode(' ' + item.text));
        menu.appendChild(link);
      });
    });
    
    dropdownDiv.appendChild(btn);
    dropdownDiv.appendChild(menu);
    hdrBtns.insertBefore(dropdownDiv, hdrBtns.firstChild);
    
    const appsBtn = document.getElementById('appsBtn');
    const appsMenu = document.getElementById('appsMenu');
    appsBtn.onclick = (e) => { e.stopPropagation(); appsMenu.classList.toggle('show'); };
    appsMenu.querySelectorAll('a').forEach(a => a.onclick = () => appsMenu.classList.remove('show'));
    document.onclick = () => appsMenu.classList.remove('show');
  }
});
