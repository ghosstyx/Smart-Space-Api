    // Автоматическая прокрутка вниз
    const container = document.getElementById('messageContainer');
    container.scrollTop = container.scrollHeight;

    // Автоматическое увеличение высоты textarea
    const textarea = document.querySelector('textarea');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });