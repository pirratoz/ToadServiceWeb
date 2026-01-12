document.querySelectorAll(".toggle-user-btn").forEach(button => {
    button.addEventListener("click", async () => {
        const field = button.dataset.field;
        const newState = !button.classList.contains("btn-success"); // инвертируем

        try {
            const response = await fetch("/ajax/set/turn", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    field: field,
                    value: newState
                })
            });

            if (response.ok) {
                // меняем стиль кнопки и текст
                button.classList.toggle("btn-success", newState);
                button.classList.toggle("btn-secondary", !newState);
                button.textContent = newState ? "Включено" : "Выключено";
            } else {
                console.error("Ошибка обновления поля");
            }
        } catch (err) {
            console.error(err);
        }
    });
});