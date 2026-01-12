document.querySelectorAll('.next-run-input').forEach(input => {
    const preview = input.closest('div').nextElementSibling; // блок предпросмотра

    const updatePreview = () => {
        const dt = new Date(input.value);
        const day = String(dt.getDate()).padStart(2,'0');
        const month = String(dt.getMonth()+1).padStart(2,'0');
        const year = String(dt.getFullYear()).slice(2);
        const hours = String(dt.getHours()).padStart(2,'0');
        const minutes = String(dt.getMinutes()).padStart(2,'0');
        const seconds = String(dt.getSeconds()).padStart(2,'0');

        preview.textContent = `⏱ Предпросмотр: ${day}.${month}.${year}, ${hours}:${minutes}:${seconds}`;
    };

    // обновляем при изменении input
    input.addEventListener('input', updatePreview);
});