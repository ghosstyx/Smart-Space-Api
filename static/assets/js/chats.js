// Анимация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Плавное появление контейнера
    document.querySelector('.chat-container').style.opacity = '0';
    setTimeout(() => {
        document.querySelector('.chat-container').style.transition = 'opacity 0.5s ease';
        document.querySelector('.chat-container').style.opacity = '1';
    }, 100);

    // Эффект волны при наведении на чат
    const chatItems = document.querySelectorAll('.chat-item');
    chatItems.forEach(item => {
        item.addEventListener('mouseenter', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const wave = document.createElement('div');
            wave.className = 'wave-effect';
            wave.style.left = `${x}px`;
            wave.style.top = `${y}px`;

            this.appendChild(wave);
            setTimeout(() => wave.remove(), 1000);
        });
    });

    // Плавный скролл в списке чатов
    const chatList = document.querySelector('.chat-list');
    chatList.addEventListener('scroll', function() {
        const scrollTop = this.scrollTop;
        const header = document.querySelector('.sidebar-header');
        header.style.boxShadow = scrollTop > 10 ? '0 2px 10px rgba(0,0,0,0.05)' : 'none';
    });
});




    // Плавная прокрутка вниз
const container = document.getElementById('messageContainer');
container.scrollTo({
    top: container.scrollHeight,
    behavior: 'smooth'
});

// Автоматическое увеличение высоты textarea
const textarea = document.querySelector('textarea');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Эффект при фокусе на поле ввода
textarea.addEventListener('focus', function() {
    this.parentElement.style.backgroundColor = '#e6f4f1';
});

textarea.addEventListener('blur', function() {
    this.parentElement.style.backgroundColor = '#f0f2f5';
});

// Анимация отправки сообщения
const messageForm = document.querySelector('.message-form');
messageForm.addEventListener('submit', function(e) {
    const btn = this.querySelector('.btn-send');
    btn.style.transform = 'scale(0.9)';
    setTimeout(() => {
        btn.style.transform = 'scale(1)';
    }, 200);
});

// Фиксация поля ввода при прокрутке
window.addEventListener('scroll', function() {
    const form = document.querySelector('.message-form');
    if (window.scrollY > 100) {
        form.style.boxShadow = '0 -2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        form.style.boxShadow = 'none';
    }
});

// Анимация печатания (пример реализации)
function showTypingIndicator() {
    const status = document.getElementById('typingStatus');
    status.style.display = 'block';
    setTimeout(() => {
        status.style.display = 'none';
    }, 2000);
}

// Слушатель для демонстрации (можно удалить в реальном приложении)
document.querySelector('textarea').addEventListener('input', function() {
    if (this.value.length > 0) {
        showTypingIndicator();
    }
});

// Плавный скролл при новых сообщениях
function scrollToBottom() {
    const container = document.getElementById('messageContainer');
    container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
    });
}

// Вызывайте эту функцию при добавлении нового сообщения
scrollToBottom();

// Альтернативный вариант с "пружинной" анимацией
function springScroll() {
    const container = document.getElementById('messageContainer');
    const start = container.scrollTop;
    const end = container.scrollHeight - container.clientHeight;
    const duration = 500;
    let startTime = null;

    function animate(currentTime) {
        if (!startTime) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);

        // "Пружинная" функция easing
        const easing = 1 - Math.pow(1 - progress, 3);
        container.scrollTop = start + (end - start) * easing;

        if (timeElapsed < duration) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
}



