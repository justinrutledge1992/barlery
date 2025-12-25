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
     Copy Registration Link
  ---------------------------- */
  const copyLinkBtn = document.getElementById("copy-link-btn");
  const registrationLinkInput = document.getElementById("registration-link");

  if (copyLinkBtn && registrationLinkInput) {
    copyLinkBtn.addEventListener("click", async () => {
      try {
        // Select the text
        registrationLinkInput.select();
        registrationLinkInput.setSelectionRange(0, 99999); // For mobile devices

        // Copy to clipboard
        await navigator.clipboard.writeText(registrationLinkInput.value);

        // Visual feedback
        const originalHTML = copyLinkBtn.innerHTML;
        copyLinkBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyLinkBtn.classList.add("btn-success");

        // Reset after 2 seconds
        setTimeout(() => {
          copyLinkBtn.innerHTML = originalHTML;
          copyLinkBtn.classList.remove("btn-success");
        }, 2000);
      } catch (err) {
        console.error("Failed to copy:", err);
        alert("Failed to copy link. Please copy manually.");
      }
    });
  }

  /* ---------------------------
     Activate / Deactivate logic
  ---------------------------- */
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.dataset.action;
    if (!["activate", "deactivate"].includes(action)) return;

    // Find the card container (not the button)
    const card = btn.closest(".account-card");
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
      // For activation, get the selected permission level
      let requestBody = { user_id: userId };
      
      if (action === "activate") {
        // Try to find permission select in the card
        const permissionSelect = card.querySelector('.permission-select');
        console.log("DEBUG: Card element:", card);
        console.log("DEBUG: Card class:", card.className);
        console.log("DEBUG: permissionSelect element:", permissionSelect);
        
        if (permissionSelect) {
          requestBody.permission_level = permissionSelect.value;
          console.log("DEBUG: Selected permission level:", permissionSelect.value);
        } else {
          console.log("DEBUG: No permission select found in card");
          console.log("DEBUG: Card HTML:", card.innerHTML);
        }
      }
      
      console.log("DEBUG: Request body:", requestBody);
      
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(requestBody),
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

  /* ---------------------------
     Edit User Modal
  ---------------------------- */
  document.addEventListener("click", (e) => {
    const editBtn = e.target.closest("[data-action='edit']");
    if (!editBtn) return;

    const userId = editBtn.dataset.userId;
    const firstName = editBtn.dataset.userFirstName;
    const lastName = editBtn.dataset.userLastName;
    const phone = editBtn.dataset.userPhone || "";
    const isStaff = editBtn.dataset.userIsStaff === "True";

    // Create modal
    const modal = document.createElement("div");
    modal.className = "edit-user-modal";
    modal.innerHTML = `
      <div class="modal-backdrop"></div>
      <div class="modal-content">
        <h2>Edit User: ${firstName} ${lastName}</h2>
        <form id="edit-user-form">
          <div class="form-group">
            <label for="edit-phone">Phone Number</label>
            <input type="tel" id="edit-phone" value="${phone}" placeholder="(555) 555-5555">
          </div>
          <div class="form-group">
            <label for="edit-permission">Permissions</label>
            <select id="edit-permission">
              <option value="basic" ${!isStaff ? 'selected' : ''}>Basic</option>
              <option value="elevated" ${isStaff ? 'selected' : ''}>Elevated</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" class="btn btn-secondary" data-action="close-modal">Cancel</button>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(modal);
    // Debug: Add change listeners to see if values are actually changing
    const phoneInputDebug = modal.querySelector("#edit-phone");
    const permissionSelectDebug = modal.querySelector("#edit-permission");
    
    console.log("DEBUG: Initial phone value:", phoneInputDebug.value);
    console.log("DEBUG: Initial permission value:", permissionSelectDebug.value);
    
    phoneInputDebug.addEventListener("input", (e) => {
      console.log("DEBUG: Phone input changed to:", e.target.value);
    });
    
    permissionSelectDebug.addEventListener("change", (e) => {
      console.log("DEBUG: Permission changed to:", e.target.value);
    });


    // Handle close
    modal.querySelector("[data-action='close-modal']").addEventListener("click", () => {
      modal.remove();
    });

    modal.querySelector(".modal-backdrop").addEventListener("click", () => {
      modal.remove();
    });

    // Handle submit
    modal.querySelector("#edit-user-form").addEventListener("submit", async (e) => {
      e.preventDefault();

      const newPhone = document.getElementById("edit-phone").value.trim();
      const newPermission = document.getElementById("edit-permission").value;

      console.log("DEBUG: Submitting edit for user", userId);
      console.log("DEBUG: New phone:", newPhone);
      console.log("DEBUG: New permission:", newPermission);

      try {
        const resp = await fetch(`/accounts/edit/${userId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            phone: newPhone,
            permission_level: newPermission,
          }),
        });

        console.log("DEBUG: Response status:", resp.status);
        
        const data = await resp.json();
        console.log("DEBUG: Response data:", data);

        if (!resp.ok || !data.success) {
          alert(data.error || "Failed to update user");
          return;
        }

        alert(data.message);
        modal.remove();
        window.location.reload();
      } catch (err) {
        console.error("DEBUG: Error details:", err);
        alert("Network error. Please try again.");
      }
    });
  });
});

  /* ---------------------------
     Edit User Modal
  ---------------------------- */
  document.addEventListener("click", (e) => {
    const editBtn = e.target.closest("[data-action='edit']");
    if (!editBtn) return;

    const userId = editBtn.dataset.userId;
    const firstName = editBtn.dataset.userFirstName;
    const lastName = editBtn.dataset.userLastName;
    const phone = editBtn.dataset.userPhone || "";
    const isStaff = editBtn.dataset.userIsStaff === "True";

    // Create modal
    const modal = document.createElement("div");
    modal.className = "edit-user-modal";
    modal.innerHTML = `
      <div class="modal-backdrop"></div>
      <div class="modal-content">
        <h2>Edit User: ${firstName} ${lastName}</h2>
        <form id="edit-user-form">
          <div class="form-group">
            <label for="edit-phone">Phone Number</label>
            <input type="tel" id="edit-phone" value="${phone}" placeholder="(555) 555-5555">
          </div>
          <div class="form-group">
            <label for="edit-permission">Permissions</label>
            <select id="edit-permission">
              <option value="basic" ${!isStaff ? 'selected' : ''}>Basic</option>
              <option value="elevated" ${isStaff ? 'selected' : ''}>Elevated</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" class="btn btn-secondary" data-action="close-modal">Cancel</button>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(modal);

    // Handle close
    modal.querySelector("[data-action='close-modal']").addEventListener("click", () => {
      modal.remove();
    });

    modal.querySelector(".modal-backdrop").addEventListener("click", () => {
      modal.remove();
    });

    // Handle submit
    modal.querySelector("#edit-user-form").addEventListener("submit", async (e) => {
      e.preventDefault();

      const newPhone = document.getElementById("edit-phone").value.trim();
      const newPermission = document.getElementById("edit-permission").value;

      console.log("DEBUG: Submitting edit for user", userId);
      console.log("DEBUG: New phone:", newPhone);
      console.log("DEBUG: New permission:", newPermission);

      try {
        const resp = await fetch(`/accounts/edit/${userId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            phone: newPhone,
            permission_level: newPermission,
          }),
        });

        console.log("DEBUG: Response status:", resp.status);
        
        const data = await resp.json();
        console.log("DEBUG: Response data:", data);

        if (!resp.ok || !data.success) {
          alert(data.error || "Failed to update user");
          return;
        }

        alert(data.message);
        modal.remove();
        window.location.reload();
      } catch (err) {
        console.error("DEBUG: Error details:", err);
        alert("Network error. Please try again.");
      }
    });
  });