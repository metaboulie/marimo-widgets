# blue = learned

## the pattern of implementing a widget

**python**

```python
import pathlib

import anywidget
import traitlets

class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "widget" / "widget.js"
    _css = pathlib.Path(__file__).parent / "widget" / "widget.css"

    # All traits must be properly typed and tagged
    trait_1 = traitlets.Type().tag(sync=True)
    trait_2 = traitlets.Type().tag(sync=True)

    def __init__(self, trait_1, trait_2):
        super().__init__()
        self.trait_1 = trait_1
        self.trait_2 = trait_2
```

**javascript**

```javascript
function render({ model, el }) {
    // define some helper functions
    const helperFunction = () => {
        // access the trait
        model.get("trait_1");

        // set the trait
        model.set("trait_1", "new value");
        // save the changes ( this is necessary to update the widget )
        model.save_changes();
    };

    // define the main function to render the widget
    const renderWidget = () => {
        el.innerHTML = "";
        ...
    };

    // initial render
    renderWidget();

    // add event listeners for input parameters
    const properties = [
        "property_1",
        "property_2",
        "property_3",
        "property_4",
        "property_5",
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

// export the widget
export default { render };
```

**css**

```css
/* use light-dark to assign colors for both light and dark themes */
:root {
    --background: light-dark(#f0f4ff, #1a1b2e);
    --foreground: light-dark(#1a1b2e, #e2e4ff);
}

/* marimo doesn't support variables in css yet, so can't reuse the variables */
.widget-container {
    background: light-dark(#f0f4ff, #1a1b2e);
    color: light-dark(#1a1b2e, #e2e4ff);
}
```

## Controller for quick widget initialization

```python
@classmethod
def controller(cls: type["PomodoroTimer"]) -> mo.ui.dictionary:
    """Get the controller for the Pomodoro Timer."""
    return mo.ui.dictionary(
        {
            "work_duration": mo.ui.number(
                start=0.1, value=25.0, label="work duration"
            ),
            "short_break": mo.ui.number(
                start=0.1, value=5.0, label="short break"
            ),
            "long_break": mo.ui.number(
                start=0.1, value=15.0, label="long break"
            ),
            "sessions_before_long_break": mo.ui.number(
                start=1,
                step=1,
                value=4,
                label="sessions before long break",
            ),
            "num_cycles": mo.ui.number(
                start=1, step=1, value=3, label="number of cycles"
            ),
        }
    )
```
