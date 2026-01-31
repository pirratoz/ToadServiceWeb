const btn = document.getElementById('activateBtn');
const input = document.getElementById('activationCode');
const box = document.getElementById('resultBox');

btn.addEventListener('click', sendCode);

// Enter = отправить
input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendCode();
});

async function sendCode() {
    const code = input.value.trim();

    if (code.length !== 16) {
        setBox("Код должен содержать 16 символов", "warning");
        return;
    }

    btn.disabled = true;
    btn.innerText = "⏳ Проверка...";
    setBox("Отправляем код...", "info");

    try {
        const response = await fetch("/ajax/code/input", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Ошибка сервера");
        }

        /*
            ожидается ответ:
            {
                success: true/false,
                message: "...",
                message_type: "success|error|warning|info"
            }
        */

        setBox(
            data.message || "Ответ получен",
            data.message_type || (data.success ? "success" : "error")
        );

        if (data.success) {
            input.value = "";
        }

    } catch (err) {
        console.error(err);
        setBox(err.message || "Ошибка запроса", "error");
    } finally {
        btn.disabled = false;
        btn.innerText = "▶ Активировать";
    }
}

function setBox(text, type) {
    box.className = "result-box " + type;
    box.innerText = text;
}
