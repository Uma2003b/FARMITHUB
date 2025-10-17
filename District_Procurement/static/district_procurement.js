// District Procurement JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // Update button text
            const themeText = this.querySelector('.theme-text');
            if (themeText) {
                themeText.textContent = newTheme === 'dark' ? 'Dark' : 'Light';
            }
        });
    }

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeText = document.querySelector('.theme-text');
    if (themeText) {
        themeText.textContent = savedTheme === 'dark' ? 'Dark' : 'Light';
    }

    // Filter form enhancement
    const filterForm = document.querySelector('.filters-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Show loading state
            const submitBtn = this.querySelector('.btn-filter');
            if (submitBtn) {
                submitBtn.textContent = 'Loading...';
                submitBtn.disabled = true;
            }
        });
    }

    // Table sorting functionality
    const table = document.querySelector('.data-table');
    if (table) {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        });
    }
});

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Toggle sort direction
    const isAscending = table.getAttribute('data-sort-dir') !== 'asc';
    table.setAttribute('data-sort-dir', isAscending ? 'asc' : 'desc');

    rows.sort((a, b) => {
        const aVal = a.cells[column].textContent.trim();
        const bVal = b.cells[column].textContent.trim();

        // Try numeric comparison first
        const aNum = parseFloat(aVal.replace(/,/g, ''));
        const bNum = parseFloat(bVal.replace(/,/g, ''));

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }

        // String comparison
        return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    });

    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}
