document.addEventListener("DOMContentLoaded", () => {
    console.log("[time_choice] running");

    // Start time options (2 PM to 11 PM)
    const START_MIN = 14;
    const START_MAX = 23;

    // Allow end times after midnight up to 12 AM (can be extended)
    // 0 == midnight; 1 == 1am, 2 == 2am, etc.
    const END_AFTER_MIDNIGHT_MAX = 0;

    const fieldIds = ["id_start_time", "id_end_time"];

    function toHHMM(h) {
        return `${String(h).padStart(2, "0")}:00`;
    }

    function toAmPm(hhmm) {
        let [h, m] = hhmm.split(":").map(Number);
        const period = h >= 12 ? "PM" : "AM";
        h = h % 12;
        if (h === 0) h = 12;
        return `${h}:${String(m).padStart(2, "0")} ${period}`;
    }

    function rangeInclusive(a, b) {
        const out = [];
        for (let i = a; i <= b; i++) out.push(i);
        return out;
    }

    fieldIds.forEach((id) => {
        const input = document.getElementById(id);
        console.log(`[time_choice] found ${id}?`, !!input);
        if (!input) return;

        // If we already inserted a select (hot reload / back button), don't duplicate
        if (document.getElementById(id + "_select")) return;

        // Hide the real input but keep it as the submitted field
        input.style.display = "none";

        // Build the visible select
        const select = document.createElement("select");
        select.id = id + "_select";

        const hours =
        id === "id_start_time"
            ? rangeInclusive(START_MIN, START_MAX)
            : [
                ...rangeInclusive(START_MIN, START_MAX),  // same-day
                ...rangeInclusive(0, END_AFTER_MIDNIGHT_MAX), // after-midnight
            ];

        hours.forEach((h) => {
        const value = toHHMM(h);            // submitted value stays 24-hr
        const label = toAmPm(value);        // user sees AM/PM

        const opt = document.createElement("option");
        opt.value = value;
        opt.textContent = label;
        select.appendChild(opt);
        });

        // Initialize: if input has a value and it exists, select it; else default first option
        const initial = input.value;
        const hasInitial = Array.from(select.options).some((o) => o.value === initial);
        select.value = hasInitial ? initial : select.options[0].value;
        input.value = select.value;

        // Keep the real input synced
        select.addEventListener("change", () => {
        input.value = select.value;
        });

        // Insert select after the (now hidden) input
        input.insertAdjacentElement("afterend", select);

        // Update the label to point at the new select for accessibility
        const labelEl = document.querySelector(`label[for="${id}"]`);
        if (labelEl) labelEl.setAttribute("for", select.id);
    });
});
