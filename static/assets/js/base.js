    // Обработка кликов для раскрытия/закрытия подменю
        document.querySelectorAll('[data-toggle="collapse"]').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();

                const target = this.getAttribute('href');
                const targetElement = document.querySelector(target);
                const parentItem = this.closest('.nav-item');

                // Закрываем все открытые подменю, кроме текущего
                document.querySelectorAll('.collapse').forEach(collapse => {
                    if (collapse !== targetElement && collapse.classList.contains('show')) {
                        collapse.classList.remove('show');
                        collapse.closest('.nav-item').classList.remove('active');
                    }
                });

                // Переключаем текущее подменю
                targetElement.classList.toggle('show');
                parentItem.classList.toggle('active');
            });
        });
