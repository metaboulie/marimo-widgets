function render({ model, el }) {
    const renderWidget = () => {
        el.innerHTML = "";

        const container = document.createElement("div");
        container.className = "array-viewer-container";

        const gridContainer = document.createElement("div");
        gridContainer.className = "grid-container";

        // Row labels
        const rowLabelContainer = document.createElement("div");
        rowLabelContainer.className = "row-labels";
        rowLabelContainer.style.gap = `${model.get("grid_gap")}px`;

        model.get("row_labels").forEach((label) => {
            const labelDiv = document.createElement("div");
            labelDiv.className = "label row-label";
            labelDiv.textContent = label;
            labelDiv.style.height = `${model.get("cell_size")}px`;
            labelDiv.style.lineHeight = `${model.get("cell_size")}px`;
            labelDiv.style.fontSize = `${model.get("font_size")}px`;
            rowLabelContainer.appendChild(labelDiv);
        });

        // Grid
        const grid = document.createElement("div");
        grid.className = "array-grid";
        grid.style.gap = `${model.get("grid_gap")}px`;

        const numCols = model.get("colors")[0].length;
        grid.style.gridTemplateColumns = `repeat(${numCols}, ${model.get(
            "cell_size"
        )}px)`;

        model.get("colors").forEach((row, i) => {
            row.forEach((color, j) => {
                const cell = document.createElement("div");
                cell.className = "array-cell";
                cell.style.width = `${model.get("cell_size")}px`;
                cell.style.height = `${model.get("cell_size")}px`;
                cell.style.backgroundColor = color;
                cell.style.fontSize = `${model.get("font_size")}px`;

                // Add marker if present
                const marker = model.get("markers")[i][j];
                if (marker) {
                    const markerSpan = document.createElement("span");
                    markerSpan.className = "cell-marker";

                    // Add specific classes for different marker types
                    if (marker === "+") {
                        markerSpan.className += " outlier-high";
                        markerSpan.textContent = "+"; // Simple plus for high outliers
                    } else if (marker === "-") {
                        markerSpan.className += " outlier-low";
                        markerSpan.textContent = "−"; // Using proper minus sign for low outliers
                    } else if (marker === "∞" || marker === "N") {
                        markerSpan.className += " special-value";
                        markerSpan.textContent = marker === "∞" ? "∞" : "n"; // Lowercase n for NaN
                    }

                    cell.appendChild(markerSpan);
                }

                // Selection handling
                const isSelected = model
                    .get("selected_cells")
                    .some(([r, c]) => r === i && c === j);
                if (isSelected) {
                    cell.classList.add("selected");
                }

                cell.addEventListener("click", () => {
                    const selected_cells = model.get("selected_cells");
                    const cellIndex = selected_cells.findIndex(
                        ([r, c]) => r === i && c === j
                    );

                    if (cellIndex === -1) {
                        model.set("selected_cells", [
                            ...selected_cells,
                            [i, j, model.get("data")[i][j]],
                        ]);
                    } else {
                        model.set("selected_cells", [
                            ...selected_cells.slice(0, cellIndex),
                            ...selected_cells.slice(cellIndex + 1),
                        ]);
                    }
                    model.save_changes();
                });

                // Tooltip
                const tooltip = document.createElement("div");
                tooltip.className = "tooltip";
                tooltip.textContent = model.get("tooltips")[i][j];
                tooltip.style.fontSize = `${model.get("font_size")}px`;
                cell.appendChild(tooltip);

                grid.appendChild(cell);
            });
        });

        // Assemble the widget
        const mainContent = document.createElement("div");
        mainContent.className = "main-content";
        mainContent.appendChild(rowLabelContainer);
        mainContent.appendChild(grid);

        container.appendChild(mainContent);
        el.appendChild(container);
    };

    renderWidget();

    // Watch for property changes
    const properties = [
        "data",
        "colors",
        "markers",
        "tooltips",
        "color_mode",
        "row_labels",
        "selected_cells",
        "cell_size",
        "grid_gap",
        "font_size",
    ];

    const handlers = properties.map((prop) => {
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
