document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('theme-toggle');
    const root = document.documentElement;
    const icon = toggleBtn.querySelector('i');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        root.setAttribute('data-bs-theme', savedTheme);
        icon.className = savedTheme === 'light' ? 'bi bi-moon' : 'bi bi-sun';
    }

    toggleBtn.addEventListener('click', () => {
        const currentTheme = root.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        root.setAttribute('data-bs-theme', newTheme);
        icon.className = newTheme === 'light' ? 'bi bi-moon' : 'bi bi-sun';
        localStorage.setItem('theme', newTheme);  // Save to localStorage
    });
});
