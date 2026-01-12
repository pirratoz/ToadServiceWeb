document.getElementById('applyTelegramBtn').addEventListener('click', async () => {

    const inputs = document.querySelectorAll('.telegram-input');
    const payload = {};
    let hasValue = false;

    inputs.forEach(input => {
        const key = input.dataset.field;
        const value = input.value.trim();

        if (value !== '') {
            hasValue = true;
            payload[key] = value;
        } else {
            payload[key] = null;
        }
    });

    if (!hasValue) {
        alert('Заполните хотя бы одно поле');
        return;
    }

    try {
        const response = await fetch('/ajax/set/telegram', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Ошибка запроса');
        }

        const data = await response.json();
        const user = data.info; // 👈 твой return

        // 🔄 Обновляем карточку Telegram
        document.getElementById('tg-api-id').textContent =
            user.api_id ?? 'Не задано';

        document.getElementById('tg-api-hash').textContent =
            user.api_hash ?? 'Не задано';

        document.getElementById('tg-phone').textContent =
            user.phone ?? 'Не задан';

        document.getElementById('tg-2fa').textContent =
            user.password_2fa ?? 'Не установлен';

        // 🧹 очищаем инпуты
        inputs.forEach(i => i.value = '');

    } catch (err) {
        console.error(err);
        alert('Ошибка при обновлении Telegram данных');
    }
});