document.addEventListener("DOMContentLoaded", function () {

    // ===== MENU TOGGLE =====
    const menuBtn = document.getElementById("menuBtn");
    const menuDropdown = document.getElementById("menuDropdown");

    if (menuBtn && menuDropdown) {
        menuBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            menuDropdown.classList.toggle("show");
        });

        document.addEventListener("click", function () {
            menuDropdown.classList.remove("show");
        });
    }

    // ===== LIVE SEARCH =====
    const searchInput = document.getElementById("searchInput");
    const rows = document.querySelectorAll(".user-card");
    const usersContainer = document.getElementById("usersContainer");
    const searchStatus = document.getElementById("searchStatus");

    let timeout = null;

    if (searchInput) {
        searchInput.addEventListener("input", function () {

            clearTimeout(timeout);
            const query = this.value.toLowerCase();

            // EMPTY → SHOW ALL
            if (query === "") {
                if (searchStatus) searchStatus.innerText = "";

                rows.forEach(row => {
                    row.style.display = "block";
                });

                return;
            }

            // FRONTEND SEARCH (< 3 letters)


            // BACKEND SEARCH (>= 3 letters)
            if (searchStatus) searchStatus.innerText = "Searching...";

            timeout = setTimeout(() => {

                fetch(`/dashboard/search-users/?q=${query}`)
                    .then(res => res.json())
                    .then(data => {

                        usersContainer.innerHTML = "";

                        if (data.users.length === 0) {
                            if (searchStatus) searchStatus.innerText = "No users found";
                            return;
                        }

                        if (searchStatus) searchStatus.innerText = "";

                        data.users.forEach(user => {

                            usersContainer.innerHTML += `
        <div class="user-card"
             data-active="${user.is_active}"
             data-staff="${user.is_staff}"
             data-id="${user.id}">

            <input type="checkbox" class="select-user">

            <div class="avatar-wrapper">

                <div class="avatar-circle">

                    ${user.image
                                    ? `<img src="${user.image}" class="avatar-img">`
                                    : `<div class="avatar-fallback">${user.username.charAt(0).toUpperCase()}</div>`
                                }

                </div>

            </div>

            <div class="user-info">

                <h3>${user.full_name}</h3>

                <p class="username-tag">@${user.username}</p>

                <p class="user-email">${user.email}</p>

                <small>
                    <i class="fa-solid fa-phone"></i>
                    ${user.phone || "No Phone"}
                </small>

                <small>
                    <i class="fa-solid fa-building-columns"></i>
                    ${user.department || "No Department"}
                </small>

                <small>
                    <i class="fa-solid fa-id-card"></i>
                    ${user.matric_no || "No Matric No"}
                </small>

            </div>

            <div class="actions">

                <button onclick="openUser('${user.id}')">
                    View
                </button>

                <button class="delete-btn"
                        onclick="deleteUser('${user.id}')">
                    Delete
                </button>

            </div>

        </div>
    `;

                        });
                    });

            }, 400);

        });
    }

    // ===== ADD USER MODAL =====
    const modal = document.getElementById("userModal");
    const addBtn = document.querySelector(".add-btn");
    const closeBtn = document.getElementById("closeModal");

    if (addBtn && modal) {
        addBtn.addEventListener("click", () => {
            modal.style.display = "flex";
        });
    }

    if (closeBtn && modal) {
        closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    // ===== VIEW MODAL =====
    const viewModal = document.getElementById("viewModal");
    const closeViewBtn = document.getElementById("closeView");

    if (closeViewBtn && viewModal) {
        closeViewBtn.onclick = () => {
            viewModal.classList.remove("show");
        };
    }

    window.addEventListener("click", (e) => {
        if (e.target === viewModal) {
            viewModal.classList.remove("show");
        }
    });

});


// ===== GLOBAL FUNCTIONS (IMPORTANT) =====

// VIEW USER
let currentUserId = null;

function openUser(userId) {
    currentUserId = userId;

    fetch(`/dashboard/get-user/${userId}/`)
        .then(res => res.json())
        .then(data => {

            document.getElementById("viewImage").src = data.image;
            document.getElementById("viewUsername").innerText = data.full_name;
            document.getElementById("viewEmail").innerText = data.email;

            document.getElementById("viewRole").innerText = data.is_staff ? "Staff" : "User";

            document.getElementById("statusSelect").value = data.is_active ? "active" : "suspended";
            document.getElementById("viewPhone").value =
                data.phone || "";

            document.getElementById("viewDepartment").value =
                data.department || "";

            document.getElementById("viewLevel").value =
                data.level || "";

            document.getElementById("viewMatric").value =
                data.matric_no || "";

            document.getElementById("viewGender").value =
                data.gender || "";

            const statusDot =
                document.getElementById("statusDot");

            if (data.is_active) {

                statusDot.style.background = "#22c55e";

            } else {

                statusDot.style.background = "#ef4444";
            }

            document.getElementById("viewJoined").innerText = data.date_joined;
            document.getElementById("viewLogin").innerText = data.last_login || "Never";
            document.getElementById("viewHostel").innerText =
                data.hostel;

            document.getElementById("viewRoom").innerText =
                data.room;

            document.getElementById("viewBookingStatus").innerText =
                data.booking_status;

            document.getElementById("viewBookingCount").innerText =
                data.booking_count;

            document.getElementById("viewModal").classList.add("show");

        })
        .catch(err => {
            console.error("Error:", err);
        });

}


// DELETE USER
function deleteUser(userId) {

    if (!confirm("Are you sure you want to delete this user?")) return;

    fetch(`/dashboard/delete-user/${userId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Delete failed");
            }
        })
        .catch(err => {
            console.error("DELETE ERROR:", err);
        });
}


// IMAGE UPLOAD
function triggerUpload(btn) {
    const card = btn.closest(".user-card");
    const input = card.querySelector(".upload-input");

    if (input) input.click();
}

function uploadImage(event, userId) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    fetch(`/dashboard/upload-image/${userId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Upload failed");
            }
        })
        .catch(err => {
            console.error("UPLOAD ERROR:", err);
        });
}


// CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// ===== FILTER MENU =====
const filterAll = document.getElementById("filterAll");
const filterActive = document.getElementById("filterActive");
const filterStaff = document.getElementById("filterStaff");

function filterUsers(type) {
    const cards = document.querySelectorAll(".user-card");

    cards.forEach(card => {
        const isActive = card.dataset.active === "True";
        const isStaff = card.dataset.staff === "True";

        if (type === "all") {
            card.style.display = "block";
        } else if (type === "active") {
            card.style.display = isActive ? "block" : "none";
        } else if (type === "staff") {
            card.style.display = isStaff ? "block" : "none";
        }
    });
}

if (filterAll) filterAll.onclick = () => filterUsers("all");
if (filterActive) filterActive.onclick = () => filterUsers("active");
if (filterStaff) filterStaff.onclick = () => filterUsers("staff");


// ===== BULK DELETE =====
const bulkDeleteBtn = document.getElementById("bulkDelete");

if (bulkDeleteBtn) {
    bulkDeleteBtn.onclick = function () {

        const selected = document.querySelectorAll(".select-user:checked");

        if (selected.length === 0) {
            alert("No users selected");
            return;
        }

        if (!confirm("Delete selected users?")) return;

        selected.forEach(checkbox => {
            const card = checkbox.closest(".user-card");
            const userId = card.dataset.id;

            fetch(`/dashboard/delete-user/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            })
                .then(() => {
                    card.remove();
                });
        });
    };
}


// ===== EXPORT USERS =====
const exportBtn = document.getElementById("exportUsers");

if (exportBtn) {
    exportBtn.onclick = function () {
        window.location.href = "/dashboard/export-users/";
    };
}

const saveUserBtn =
    document.getElementById("saveUserBtn");

if (saveUserBtn) {

    saveUserBtn.addEventListener("click", () => {

        const status = document.getElementById("statusSelect").value;
        const phone =
            document.getElementById("viewPhone").value;

        const department =
            document.getElementById("viewDepartment").value;

        const level =
            document.getElementById("viewLevel").value;

        const matric_no =
            document.getElementById("viewMatric").value;

        const gender =
            document.getElementById("viewGender").value;

        fetch("/dashboard/update-user-status/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                user_id: currentUserId,

                status: status,

                phone: phone,

                department: department,

                level: level,

                matric_no: matric_no,

                gender: gender

            })

        })

            .then(res => res.json())

            .then(data => {

                if (data.success) {

                    alert("User updated successfully");

                    location.reload();

                } else {

                    alert("Update failed");

                }

            });

    });

}