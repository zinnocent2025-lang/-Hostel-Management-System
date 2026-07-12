const openBtn = document.getElementById("openPanel");
const closeBtn = document.getElementById("closePanel");
const panel = document.getElementById("controlPanel");

const adminToggle = document.getElementById("adminToggle");
const adminDropdown = document.getElementById("adminDropdown");

const openProfile = document.getElementById("openProfile");
const profileModal = document.getElementById("profileModal");
const closeProfile = document.getElementById("closeProfile");

// TOGGLE DROPDOWN
adminToggle.onclick = () => {
    adminDropdown.classList.toggle("show");
};

// OPEN PROFILE
openProfile.onclick = () => {
    profileModal.style.display = "flex";
    adminDropdown.classList.remove("show");
};

// CLOSE PROFILE
closeProfile.onclick = () => {
    profileModal.style.display = "none";
};

// CLICK OUTSIDE
window.onclick = (e) => {
    if (!e.target.closest(".admin-section")) {
        adminDropdown.classList.remove("show");
    }

    if (e.target === profileModal) {
        profileModal.style.display = "none";
    }
};
openBtn.addEventListener("click", () => {
    panel.classList.add("active");
});

closeBtn.addEventListener("click", () => {
    panel.classList.remove("active");
});

// ================= PROFILE SAVE =================

const uploadTrigger = document.getElementById("uploadTrigger");
const profileInput = document.getElementById("profileInput");
const profilePreview = document.getElementById("profilePreview");

// OPEN FILE PICKER
uploadTrigger.onclick = () => profileInput.click();

// PREVIEW IMAGE
profileInput.onchange = () => {
    const file = profileInput.files[0];
    if (file) {
        profilePreview.src = URL.createObjectURL(file);
    }
};

// SAVE PROFILE
document.getElementById("saveProfile").onclick = function () {

    let formData = new FormData();

    let email = document.getElementById("profileEmail").value;
    let imageInput = document.getElementById("profileInput");

    formData.append("email", email);

    // 🔥 VERY IMPORTANT
    if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]);
    }

    fetch("/dashboard/update-profile/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
        .then(res => res.json())
        .then(() => {
            alert("Updated");
            location.reload();
        });
};

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        .split('=')[1];
}

const gearIcon = document.querySelector(".fa-gear");
const settingsPanel = document.getElementById("settingsPanel");

gearIcon.onclick = () => {
    settingsPanel.style.display =
        settingsPanel.style.display === "block" ? "none" : "block";
};

window.addEventListener("click", function (e) {
    if (!e.target.closest(".fa-gear") && !e.target.closest("#settingsPanel")) {
        settingsPanel.style.display = "none";
    }
});


function openNotifications() {
    document.getElementById("settingsMain").style.display = "none";

    document.getElementById("settingsSub").style.display = "block";
    document.getElementById("settingsSub").innerHTML = `
        <div class="settings-header" onclick="goBack()">← Back</div>
        <p>No new notifications</p>
    `;
}
function openSystemInfo() {
    document.getElementById("settingsMain").style.display = "none";

    document.getElementById("settingsSub").style.display = "block";
    document.getElementById("settingsSub").innerHTML = `
        <div class="settings-header" onclick="goBack()">← Back</div>
        <p>Users: --</p>
        <p>Hostels: --</p>
        <p>Bookings: --</p>
    `;
}
window.addEventListener("click", function (e) {
    if (!e.target.closest("#settingsPanel") && !e.target.closest("#infoCard") && !e.target.closest(".fa-gear")) {
        document.getElementById("infoCard").style.display = "none";
    }
});

function goBack() {
    document.getElementById("settingsMain").style.display = "block";
    document.getElementById("settingsSub").style.display = "none";
}


const openHM = document.getElementById("openHostelManager");
const hostelManager = document.getElementById("hostelManager");
const closeHM = document.getElementById("closeHostelManager");

openHM.onclick = () => hostelManager.classList.add("show");
closeHM.onclick = () => hostelManager.classList.remove("show");

const deleteButtons = document.querySelectorAll(".delete-btn");

const deleteModal = document.getElementById("deleteModal");

const confirmDelete = document.getElementById("confirmDelete");

const cancelDelete = document.getElementById("cancelDelete");

deleteButtons.forEach(button => {

    button.addEventListener("click", () => {

        deleteModal.style.display = "flex";

        confirmDelete.href = button.dataset.url;

    });

});

cancelDelete.addEventListener("click", () => {

    deleteModal.style.display = "none";

});



const hostelSearch = document.getElementById("hostelSearch");

hostelSearch.addEventListener("keyup", () => {

    const value = hostelSearch.value.toLowerCase();

    const hostelRows = document.querySelectorAll(".hostel-row");

    hostelRows.forEach(row => {

        const text = row.innerText.toLowerCase();

        row.style.display = text.includes(value)
            ? "flex"
            : "none";

    });

});

/* =========================
   LOGOUT MODAL
========================= */

const openLogoutModal =
    document.getElementById("openLogoutModal");

const logoutModal =
    document.getElementById("logoutModal");

const cancelLogout =
    document.getElementById("cancelLogout");

if (
    openLogoutModal &&
    logoutModal &&
    cancelLogout
) {

    openLogoutModal.addEventListener("click", () => {

        logoutModal.classList.add("active");

        adminDropdown.classList.remove("show");

    });

    cancelLogout.addEventListener("click", () => {

        logoutModal.classList.remove("active");

    });

    logoutModal.addEventListener("click", (e) => {

        if (e.target === logoutModal) {

            logoutModal.classList.remove("active");

        }

    });

}

// =========================
// MESSAGE MODAL
// =========================

const messageModal =
    document.getElementById("messageModal");

const openMessages =
    document.getElementById("openMessages");

const closeMessages =
    document.getElementById("closeMessages");

const messageBox =
    document.querySelector(".message-box");

// OPEN

if (openMessages) {

    openMessages.addEventListener("click", () => {

        messageModal.classList.add("active");

    });
}

// CLOSE BUTTON

if (closeMessages) {

    closeMessages.addEventListener("click", () => {

        messageModal.classList.remove("active");

    });
}

// ONLY CLOSE WHEN CLICKING OUTSIDE

if (messageModal) {

    messageModal.addEventListener("click", (e) => {

        if (!messageBox.contains(e.target)) {

            messageModal.classList.remove("active");

        }

    });
}

// =========================
// TYPING INDICATOR
// =========================

const chatInput =
    document.getElementById("chatInput");

const typingIndicator =
    document.getElementById("typingIndicator");

let typingTimeout;

if (chatInput && typingIndicator) {

    chatInput.addEventListener("input", () => {

        typingIndicator.style.display = "block";

        clearTimeout(typingTimeout);

        typingTimeout = setTimeout(() => {

            typingIndicator.style.display = "none";

        }, 1500);

    });

}

// ================= VOICE RECORD =================

const recordBtn = document.getElementById("recordVoice");

if (recordBtn) {

    let mediaRecorder;

    let audioChunks = [];

    let isRecording = false;

    recordBtn.addEventListener("click", async () => {

        // START RECORDING
        if (!isRecording) {

            try {

                const stream =
                    await navigator.mediaDevices.getUserMedia({
                        audio: true
                    });

                mediaRecorder =
                    new MediaRecorder(stream);

                mediaRecorder.start();

                audioChunks = [];

                mediaRecorder.ondataavailable = e => {

                    audioChunks.push(e.data);
                };

                mediaRecorder.onstop = async () => {

                    const audioBlob =
                        new Blob(audioChunks, {
                            type: "audio/webm"
                        });

                    const audioFile =
                        new File(
                            [audioBlob],
                            "voice.webm",
                            {
                                type: "audio/webm"
                            }
                        );

                    const dataTransfer =
                        new DataTransfer();

                    dataTransfer.items.add(audioFile);

                    document.getElementById(
                        "chatFile"
                    ).files =
                        dataTransfer.files;

                    document.getElementById(
                        "chatForm"
                    ).submit();
                };

                recordBtn.innerHTML =
                    '<i class="fa-solid fa-stop"></i>';

                recordBtn.style.background =
                    "#dc2626";

                isRecording = true;

            } catch (error) {

                alert(
                    "Microphone access denied"
                );
            }

        }

        // STOP RECORDING
        else {

            mediaRecorder.stop();

            recordBtn.innerHTML =
                '<i class="fa-solid fa-microphone"></i>';

            recordBtn.style.background =
                "#2563eb";

            isRecording = false;
        }
    });
}

// AUTO SCROLL CHAT

const chatMessages =
    document.querySelector(".chat-messages");

if (chatMessages) {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


const chatForm =
    document.getElementById("chatForm");

if (chatForm) {

    chatForm.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            const formData =
                new FormData(chatForm);

            const response =
                await fetch(
                    window.location.href,
                    {
                        method: "POST",
                        body: formData,
                        headers: {
                            "X-Requested-With": "XMLHttpRequest"
                        }
                    }
                );

            if (response.ok) {

                location.reload();

            }

        }
    );
}

const bookingModal =
    document.getElementById(
        "bookingSettingsModal"
    );

const openBookingBtn =
    document.getElementById(
        "openBookingSettings"
    );

const closeBookingBtn =
    document.getElementById(
        "closeBookingModal"
    );

if (
    bookingModal &&
    openBookingBtn &&
    closeBookingBtn
) {

    openBookingBtn.onclick = () => {

        bookingModal.classList.add("show");

        loadBookingSettings();

    };

    closeBookingBtn.onclick = () => {

        bookingModal.classList.remove(
            "show"
        );

    };

}


function loadBookingSettings() {

    fetch("/dashboard/get-settings/")

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "maleDeadline"
            ).value =
                data.male_booking_deadline;

            document.getElementById(
                "femaleDeadline"
            ).value =
                data.female_booking_deadline;

            document.getElementById(
                "externalDeadline"
            ).value =
                data.external_booking_deadline;

            document.getElementById(
                "allowMale"
            ).checked =
                data.allow_male_booking;

            document.getElementById(
                "allowFemale"
            ).checked =
                data.allow_female_booking;

            document.getElementById(
                "allowExternal"
            ).checked =
                data.allow_external_booking;
        });

}


document
    .getElementById("saveBookingSettings")
    .addEventListener("click", () => {

        fetch(
            "/dashboard/update-settings/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "X-CSRFToken":
                        getCSRFToken()
                },

                body: JSON.stringify({

                    male_booking_deadline: document.getElementById("maleDeadline").value,

                    female_booking_deadline: document.getElementById("femaleDeadline").value,
                    male_hostel_price:
                        document.getElementById("malePrice").value,

                    female_hostel_price:
                        document.getElementById("femalePrice").value,

                    external_booking_deadline:
                        document.getElementById(
                            "externalDeadline"
                        ).value,

                    allow_male_booking:
                        document.getElementById(
                            "allowMale"
                        ).checked,

                    allow_female_booking:
                        document.getElementById(
                            "allowFemale"
                        ).checked,

                    allow_external_booking:
                        document.getElementById(
                            "allowExternal"
                        ).checked

                })

            }
        )

            .then(res => res.json())

            .then(data => {

                if (data.success) {

                    alert(
                        "Settings saved successfully"
                    );

                    bookingModal.classList.remove(
                        "show"
                    );

                }

            });

    });