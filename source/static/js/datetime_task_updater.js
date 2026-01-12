document.querySelectorAll('.apply-next-run-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const taskType = button.dataset.taskType;
        const input = button.previousElementSibling; // input datetime-local
        const newDatetime = input.value; // формат YYYY-MM-DDTHH:MM:SS

        try {
            const response = await fetch('/ajax/set/next_run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: taskType,
                    next_run: newDatetime
                })
            });

            if (response.ok) {
                const result = await response.json();

                // Находим блок "Следующий запуск" для этой задачи
                const taskRow = button.closest('.task-row');
                const nextRunDiv = taskRow.querySelector('.next-run-text');

                // Преобразуем дату в формат HH:MM DD.MM.YYYY
                const dt = new Date(newDatetime);
                const formatted = dt.toLocaleString('ru-RU', {
                    hour: '2-digit',
                    minute: '2-digit',
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                });

                nextRunDiv.textContent = `⏱ Следующий запуск: ${formatted}`;
            } else {
                console.error('Ошибка обновления даты');
            }
        } catch (err) {
            console.error(err);
        }
    });
});