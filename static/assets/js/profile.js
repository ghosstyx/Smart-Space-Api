document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle) {
        // Показываем кнопку только на мобильных
        function checkScreenSize() {
            if (window.innerWidth <= 992) {
                sidebarToggle.style.display = 'block';
                sidebar.classList.remove('active');
            } else {
                sidebarToggle.style.display = 'none';
                sidebar.classList.add('active');
            }
        }

        // Проверяем при загрузке и ресайзе
        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);

        // Обработчик клика
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Анимация аватара (оставляем как было)
    const profilePic = document.querySelector('.profile-pic');
    if (profilePic) {
        profilePic.addEventListener('mouseenter', () => profilePic.classList.add('pulse'));
        profilePic.addEventListener('mouseleave', () => setTimeout(() => profilePic.classList.remove('pulse'), 2000));
        profilePic.addEventListener('touchstart', () => profilePic.classList.add('pulse'));
        profilePic.addEventListener('touchend', () => setTimeout(() => profilePic.classList.remove('pulse'), 1000));
    }
});