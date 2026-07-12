// ==========================
// PAGE FADE-IN
// ==========================

window.addEventListener("load", () => {

    document.body.classList.add("loaded");

});


// ==========================
// BUTTON LOADING EFFECT
// ==========================

const bookingForm = document.querySelector("form");

const bookBtn = document.querySelector(".book-btn");

if (bookingForm) {

    bookingForm.addEventListener("submit", () => {

        bookBtn.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin"></i>
            Reserving Room...
        `;

        bookBtn.disabled = true;

    });

}


// ==========================
// GLASS HOVER EFFECT
// ==========================

const glassCards = document.querySelectorAll(
    ".glass-card, .summary-card"
);

glassCards.forEach(card => {

    card.addEventListener("mousemove", (e) => {

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;

        const y = e.clientY - rect.top;

        card.style.background = `
            radial-gradient(
                circle at ${x}px ${y}px,
                rgba(255,255,255,0.18),
                rgba(255,255,255,0.10)
            )
        `;

    });

    card.addEventListener("mouseleave", () => {

        card.style.background =
        "rgba(255,255,255,0.12)";

    });

});