// Обработка сайдбара и подменю
document.addEventListener('DOMContentLoaded', function() {
    // Кнопка мобильного меню
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('active');
        });
    }

    // Раскрывающиеся подменю
    document.querySelectorAll('[data-toggle="collapse"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target.classList.toggle('show');
            this.closest('.nav-item').classList.toggle('active');
        });
    });
});