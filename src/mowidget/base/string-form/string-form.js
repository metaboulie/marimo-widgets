function render({ model, el }) {
    const createRow = (key = "", value = "") => {
        const row = document.createElement("div");
        row.className = "form-row";
        row.style.opacity = "0";
        row.style.transform = "translateY(10px)";

        const keyInput = document.createElement("input");
        keyInput.type = "text";
        keyInput.value = key;
        keyInput.placeholder = "Key";
        keyInput.className = "key-input";

        const valueInput = document.createElement("input");
        valueInput.type = "text";
        valueInput.value = value;
        valueInput.placeholder = "Value";
        valueInput.className = "value-input";

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "×";
        deleteBtn.className = "delete-btn";
        deleteBtn.onclick = () => row.remove();

        row.appendChild(keyInput);
        row.appendChild(valueInput);
        row.appendChild(deleteBtn);

        // Add animation
        setTimeout(() => {
            row.style.transition = "all 0.3s ease";
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, 50);

        return row;
    };

    const renderWidget = () => {
        el.innerHTML = "";
        const container = document.createElement("div");
        container.className = "form-container";

        const formArea = document.createElement("div");
        formArea.className = "form-area";

        // Add initial rows based on default keys
        const defaultKeys = model.get("default_keys");
        const formData = model.get("form_data");
        defaultKeys.forEach((key) => {
            formArea.appendChild(createRow(key, formData[key] || ""));
        });

        const addButton = document.createElement("button");
        addButton.innerHTML = "<span>Add Field</span>";
        addButton.className = "add-btn";
        addButton.onclick = () => formArea.appendChild(createRow());

        const submitButton = document.createElement("button");
        submitButton.innerHTML = "<span>Save Changes</span>";
        submitButton.className = "submit-btn";
        submitButton.onclick = () => {
            const newFormData = {};
            formArea.querySelectorAll(".form-row").forEach((row) => {
                const key = row.querySelector(".key-input").value.trim();
                const value = row.querySelector(".value-input").value.trim();
                if (key) {
                    newFormData[key] = value;
                }
            });
            model.set("form_data", newFormData);
            model.save_changes();
        };

        container.appendChild(formArea);
        container.appendChild(addButton);
        container.appendChild(submitButton);
        el.appendChild(container);
    };

    renderWidget();

    const handlers = ["default_keys"].map((prop) => {
        const handler = () => renderWidget();
        model.on(`change:${prop}`, handler);
        return { prop, handler };
    });

    return () => {
        handlers.forEach(({ prop, handler }) => {
            model.off(`change:${prop}`, handler);
        });
        el.innerHTML = "";
    };
}

export default { render };
