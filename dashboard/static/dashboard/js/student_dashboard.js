document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menuToggle");
    const sidebar = document.querySelector(".sidebar");

    menuBtn.addEventListener("click", function () {
        sidebar.classList.toggle("active");
    });

    document.addEventListener("click", function (e) {
        if (
            !sidebar.contains(e.target) &&
            !menuBtn.contains(e.target)
        ) {
            sidebar.classList.remove("active");
        }
    });

});

document.addEventListener("DOMContentLoaded", function () {

    /* PIE CHART */

    new Chart(document.getElementById("pieChart"), {

        type: "pie",

        data: {

            labels: [
                "Occupied",
                "Available",
                "Maintenance"
            ],

            datasets: [{

                data: [

                    hostelAnalytics.occupied,
                    hostelAnalytics.available,
                    hostelAnalytics.maintenance

                ],

                backgroundColor: [

                    "#2563eb",
                    "#10b981",
                    "#f59e0b"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    position: "bottom"
                }

            }

        }

    });
    /* LINE CHART */
    /* LINE CHART */
    new Chart(document.getElementById("lineChart"), {
        type: "line",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            datasets: [{
                label: "Electricity Level",
                data: [

                    hostelAnalytics.mon,
                    hostelAnalytics.tue,
                    hostelAnalytics.wed,
                    hostelAnalytics.thu,
                    hostelAnalytics.fri,
                    hostelAnalytics.sat,
                    hostelAnalytics.sun

                ],
                borderColor: "#2563eb",
                backgroundColor: "rgba(37,99,235,0.1)",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true
        }
    });

});

function openProfileModal() {
    document.getElementById("profileModal").classList.add("show");
}

function closeProfileModal() {
    document.getElementById("profileModal").classList.remove("show");
}

function openLogoutModal() {

    document
        .getElementById("logoutModal")
        .classList.add("show");
}

function closeLogoutModal() {

    document
        .getElementById("logoutModal")
        .classList.remove("show");
}
document.getElementById("profileForm")
    .addEventListener("submit", function (e) {

        e.preventDefault();

        const formData = new FormData(this);

        fetch("/dashboard/update-profile/", {

            method: "POST",

            body: formData,

            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }

        })

            .then(async (res) => {

                const text = await res.text();

                try {

                    return JSON.parse(text);

                } catch (error) {

                    console.error("SERVER RESPONSE:", text);

                    alert("Django server error. Check terminal.");

                    throw error;
                }

            })

            .then(data => {

                if (data.success) {

                    location.reload();

                } else {

                    alert(data.message || "Update failed");

                }

            })

            .catch(error => {

                console.error(error);

            });

    });
document.querySelectorAll(".fill").forEach(fill => {

    let value = 0;

    if (fill.classList.contains("electric")) {
        value = hostelAnalytics.electricity;
    }

    else if (fill.classList.contains("water")) {
        value = hostelAnalytics.water;
    }

    else if (fill.classList.contains("maintenance")) {
        value = hostelAnalytics.maintenance;
    }
    fill.style.width = value + "%";

    // COLOR RULES
    if (value >= 70) {
        fill.style.backgroundColor = "#22c55e"; // GREEN
    }

    else if (value >= 40) {
        fill.style.backgroundColor = "#f59e0b"; // ORANGE
    }

    else {
        fill.style.backgroundColor = "#ef4444"; // RED
    }

});

/* =========================
   AUTO SCROLL CHAT
========================= */

const chatMessages = document.getElementById("chatMessages");

if (chatMessages) {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}

/* =========================
   FILE PREVIEW NAME
========================= */

const chatFile = document.getElementById("chatFile");

if (chatFile) {

    chatFile.addEventListener("change", function () {

        if (this.files.length > 0) {

            console.log(
                "Selected:",
                this.files[0].name
            );

        }

    });
}


/* =========================
VOICE RECORDER
========================= */

let mediaRecorder;

let audioChunks = [];

const recordBtn =
    document.getElementById("recordBtn");

const chatForm =
    document.querySelector(".chat-form");

if (recordBtn) {


    recordBtn.addEventListener(
        "click",
        async function () {

            // START RECORDING
            if (!mediaRecorder ||
                mediaRecorder.state === "inactive") {

                const stream =
                    await navigator.mediaDevices.getUserMedia({
                        audio: true
                    });

                mediaRecorder =
                    new MediaRecorder(stream);

                audioChunks = [];

                mediaRecorder.start();

                recordBtn.innerHTML =
                    '<i class="fa-solid fa-stop"></i>';

                mediaRecorder.addEventListener(
                    "dataavailable",
                    event => {

                        audioChunks.push(event.data);

                    }
                );

                mediaRecorder.addEventListener(
                    "stop",
                    () => {

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

                        chatForm.submit();
                    }
                );
            }

            // STOP RECORDING
            else {

                mediaRecorder.stop();

                recordBtn.innerHTML =
                    '<i class="fa-solid fa-microphone"></i>';
            }
        }
    );

}

function refreshDashboardData() {

    fetch("/student-dashboard-data/")

        .then(response => response.json())

        .then(data => {

            const hostel =
                document.getElementById("currentHostel");

            const room =
                document.getElementById("currentRoom");

            const status =
                document.getElementById("bookingStatus");

            const link =
                document.getElementById("hostelCardLink");

            if (hostel) {
                hostel.textContent =
                    data.current_hostel;
            }

            if (room) {
                room.textContent =
                    data.current_room || "N/A";
            }

            if (status) {
                status.textContent =
                    data.booking_status;
            }

            if (link) {
                link.href =
                    data.current_hostel_url;
            }

        })

        .catch(error => {

            console.log(error);

        });

}

/* check every 5 seconds */

setInterval(
    refreshDashboardData,
    5000
);

const searchInput =
    document.getElementById("dashboardSearch");

const searchResults =
    document.getElementById("searchResults");

if (searchInput) {

    searchInput.addEventListener(
        "input",
        function () {

            const query = this.value.trim();

            if (!query) {

                searchResults.innerHTML = "";
                return;
            }

            fetch(
                `/dashboard/search-hostels/?q=${query}`
            )

                .then(res => res.json())

                .then(data => {

                    searchResults.innerHTML = "";

                    data.results.forEach(item => {

                        searchResults.innerHTML += `
                        <a
                            href="${item.url}"
                            class="search-item"
                        >
                            <strong>${item.name}</strong>
                            <small>${item.type}</small>
                        </a>
                    `;

                    });

                });

        }
    );

}