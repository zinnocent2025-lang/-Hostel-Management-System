
window.openUsers = openUsers;
window.openPermissions = openPermissions;
window.updateUser = updateUser;
window.togglePerm = togglePerm;
window.deleteGroup = deleteGroup;
window.closeUsers = closeUsers;
window.closePermissions = closePermissions;

let currentGroup = null;
let currentGroupName = "";

// ================= OPEN PERMISSIONS MODAL =================
function openPermissions(groupId, groupName) {

    currentGroup = groupId;
    currentGroupName = groupName;

    document.getElementById("permissionsModal").style.display = "flex";
    document.getElementById("permTitle").innerText = groupName + " - Permissions";

    fetch(`/dashboard/group-data/${groupId}/`)
        .then(res => res.json())
        .then(data => {

            let permHTML = "";

            data.permissions.forEach(p => {
                permHTML += `
                <div class="row">
                    <label>
                        <input type="checkbox"
                            ${p.enabled ? "checked" : ""}
                            onchange="togglePerm(${p.id})">
                        ${p.name}
                    </label>
                </div>
            `;
            });

            document.getElementById("permContainer").innerHTML = permHTML;

            // Hide delete for Admin
            document.getElementById("deleteGroupBtn").style.display =
                data.is_admin ? "none" : "block";
        });
}

// ================= OPEN USERS MODAL =================
function openUsers(groupId, groupName) {

    currentGroup = parseInt(groupId);
    currentGroupName = groupName;

    document.getElementById("usersModal").style.display = "flex";
    document.getElementById("usersTitle").innerText = groupName + " - Users";

    fetch(`/dashboard/group-data/${groupId}/`)
        .then(res => res.json())
        .then(data => {

            let usersHTML = ""; // ✅ THIS WAS MISSING

            data.users.forEach(u => {
                usersHTML += `
                <div class="row">
                    <span>${u.username}</span>
                    <button class="btn-action"
                        onclick="updateUser(${u.id}, '${u.in_group ? 'remove' : 'add'}')">
                        ${u.in_group ? "Remove" : "Add"}
                    </button>
                </div>
            `;
            });

            document.getElementById("usersContainer").innerHTML = usersHTML;
        });
}

// ================= UPDATE USER =================
function updateUser(userId, action) {

    console.log("Sending:", userId, currentGroup, action);

    fetch(`/dashboard/update-group-user/?user_id=${userId}&group_id=${currentGroup}&action=${action}`)
        .then(res => res.json())
        .then(data => {

            console.log("Response:", data);

            if (data.error) {
                alert(data.error);
                return;
            }

            openUsers(currentGroup, currentGroupName);

            openUsers(currentGroup, currentGroupName);

            // 🔥 update badge only
            updateBadge(currentGroup);
        });
}


// ================= TOGGLE PERMISSION =================
function togglePerm(permId) {

    fetch(`/dashboard/toggle-permission/?group_id=${currentGroup}&perm_id=${permId}`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            // 🔥 REFRESH BOTH MODAL + CARD UI
            openPermissions(currentGroup, currentGroupName);

            // 🔥 ALSO REFRESH MAIN PAGE
            location.reload();
        });
}

// ================= DELETE GROUP =================
function deleteGroup() {

    if (!confirm("Delete this group?")) return;

    fetch(`/dashboard/delete-group/${currentGroup}/`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
            } else {
                location.reload();
            }
        });
}

// ================= CLOSE MODALS =================
function closePermissions() {
    document.getElementById("permissionsModal").style.display = "none";
}

function closeUsers() {
    document.getElementById("usersModal").style.display = "none";
}

function updateBadge(groupId) {

    fetch(`/dashboard/group-data/${groupId}/`)
    .then(res => res.json())
    .then(data => {

        const card = document.getElementById(`group-${groupId}`);
        const badge = card.querySelector(".badge");

        const count = data.users.filter(u => u.in_group).length;

        badge.innerText = count + (count === 1 ? " user" : " users");
    });
}