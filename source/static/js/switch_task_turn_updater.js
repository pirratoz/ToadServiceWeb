document.querySelectorAll('.toggle-task-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const taskType = button.dataset.taskType;
        const newState = !button.classList.contains('btn-turn-on'); // инвертируем состояние

        try {
            const response = await fetch("/ajax/set/turn", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    field: taskType,
                    value: newState
                })
            });

            if (response.ok) {
                // Обновляем визуально кнопку
                button.classList.toggle("btn-turn-on", newState);
                button.classList.toggle("btn-turn-off", !newState);

                const icon = button.querySelector("i");
                if (newState) {
                    icon.classList.remove("bi-x-lg");
                    icon.classList.add("bi-check-lg");
                } else {
                    icon.classList.remove("bi-check-lg");
                    icon.classList.add("bi-x-lg");
                }

                // Обновляем tooltip
                button.title = newState ? "Включено" : "Выключено";
            } else {
                const data = await response.json();
                console.error("Ошибка обновления:", data.message || response.statusText);
            }
        } catch (err) {
            console.error("Ошибка AJAX:", err);
        }
    });
});