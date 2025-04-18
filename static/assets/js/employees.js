document.addEventListener('DOMContentLoaded', function() {
    // Поиск сотрудников
    const searchInput = document.querySelector('.search-box input');
    const employeeCards = document.querySelectorAll('.employee-card');

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();

        employeeCards.forEach(card => {
            const name = card.querySelector('h3').textContent.toLowerCase();
            const position = card.querySelector('.position').textContent.toLowerCase();
            const department = card.querySelector('.department').textContent.toLowerCase();
            const skills = card.querySelector('.card-skills').textContent.toLowerCase();

            if (name.includes(searchTerm) ||
                position.includes(searchTerm) ||
                department.includes(searchTerm) ||
                skills.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });


document.getElementById('departmentFilter').addEventListener('change', function() {
    const deptId = this.value;

    fetch(`?department=${deptId}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка сети');
        return response.json();
    })
    .then(data => {
        document.querySelector('.employees-grid').innerHTML = data.html;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при фильтрации');
    });
});


    // Анимация при наведении
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

