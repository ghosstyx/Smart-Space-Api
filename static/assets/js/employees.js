document.addEventListener('DOMContentLoaded', function() {
    // Поиск сотрудников
    const searchInput = document.querySelector('.search-box input');
    const employeeCards = document.querySelectorAll('.employee-card');
    const loadingIndicator = document.querySelector('.search-loading')
    console.log(document.querySelectorAll('.employee-card'));
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        loadingIndicator.style.display = 'block';
        searchTimeout = setTimeout(() => {
            const searchTerm = this.value.toLowerCase();

            employeeCards.forEach(card => {
                const name = card.querySelector('h3').textContent.toLowerCase();
                const position = card.querySelector('.position').textContent.toLowerCase();
                const department = card.querySelector('.department').textContent.toLowerCase();

                if (name.includes(searchTerm) ||
                    position.includes(searchTerm) ||
                    department.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
            loadingIndicator.style.display = 'none';
            }, 300);
    });
    // function searchWithAjax(term) {
    //     loadingIndicator.style.display = 'block';
    //
    //     fetch(`/user/employees/?search=${term}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             document.getElementById('employeesResults').innerHTML = data.html;
    //         })
    //         .finally(() => {
    //             loadingIndicator.style.display = 'none';
    //         });
    // }

    document.getElementById('departmentFilter').addEventListener('change', function() {
        const deptId = this.value;
        const currentUrl = new URL(window.location.href);

        const params = new URLSearchParams(currentUrl.search);
        params.set('department', deptId);  // Обновляем только department

        fetch(`?${params.toString()}`, {  // Передаем все параметры
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сети');
            return response.json();
        })
        .then(data => {
            document.getElementById('employeesResults').innerHTML = data.html;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при фильтрации');
        });
    });

    // Анимация карточек
    employeeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 12px 28px rgba(26, 115, 232, 0.2)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '0 6px 20px rgba(26, 115, 232, 0.15)';
        });
    });
});