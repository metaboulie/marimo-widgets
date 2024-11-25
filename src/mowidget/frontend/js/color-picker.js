export default {
    render({ model, el }) {
        const renderWidget = () => {
            el.innerHTML = `
                <div class="color-picker-container">
                    <div class="picker-section">
                        <canvas class="color-canvas" width="300" height="200"></canvas>
                        <div class="selected-color-preview" style="background-color: ${model.get(
                            "selected_color"
                        )}"></div>
                    </div>
                </div>
            `;

            const canvas = el.querySelector(".color-canvas");
            const ctx = canvas.getContext("2d");
            let isMouseDown = false;

            function drawColorPicker() {
                // Draw main color gradient
                const colorGradient = ctx.createLinearGradient(
                    0,
                    0,
                    canvas.width,
                    0
                );
                colorGradient.addColorStop(0, "rgb(255, 0, 0)");
                colorGradient.addColorStop(0.17, "rgb(255, 0, 255)");
                colorGradient.addColorStop(0.33, "rgb(0, 0, 255)");
                colorGradient.addColorStop(0.5, "rgb(0, 255, 255)");
                colorGradient.addColorStop(0.67, "rgb(0, 255, 0)");
                colorGradient.addColorStop(0.83, "rgb(255, 255, 0)");
                colorGradient.addColorStop(1, "rgb(255, 0, 0)");

                ctx.fillStyle = colorGradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Draw brightness/darkness gradient
                const valueGradient = ctx.createLinearGradient(
                    0,
                    0,
                    0,
                    canvas.height
                );
                valueGradient.addColorStop(0, "rgba(255, 255, 255, 1)");
                valueGradient.addColorStop(0.5, "rgba(255, 255, 255, 0)");
                valueGradient.addColorStop(0.5, "rgba(0, 0, 0, 0)");
                valueGradient.addColorStop(1, "rgba(0, 0, 0, 1)");

                ctx.fillStyle = valueGradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            function updateColor(e) {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                if (
                    x >= 0 &&
                    x <= canvas.width &&
                    y >= 0 &&
                    y <= canvas.height
                ) {
                    const imageData = ctx.getImageData(x, y, 1, 1).data;
                    const color = `#${[...imageData]
                        .slice(0, 3)
                        .map((x) => x.toString(16).padStart(2, "0"))
                        .join("")}`;

                    model.set("selected_color", color);
                    model.save_changes();
                    el.querySelector(
                        ".selected-color-preview"
                    ).style.backgroundColor = color;
                }
            }

            // Draw initial color picker
            drawColorPicker();

            // Mouse event handlers
            canvas.addEventListener("mousedown", (e) => {
                isMouseDown = true;
                updateColor(e);
            });

            canvas.addEventListener("mousemove", (e) => {
                if (isMouseDown) {
                    updateColor(e);
                }
            });

            canvas.addEventListener("mouseup", () => {
                isMouseDown = false;
            });

            canvas.addEventListener("mouseleave", () => {
                isMouseDown = false;
            });

            // Touch event handlers
            canvas.addEventListener("touchstart", (e) => {
                e.preventDefault();
                updateColor(e.touches[0]);
            });

            canvas.addEventListener("touchmove", (e) => {
                e.preventDefault();
                updateColor(e.touches[0]);
            });
        };

        // Initial render
        renderWidget();

        // Cleanup
        return () => {
            el.innerHTML = "";
        };
    },
};
