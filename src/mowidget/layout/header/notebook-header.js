function escapeHTML(str) {
    return str.replace(
        /[&<>'"]/g,
        (tag) =>
            ({
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                "'": "&#39;",
                '"': "&quot;",
            }[tag] || tag)
    );
}

function stripHTML(html) {
    const tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

function renderValue(value) {
    if (typeof value !== "string") {
        return escapeHTML(String(value));
    }

    const isHTML = /<[a-z][\s\S]*>/i.test(value);
    const strippedValue = isHTML ? stripHTML(value) : value;

    if (strippedValue.length > 100) {
        if (isHTML) {
            return `
                <div class="preview">${value.substring(0, 100)}...</div>
                <div class="full-text" style="display: none;">${value}</div>
                <button class="toggle-button">Show More</button>
            `;
        } else {
            return `
                <div class="preview">${escapeHTML(
                    value.substring(0, 100)
                )}...</div>
                <div class="full-text" style="display: none;">${escapeHTML(
                    value
                )}</div>
                <button class="toggle-button">Show More</button>
            `;
        }
    }

    return isHTML ? value : escapeHTML(value);
}

function render({ model, el }) {
    const renderWidget = () => {
        el.innerHTML = "";

        const metadata = model.get("metadata");
        const banner = model.get("banner");
        const container = document.createElement("div");
        container.className = "header-container";

        container.innerHTML = `
            ${
                banner
                    ? `<img class="banner" src="${banner}" alt="Notebook Banner">`
                    : ""
            }
            <div class="form-container">
                ${Object.entries(metadata)
                    .map(
                        ([key, value]) => `
                    <div class="form-row">
                        <label>${escapeHTML(key)}</label>
                        <div class="value-container">
                            ${renderValue(value)}
                        </div>
                    </div>
                `
                    )
                    .join("")}
            </div>
        `;

        el.appendChild(container);

        container.querySelectorAll(".toggle-button").forEach((button) => {
            button.addEventListener("click", () => {
                const row = button.closest(".form-row");
                const preview = row.querySelector(".preview");
                const fullText = row.querySelector(".full-text");

                if (fullText.style.display === "none") {
                    fullText.style.display = "block";
                    preview.style.display = "none";
                    button.textContent = "Show Less";
                } else {
                    fullText.style.display = "none";
                    preview.style.display = "block";
                    button.textContent = "Show More";
                }
            });
        });
    };

    // Initial render
    renderWidget();

    // Create change handlers
    const handleMetadataChange = () => {
        renderWidget();
    };

    const handleBannerChange = () => {
        renderWidget();
    };

    // Add event listeners
    model.on("change:metadata", handleMetadataChange);
    model.on("change:banner", handleBannerChange);
}

export default { render };
