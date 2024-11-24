function render({ model, el }) {
    // Stores the ID returned by setInterval, used to track and control the timer
    // When null, indicates the timer is not running
    // When set, contains the interval ID that can be used to stop the timer
    let timerInterval = null;

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, "0")}:${secs
            .toString()
            .padStart(2, "0")}`;
    };

    const toggleTimer = () => {
        if (model.get("_timer_state") !== "running") {
            model.set("_timer_state", "running");
            startTimer();
        } else {
            model.set("_timer_state", "paused");
            stopTimer();
        }
        renderWidget();
    };

    const startTimer = () => {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            let remaining = model.get("_remaining_seconds");
            if (remaining > 1) {
                model.set("_remaining_seconds", remaining - 1);
            } else {
                handleSessionComplete();
            }
            renderWidget();
        }, 1000);
    };

    const stopTimer = () => {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    };

    const skipSession = () => {
        stopTimer();
        handleSessionComplete();
    };

    const resetTimer = () => {
        stopTimer();
        model.set("_timer_state", "stopped");
        model.set("_remaining_seconds", model.get("_work_duration_seconds"));
        model.set("_is_break", false);
        model.set("_current_session", 0);
        model.set("_current_cycle", 1);
        renderWidget();
    };

    const handleSessionComplete = () => {
        stopTimer();

        if (model.get("_current_cycle") > model.get("num_cycles")) {
            model.set("_timer_state", "stopped");
            renderWidget();
            return;
        }

        if (!model.get("_is_break")) {
            const currentSession = model.get("_current_session") + 1;
            model.set("_current_session", currentSession);
            model.set("_is_break", true);

            // Check if it's time for a long break
            if (
                currentSession % model.get("sessions_before_long_break") ===
                0
            ) {
                model.set(
                    "_remaining_seconds",
                    model.get("_long_break_seconds")
                );
            } else {
                model.set(
                    "_remaining_seconds",
                    model.get("_short_break_seconds")
                );
            }
        } else {
            model.set("_is_break", false);
            model.set(
                "_remaining_seconds",
                model.get("_work_duration_seconds")
            );

            // If we just finished a long break, reset session counter
            if (
                model.get("_current_session") %
                    model.get("sessions_before_long_break") ===
                0
            ) {
                model.set("_current_session", 0);
                model.set("_current_cycle", model.get("_current_cycle") + 1);
            }
        }
        model.set("_timer_state", "stopped");
        renderWidget();
    };

    const renderWidget = () => {
        const isFinished =
            model.get("_current_cycle") > model.get("num_cycles");

        el.innerHTML = `
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <div class="pomodoro-container">
                    ${
                        isFinished
                            ? `<div class="timer-display">Finished!</div>
                         <div class="session-info">All cycles completed!</div>`
                            : `<div class="timer-display">${formatTime(
                                  model.get("_remaining_seconds")
                              )}</div>
                         <div class="session-info"> 
                            ${
                                model.get("_is_break")
                                    ? "Break Time"
                                    : "Work Session"
                            } 
                            ${model.get("_current_session")}/${model.get(
                                  "sessions_before_long_break"
                              )}
                            (Cycle ${model.get("_current_cycle")}/${model.get(
                                  "num_cycles"
                              )})
                         </div>`
                    }
                    <div class="controls">
                        ${
                            !isFinished
                                ? `<button class="control-btn" id="startBtn">
                                ${
                                    model.get("_timer_state") === "running"
                                        ? "Pause"
                                        : "Start"
                                }
                            </button>
                            <button class="control-btn" id="skipBtn">Skip</button>`
                                : ""
                        }
                        <button class="control-btn" id="resetBtn">Reset</button>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners only for buttons that exist
        if (!isFinished) {
            el.querySelector("#startBtn").addEventListener(
                "click",
                toggleTimer
            );
            el.querySelector("#skipBtn").addEventListener(
                "click",
                skipSession
            );
        }
        el.querySelector("#resetBtn").addEventListener(
            "click",
            onClickResetBtn
        );
    };

    const onClickResetBtn = () => {
        // Pause the timer if it's running
        if (model.get("_timer_state") === "running") {
            stopTimer();
            model.set("_timer_state", "paused");
            renderWidget();
        }

        // Create and show confirmation dialog
        const confirmed = window.confirm(
            "Are you sure you want to reset the timer?"
        );

        if (confirmed) {
            resetTimer();
        } else {
            renderWidget();
        }
    };

    // Initial render
    renderWidget();

    // Add event listeners for input parameters
    const properties = [
        "_work_duration_seconds",
        "_short_break_seconds",
        "_long_break_seconds",
        "sessions_before_long_break",
        "num_cycles",
    ];

    const handlers = properties.map((prop) => {
        const handler = () => {
            resetTimer();
            renderWidget();
        };
        model.on(`change:${prop}`, handler);
        return { prop, handler };
    });

    return () => {
        stopTimer();
        handlers.forEach(({ prop, handler }) => {
            model.off(`change:${prop}`, handler);
        });
        el.innerHTML = "";
    };
}

export default { render };
