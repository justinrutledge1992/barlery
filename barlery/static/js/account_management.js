/**
 * Account Management JavaScript
 * Handles user account deactivation and activation
 */

document.addEventListener("DOMContentLoaded", () => {
  console.log("Account Management loaded");

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  /* ---------------------------
     Activate / Deactivate logic
  ---------------------------- */
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.dataset.action;
    if (!["activate", "deactivate"].includes(action)) return;

    const card = btn.closest("[data-user-id]");
    const userId = card?.dataset.userId;

    const first = btn.dataset.userFirstName || "";
    const last = btn.dataset.userLastName || "";
    const fullName = `${first} ${last}`.trim() || "this user";

    const url = btn.dataset.url;
    if (!url || !userId) {
      alert("Error: could not determine which user to update.");
      return;
    }

    const confirmMessage =
      action === "deactivate"
        ? `Deactivate account for ${fullName}?\n\nThey will immediately lose access and will not be able to log in.`
        : `Are you sure you want to activate the account for ${fullName}?`;

    if (!confirm(confirmMessage)) return;

    btn.disabled = true;
    btn.innerHTML =
      action === "deactivate"
        ? '<i class="fas fa-spinner fa-spin"></i> Deactivating...'
        : '<i class="fas fa-spinner fa-spin"></i> Activating...';

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ user_id: userId }),
      });

      const data = await resp.json().catch(() => ({}));

      if (!resp.ok || !data.success) {
        alert(data.error || `Request failed (${resp.status})`);
        window.location.reload();
        return;
      }

      // ✅ Always refresh page after success
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Network error. Please try again.");
      window.location.reload();
    }
  });

  /* ---------------------------
     Toggle Deactivated Users
  ---------------------------- */
  const toggleBtn = document.getElementById("toggle-deactivated-users");
  const deactivatedSection = document.getElementById("deactivated-users-section");

  if (toggleBtn && deactivatedSection) {
    toggleBtn.addEventListener("click", () => {
      const isCollapsed = deactivatedSection.classList.toggle("is-collapsed");
      toggleBtn.textContent = isCollapsed
        ? "See Deactivated Users"
        : "Hide Deactivated Users";

      if (!isCollapsed) {
        deactivatedSection.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  }
});
