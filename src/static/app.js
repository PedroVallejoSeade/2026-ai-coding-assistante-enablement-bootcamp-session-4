document.addEventListener("DOMContentLoaded", () => {
  const capabilitiesList = document.getElementById("capabilities-list");
  const capabilitySelect = document.getElementById("capability");
  const registerForm = document.getElementById("register-form");
  const consultantForm = document.getElementById("consultant-form");
  const consultantList = document.getElementById("consultants-list");
  const consultantTitle = document.getElementById("consultant-form-title");
  const consultantEmailInput = document.getElementById("consultant-email");
  const consultantNameInput = document.getElementById("consultant-name");
  const consultantPracticeAreaInput = document.getElementById("consultant-practice-area");
  const consultantAvailabilityInput = document.getElementById("consultant-availability");
  const consultantCertificationsInput = document.getElementById("consultant-certifications");
  const consultantSkillsInput = document.getElementById("consultant-skills");
  const consultantSubmitButton = document.getElementById("consultant-submit");
  const consultantCancelButton = document.getElementById("consultant-cancel");
  const messageDiv = document.getElementById("message");

  let editingConsultantEmail = null;

  function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");

    window.clearTimeout(showMessage.timeoutId);
    showMessage.timeoutId = window.setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function parseCommaSeparatedList(value) {
    return value
      .split(",")
      .map((entry) => entry.trim())
      .filter(Boolean);
  }

  function resetConsultantForm() {
    editingConsultantEmail = null;
    consultantForm.reset();
    consultantTitle.textContent = "Create Consultant Profile";
    consultantSubmitButton.textContent = "Save Consultant Profile";
    consultantEmailInput.disabled = false;
    consultantCancelButton.classList.add("hidden");
  }

  function populateConsultantForm(consultant) {
    editingConsultantEmail = consultant.email;
    consultantTitle.textContent = `Update ${consultant.name || consultant.email}`;
    consultantSubmitButton.textContent = "Update Consultant Profile";
    consultantEmailInput.value = consultant.email || "";
    consultantEmailInput.disabled = true;
    consultantNameInput.value = consultant.name || "";
    consultantPracticeAreaInput.value = consultant.practice_area || "";
    consultantAvailabilityInput.value = consultant.availability || "";
    consultantCertificationsInput.value = (consultant.certifications || []).join(", ");
    consultantSkillsInput.value = (consultant.skills || []).join(", ");
    consultantCancelButton.classList.remove("hidden");
  }

  async function fetchCapabilities() {
    try {
      const response = await fetch("/capabilities");
      if (!response.ok) {
        throw new Error("Failed to fetch capabilities");
      }

      const capabilities = await response.json();
      capabilitiesList.innerHTML = "";
      capabilitySelect.innerHTML = '<option value="">-- Select a capability --</option>';

      Object.entries(capabilities).forEach(([name, details]) => {
        const capabilityCard = document.createElement("div");
        capabilityCard.className = "capability-card";

        const availableCapacity = details.capacity || 0;
        const consultants = details.consultants || [];
        const consultantsHTML = consultants.length > 0
          ? `<div class="consultants-section">
              <h5>Registered Consultants:</h5>
              <ul class="consultants-list">
                ${consultants
                  .map((consultant) => {
                    const consultantName = consultant.name || consultant.email;
                    const consultantPracticeArea = consultant.practice_area || "Unassigned";
                    const consultantAvailability = consultant.availability || "Unknown";
                    return `<li>
                      <div class="consultant-summary">
                        <span class="consultant-email">${escapeHtml(consultantName)}</span>
                        <span class="consultant-meta">${escapeHtml(consultant.email)} • ${escapeHtml(consultantPracticeArea)} • ${escapeHtml(consultantAvailability)}</span>
                      </div>
                      <button class="delete-btn" data-capability="${escapeHtml(name)}" data-email="${escapeHtml(consultant.email)}">Remove</button>
                    </li>`;
                  })
                  .join("")}
              </ul>
            </div>`
          : "<p><em>No consultants registered yet</em></p>";

        capabilityCard.innerHTML = `
          <h4>${escapeHtml(name)}</h4>
          <p>${escapeHtml(details.description)}</p>
          <p><strong>Practice Area:</strong> ${escapeHtml(details.practice_area)}</p>
          <p><strong>Industry Verticals:</strong> ${escapeHtml((details.industry_verticals || []).join(", ") || "Not specified")}</p>
          <p><strong>Capacity:</strong> ${escapeHtml(String(availableCapacity))} hours/week available</p>
          <p><strong>Current Team:</strong> ${escapeHtml(String(consultants.length))} consultants</p>
          <div class="consultants-container">
            ${consultantsHTML}
          </div>
        `;

        capabilitiesList.appendChild(capabilityCard);

        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        capabilitySelect.appendChild(option);
      });

      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      capabilitiesList.innerHTML = "<p>Failed to load capabilities. Please try again later.</p>";
      console.error("Error fetching capabilities:", error);
    }
  }

  async function fetchConsultants() {
    try {
      const response = await fetch("/consultants");
      if (!response.ok) {
        throw new Error("Failed to fetch consultants");
      }

      const consultants = await response.json();
      if (consultants.length === 0) {
        consultantList.innerHTML = "<p><em>No consultant profiles available yet</em></p>";
        return;
      }

      consultantList.innerHTML = `
        <div class="consultant-profile-list">
          ${consultants
            .map(
              (consultant) => `
                <article class="consultant-profile-card">
                  <div>
                    <h4>${escapeHtml(consultant.name || consultant.email)}</h4>
                    <p>${escapeHtml(consultant.email)}</p>
                    <p><strong>Practice Area:</strong> ${escapeHtml(consultant.practice_area || "Unassigned")}</p>
                    <p><strong>Availability:</strong> ${escapeHtml(consultant.availability || "Unknown")}</p>
                    <p><strong>Capabilities:</strong> ${escapeHtml((consultant.capabilities || []).join(", ") || "Not yet assigned")}</p>
                  </div>
                  <button class="edit-btn" data-email="${escapeHtml(consultant.email)}">Edit</button>
                </article>
              `
            )
            .join("")}
        </div>
      `;

      document.querySelectorAll(".edit-btn").forEach((button) => {
        button.addEventListener("click", async () => {
          const email = button.getAttribute("data-email");
          const response = await fetch(`/consultants/${encodeURIComponent(email)}`);
          const consultant = await response.json();
          populateConsultantForm(consultant);
        });
      });
    } catch (error) {
      consultantList.innerHTML = "<p>Failed to load consultant profiles. Please try again later.</p>";
      console.error("Error fetching consultants:", error);
    }
  }

  async function refreshData() {
    await Promise.all([fetchCapabilities(), fetchConsultants()]);
  }

  async function handleUnregister(event) {
    const button = event.target;
    const capability = button.getAttribute("data-capability");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(capability)}/unregister?email=${encodeURIComponent(email)}`,
        { method: "DELETE" }
      );
      const result = await response.json();

      if (!response.ok) {
        showMessage(result.detail || "An error occurred", "error");
        return;
      }

      await refreshData();
      showMessage(result.message, "success");
    } catch (error) {
      showMessage("Failed to unregister. Please try again.", "error");
      console.error("Error unregistering:", error);
    }
  }

  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const capability = capabilitySelect.value;

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(capability)}/register?email=${encodeURIComponent(email)}`,
        { method: "POST" }
      );
      const result = await response.json();

      if (!response.ok) {
        showMessage(result.detail || "An error occurred", "error");
        return;
      }

      registerForm.reset();
      await refreshData();
      showMessage(result.message, "success");
    } catch (error) {
      showMessage("Failed to register. Please try again.", "error");
      console.error("Error registering:", error);
    }
  });

  consultantForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      email: consultantEmailInput.value,
      name: consultantNameInput.value,
      practice_area: consultantPracticeAreaInput.value,
      availability: consultantAvailabilityInput.value,
      certifications: parseCommaSeparatedList(consultantCertificationsInput.value),
      skills: parseCommaSeparatedList(consultantSkillsInput.value),
    };

    const isUpdate = Boolean(editingConsultantEmail);
    const url = isUpdate
      ? `/consultants/${encodeURIComponent(editingConsultantEmail)}`
      : "/consultants";
    const method = isUpdate ? "PATCH" : "POST";
    const body = isUpdate
      ? JSON.stringify({
          name: payload.name,
          practice_area: payload.practice_area,
          availability: payload.availability,
          certifications: payload.certifications,
          skills: payload.skills,
        })
      : JSON.stringify(payload);

    try {
      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body,
      });
      const result = await response.json();

      if (!response.ok) {
        showMessage(result.detail || "Unable to save consultant profile.", "error");
        return;
      }

      resetConsultantForm();
      await refreshData();
      showMessage(
        isUpdate ? `Updated ${result.email}` : `Created ${result.email}`,
        "success"
      );
    } catch (error) {
      showMessage("Failed to save consultant profile. Please try again.", "error");
      console.error("Error saving consultant profile:", error);
    }
  });

  consultantCancelButton.addEventListener("click", resetConsultantForm);

  resetConsultantForm();
  refreshData();
});
