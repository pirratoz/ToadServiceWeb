document.querySelectorAll(".work-type-select").forEach(select => {
    select.addEventListener("change", async () => {
        const workType = select.value;

        try {
            const response = await fetch("/ajax/set/work", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    type: workType
                })
            });

            if (!response.ok) {
                console.error("Ошибка сохранения типа работы");
            }
        } catch (e) {
            console.error("AJAX error:", e);
        }
    });
});