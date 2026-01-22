document.getElementById('toggleBotBtn')?.addEventListener('click', async () => {
    const btn = document.getElementById('toggleBotBtn');
    const statusText = document.querySelector('.status-text');
    const statusDot = document.querySelector('.status-dot');
    const messageBox = document.querySelector('.bot-message');

    const url = '/ajax/bot/turn';

    // === UI: временное состояние ===
    btn.disabled = true;
    const prevText = btn.innerText;
    btn.innerText = '⏳ Обработка...';

    messageBox.className = 'bot-message info';
    messageBox.innerText = 'Отправляем команду боту...';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({}) // сервер сам решает что делать
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Ошибка сервера');
        }

        /*
            Сервер:
            {
                running: true|false,
                message: "текст",
                message_type: "success|error|warning|info"
            }
        */

        // === ЕДИНСТВЕННЫЙ ИСТОЧНИК ИСТИНЫ ===
        const running = Boolean(data.running);

        // статус
        statusText.innerText = running ? 'Работает' : 'Остановлен';
        statusDot.classList.toggle('online', running);
        statusDot.classList.toggle('offline', !running);

        // кнопка
        btn.classList.toggle('btn-start', !running);
        btn.classList.toggle('btn-stop', running);
        btn.innerText = running
            ? '⛔ Остановить бота'
            : '▶️ Запустить бота';

        // сообщение
        messageBox.className = `bot-message ${data.message_type || 'info'}`;
        messageBox.innerText = data.message || 'Статус обновлён';

    } catch (err) {
        console.error(err);

        btn.innerText = prevText;

        messageBox.className = 'bot-message error';
        messageBox.innerText = err.message || 'Не удалось выполнить действие';

    } finally {
        btn.disabled = false;
    }
});


document.getElementById('applyBotCodeBtn').addEventListener('click', async () => {
    const codeInput = document.getElementById('botCodeInput');
    const message = document.getElementById('botCodeMessage');
    const code = codeInput.value.trim();
    const payload = {};

    payload["code"] = code;

    message.textContent = '';
    message.className = 'bot-message';

    if (!code) {
        message.textContent = 'Введите код подтверждения';
        message.classList.add('error');
        return;
    }

    try {
        const response = await fetch('/ajax/bot/code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Ошибка при запуске бота');
        }

        if (data.running) {
            message.textContent = 'Бот успешно запущен';
            message.classList.add('success');
            codeInput.value = '';
        } else {
            message.textContent = data.message || 'Не удалось запустить бота';
            message.classList.add('error');
        }

    } catch (err) {
        console.error(err);
        message.textContent = err.message;
        message.classList.add('error');
    }
});
