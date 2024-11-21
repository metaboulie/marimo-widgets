export default {
    render({ model, el }) {
        const renderWidget = () => {
            el.innerHTML = "";

            const container = document.createElement("div");
            container.className = "color-matrix-container";

            const gridContainer = document.createElement("div");
            gridContainer.className = "grid-container";

            const rowLabelContainer = document.createElement("div");
            rowLabelContainer.className = "row-labels";
            rowLabelContainer.style.gap = `${model.get("grid_gap")}px`;

            model.get("row_labels").forEach((label) => {
                const labelDiv = document.createElement("div");
                labelDiv.className = "label row-label";
                labelDiv.textContent = label;
                labelDiv.style.height = `${model.get("cell_height")}px`;
                labelDiv.style.lineHeight = `${model.get("cell_height")}px`;
                labelDiv.style.fontSize = `${model.get("font_size")}px`;
                rowLabelContainer.appendChild(labelDiv);
            });

            const grid = document.createElement("div");
            grid.className = "color-grid";
            grid.style.gap = `${model.get("grid_gap")}px`;

            const numCols = model.get("colors")[0].length;
            grid.style.gridTemplateColumns = `repeat(${numCols}, ${model.get(
                "cell_width"
            )}px)`;

            model.get("colors").forEach((row, i) => {
                row.forEach((color, j) => {
                    const cell = document.createElement("div");
                    cell.className = "color-cell";
                    cell.style.width = `${model.get("cell_width")}px`;
                    cell.style.height = `${model.get("cell_height")}px`;
                    cell.style.backgroundColor = color;

                    // Check if cell is selected
                    const isSelected = model
                        .get("selected_cells")
                        .some(([r, c]) => r === i && c === j);
                    if (isSelected) {
                        cell.classList.add("selected");
                    }

                    // Add click handler for selection
                    cell.addEventListener("click", () => {
                        const selected_cells = model.get("selected_cells");
                        const cellIndex = selected_cells.findIndex(
                            ([r, c]) => r === i && c === j
                        );

                        if (cellIndex === -1) {
                            // Add cell to selection
                            model.set("selected_cells", [
                                ...selected_cells,
                                [i, j, color],
                            ]);
                        } else {
                            // Remove cell from selection
                            model.set("selected_cells", [
                                ...selected_cells.slice(0, cellIndex),
                                ...selected_cells.slice(cellIndex + 1),
                            ]);
                        }
                        model.save_changes();
                    });

                    const tooltip = document.createElement("div");
                    tooltip.className = "tooltip";
                    tooltip.textContent = model.get("tooltips")[i][j];
                    tooltip.style.fontSize = `${model.get("font_size")}px`;
                    cell.appendChild(tooltip);

                    grid.appendChild(cell);
                });
            });

            gridContainer.appendChild(rowLabelContainer);
            gridContainer.appendChild(grid);
            container.appendChild(gridContainer);
            el.appendChild(container);
        };

        renderWidget();

        const properties = [
            "colors",
            "tooltips",
            "row_labels",
            "cell_width",
            "cell_height",
            "grid_gap",
            "font_size",
            "selected_cells",
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
    },
};
