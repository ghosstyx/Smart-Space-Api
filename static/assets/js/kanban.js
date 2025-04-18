document.addEventListener('DOMContentLoaded', function() {
    // Элементы модального окна
    const modal = document.getElementById('task-modal');
    const newTaskBtn = document.getElementById('new-task-btn');
    const closeModal = document.querySelector('.close-modal');
    const taskForm = document.getElementById('task-form');
    const modalTitle = document.getElementById('modal-title');

    // Функция для toast-уведомлений
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }, 100);
    }

    // Обработчик отправки формы
    taskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        formData.append('action', 'create_task');

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                document.getElementById('todo-tasks').insertAdjacentHTML('afterbegin', data.task_html);
                updateTaskCounts();
                taskForm.reset();
            } else {
                console.error(data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Успешно!');
        });
    });

    // Открытие модального окна для новой задачи
    newTaskBtn.addEventListener('click', function() {
        modalTitle.textContent = 'New Task';
        taskForm.reset();
        modal.style.display = 'block';
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Закрытие при клике вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Drag and Drop функционал
    const taskCards = document.querySelectorAll('.task-card');
    const taskLists = document.querySelectorAll('.tasks-list');

    let draggedTask = null;

    // Начало перетаскивания
    taskCards.forEach(task => {
        task.addEventListener('dragstart', function() {
            draggedTask = this;
            setTimeout(() => {
                this.classList.add('dragging');
            }, 0);
        });

        task.addEventListener('dragend', function() {
            this.classList.remove('dragging');
        });
    });

    // Перетаскивание над колонкой
    taskLists.forEach(list => {
        list.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
            const afterElement = getDragAfterElement(this, e.clientY);
            if (afterElement == null) {
                this.appendChild(draggedTask);
            } else {
                this.insertBefore(draggedTask, afterElement);
            }
        });

        list.addEventListener('dragleave', function() {
            this.classList.remove('drag-over');
        });

        list.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');

            const newStatus = this.parentElement.id.replace('-column', '');
            updateTaskStatus(draggedTask.dataset.taskId, newStatus);
        });
    });

    // Обработчик удаления задачи
    let taskToDelete = null;
    const confirmDeleteModal = document.getElementById('confirm-delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    // Обработчик клика по кнопке удаления
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-task-btn')) {
            taskToDelete = e.target.dataset.taskId;
            confirmDeleteModal.style.display = 'block';
        }
    });

    // Подтверждение удаления
    confirmDeleteBtn.addEventListener('click', function() {
        if (taskToDelete) {
            deleteTask(taskToDelete);
        }
        confirmDeleteModal.style.display = 'none';
    });

    // Отмена удаления
    cancelDeleteBtn.addEventListener('click', function() {
        confirmDeleteModal.style.display = 'none';
    });

    // Закрытие при клике вне модального окна
    confirmDeleteModal.addEventListener('click', function(e) {
        if (e.target === confirmDeleteModal) {
            confirmDeleteModal.style.display = 'none';
        }
    });

    // Функция для удаления задачи через AJAX
    function deleteTask(taskId) {
        const taskCard = document.querySelector(`.task-card[data-task-id="${taskId}"]`);
        taskCard.classList.add('deleting');
        setTimeout(() => {
            const csrfToken = getCookie('csrftoken');

            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
                body: `action=delete_task&task_id=${taskId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    taskCard.remove();
                    updateTaskCounts();
                    showToast('Задача успешно удалена');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }, 300);
    }

    // Вспомогательная функция для определения позиции
    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.task-card:not(.dragging)')];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    // Обновление статуса задачи через AJAX
    function updateTaskStatus(taskId, newStatus) {
        const csrfToken = getCookie('csrftoken');

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: `action=update_status&task_id=${taskId}&new_status=${newStatus}`
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Failed to update task status');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Обновление счетчиков задач
    function updateTaskCounts() {
        document.querySelectorAll('.kanban-column').forEach(column => {
            const count = column.querySelector('.tasks-list').children.length;
            column.querySelector('.task-count').textContent = count;
        });
    }

    // Вспомогательная функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});