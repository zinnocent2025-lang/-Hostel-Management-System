document.addEventListener("DOMContentLoaded", function () {

    // ================= MENU TOGGLE =================
    const menuBtn = document.getElementById("menuBtn");
    const menuDropdown = document.getElementById("menuDropdown");

    if (menuBtn && menuDropdown) {
        menuBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            menuDropdown.classList.toggle("show");
        });
    }

    document.addEventListener("click", function () {
        if (menuDropdown) {
            menuDropdown.classList.remove("show");
        }
    });

    // ================= CLOSE MENU WHEN CLICK OUTSIDE =================
    document.addEventListener("click", function () {
        if (menuDropdown) {
            menuDropdown.classList.remove("show");
        }
    });

    // ================= FILTER SYSTEM =================
    const rows = document.querySelectorAll("tbody tr");

    function filterRows(status) {
        rows.forEach(row => {
            if (status === "all" || row.dataset.status === status) {
                row.style.display = "table-row";
            } else {
                row.style.display = "none";
            }
        });
    }

    // ================= MENU BUTTONS =================
    const pendingBtn = document.getElementById("showPending");
    const approvedBtn = document.getElementById("showApproved");
    const rejectedBtn = document.getElementById("showRejected");
    const allBtn = document.getElementById("showAll");

    if (pendingBtn) {
        pendingBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            filterRows("pending");
        });
    }

    if (approvedBtn) {
        approvedBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            filterRows("approved");
        });
    }

    if (rejectedBtn) {
        rejectedBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            filterRows("rejected");
        });
    }

    if (allBtn) {
        allBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            filterRows("all");
        });
    }

});

function updateStatus(id, type, status) {
    console.log(id);
    console.log(type);
    console.log(status);


    fetch(`/dashboard/update-booking/${id}/`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body: JSON.stringify({
            status: status,
            booking_type: type
        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.success){

            const row =
                document.querySelector(
                    `[data-booking-id="${type}-${id}"]`
                );

            if(row){

                row.dataset.status = status;

                const badge =
                    row.querySelector(".status");

                badge.innerText = status;

                badge.className =
                    `status ${status}`;
            }
        }

    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================
// SEARCH BOOKINGS
// ============================

const bookingSearch =
    document.getElementById("bookingSearch");

if (bookingSearch) {

    bookingSearch.addEventListener(
        "keyup",

        function () {

            const value =
                this.value.toLowerCase();

            document
                .querySelectorAll("tbody tr")

                .forEach(row => {

                    const text =
                        row.innerText.toLowerCase();

                    row.style.display =
                        text.includes(value)
                            ? ""
                            : "none";

                });

        }

    );

}

// ============================
// HOSTEL FILTERS
// ============================

const filterBtns =
    document.querySelectorAll(".filter-btn");

filterBtns.forEach(btn => {

    btn.addEventListener(
        "click",

        function () {

            filterBtns.forEach(
                b => b.classList.remove("active")
            );

            this.classList.add("active");

            const filter =
                this.dataset.filter;

            document
                .querySelectorAll("tbody tr")

                .forEach(row => {

                    if (
                        filter === "all"
                    ) {
                        row.style.display = "";
                        return;
                    }

                    const hostel =
                        row.dataset.hostel;

                    row.style.display =
                        hostel === filter
                            ? ""
                            : "none";

                });

        }

    );

});