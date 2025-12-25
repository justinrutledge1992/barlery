document.addEventListener("DOMContentLoaded", () => {
    console.log("[event_time_choice] running");

    // Time range: 2:00 PM (14:00) to 12:00 AM (00:00)
    const START_MIN_HOUR = 14; // 2:00 PM
    const END_MAX_HOUR = 0;    // 12:00 AM (midnight)
    
    const DEFAULT_START_TIME = "16:00"; // 4:00 PM

    const startTimeId = "id_start_time";
    const endTimeId = "id_end_time";

    function toHHMM(h, m) {
        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
    }

    function toAmPm(hhmm) {
        let [h, m] = hhmm.split(":").map(Number);
        const period = h >= 12 ? "PM" : "AM";
        h = h % 12;
        if (h === 0) h = 12;
        return `${h}:${String(m).padStart(2, "0")} ${period}`;
    }

    // Generate time options from 2:00 PM to 11:45 PM, plus 12:00 AM
    function generateTimeOptions() {
        const options = [];
        
        // 2:00 PM (14:00) to 11:45 PM (23:45)
        for (let h = START_MIN_HOUR; h < 24; h++) {
            for (let m = 0; m < 60; m += 15) {
                options.push(toHHMM(h, m));
            }
        }
        
        // Add midnight (12:00 AM)
        options.push(toHHMM(0, 0));
        
        return options;
    }

    const timeOptions = generateTimeOptions();

    // Build the start time select
    const startInput = document.getElementById(startTimeId);
    if (startInput) {
        // Check if already processed
        if (document.getElementById(startTimeId + "_select")) {
            console.log("[event_time_choice] start time already processed");
        } else {
            startInput.style.display = "none";

            const startSelect = document.createElement("select");
            startSelect.id = startTimeId + "_select";

            timeOptions.forEach((value) => {
                const label = toAmPm(value);
                const opt = document.createElement("option");
                opt.value = value;
                opt.textContent = label;
                startSelect.appendChild(opt);
            });

            // Set default or existing value
            const initialStart = startInput.value;
            if (initialStart && timeOptions.includes(initialStart)) {
                startSelect.value = initialStart;
            } else {
                startSelect.value = DEFAULT_START_TIME;
            }
            startInput.value = startSelect.value;

            // Keep the real input synced
            startSelect.addEventListener("change", () => {
                startInput.value = startSelect.value;
                updateEndTimeOptions();
            });

            startInput.insertAdjacentElement("afterend", startSelect);

            const startLabel = document.querySelector(`label[for="${startTimeId}"]`);
            if (startLabel) startLabel.setAttribute("for", startSelect.id);
        }
    }

    // Build the end time select
    const endInput = document.getElementById(endTimeId);
    let endSelect;
    
    if (endInput) {
        // Check if already processed
        if (document.getElementById(endTimeId + "_select")) {
            console.log("[event_time_choice] end time already processed");
            endSelect = document.getElementById(endTimeId + "_select");
        } else {
            endInput.style.display = "none";

            endSelect = document.createElement("select");
            endSelect.id = endTimeId + "_select";

            // Add empty option for "no end time"
            const emptyOpt = document.createElement("option");
            emptyOpt.value = "";
            emptyOpt.textContent = "--- N/A ---";
            endSelect.appendChild(emptyOpt);

            // Initial population (will be filtered after start time is set)
            timeOptions.forEach((value) => {
                const label = toAmPm(value);
                const opt = document.createElement("option");
                opt.value = value;
                opt.textContent = label;
                endSelect.appendChild(opt);
            });

            // Set initial value
            const initialEnd = endInput.value;
            if (initialEnd && timeOptions.includes(initialEnd)) {
                endSelect.value = initialEnd;
            } else {
                endSelect.value = "";
            }
            endInput.value = endSelect.value;

            // Keep the real input synced
            endSelect.addEventListener("change", () => {
                endInput.value = endSelect.value;
            });

            endInput.insertAdjacentElement("afterend", endSelect);

            const endLabel = document.querySelector(`label[for="${endTimeId}"]`);
            if (endLabel) endLabel.setAttribute("for", endSelect.id);
        }
    }

    // Function to update end time options based on start time
    function updateEndTimeOptions() {
        const startSelect = document.getElementById(startTimeId + "_select");
        const endSelect = document.getElementById(endTimeId + "_select");
        
        if (!startSelect || !endSelect) return;

        const startTime = startSelect.value;
        const currentEndValue = endSelect.value;

        // Clear all options except the empty one
        endSelect.innerHTML = "";
        
        // Re-add empty option
        const emptyOpt = document.createElement("option");
        emptyOpt.value = "";
        emptyOpt.textContent = "--- N/A ---";
        endSelect.appendChild(emptyOpt);

        // Filter valid end times (must be after start time)
        // Midnight (00:00) is always valid as it's considered "next day"
        timeOptions.forEach((value) => {
            const isValid = isValidEndTime(startTime, value);
            
            if (isValid) {
                const label = toAmPm(value);
                const opt = document.createElement("option");
                opt.value = value;
                opt.textContent = label;
                endSelect.appendChild(opt);
            }
        });

        // Try to restore previous selection if still valid
        if (currentEndValue && Array.from(endSelect.options).some(o => o.value === currentEndValue)) {
            endSelect.value = currentEndValue;
        } else {
            endSelect.value = "";
        }
        
        endInput.value = endSelect.value;
    }

    // Check if end time is valid (after start time)
    // Midnight (00:00) is treated as next day, so always valid
    function isValidEndTime(startTime, endTime) {
        if (endTime === "00:00") {
            // Midnight is always valid (next day)
            return true;
        }

        const [startH, startM] = startTime.split(":").map(Number);
        const [endH, endM] = endTime.split(":").map(Number);

        // Convert to minutes since start of range (14:00)
        const startMinutes = startH * 60 + startM;
        const endMinutes = endH * 60 + endM;

        return endMinutes > startMinutes;
    }

    // Initial filter of end time options
    updateEndTimeOptions();
});