// Анимация при загрузке
        document.addEventListener('DOMContentLoaded', () => {
            const items = document.querySelectorAll('.detail-item, .skill-tag, .stat-card');

            items.forEach((item, index) => {
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 100 * index);
            });

            // Добавляем эффект пульсации при наведении на фото
            const profilePic = document.querySelector('.profile-pic');
            profilePic.addEventListener('mouseenter', () => {
                profilePic.classList.add('pulse');
            });

            profilePic.addEventListener('mouseleave', () => {
                setTimeout(() => {
                    profilePic.classList.remove('pulse');
                }, 2000);
            });
        });