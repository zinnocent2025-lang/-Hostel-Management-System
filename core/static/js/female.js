const toggle = document.getElementById("themeToggle");
const body = document.body;
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

/* ===== Load saved theme ===== */
if (localStorage.getItem("theme") === "light") {
  body.classList.add("light-mode");
  toggle.textContent = "";
} else {
  toggle.textContent = "";
}

/* ===== Toggle Theme ===== */
toggle.addEventListener("click", () => {
  body.classList.toggle("light-mode");

  if (body.classList.contains("light-mode")) {
    localStorage.setItem("theme", "light");
    toggle.textContent = "";
  } else {
    localStorage.setItem("theme", "dark");
    toggle.textContent = "";
  }
});

/* ===== Mobile Menu ===== */
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
  hamburger.classList.toggle("active");
});

/* ===== Pages Dropdown ===== */

const pagesToggle = document.getElementById("pagesToggle");
const pagesDropdown = document.getElementById("pagesDropdown");

if (pagesToggle) {
  pagesToggle.addEventListener("click", function (e) {
    e.preventDefault();
    pagesDropdown.classList.toggle("show");
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".pages-menu")) {
      pagesDropdown.classList.remove("show");
    }
  });
}

/* ===== MORE DETAILS MODAL ===== */

const moreBtn = document.querySelector(".more-btn");

if (moreBtn) {
  moreBtn.addEventListener("click", () => {

    const overlay = document.createElement("div");
    overlay.classList.add("modal-overlay");

    const modal = document.createElement("div");
    modal.classList.add("modal-box");

    modal.innerHTML = `
      <h2>About Jobitech Hostel</h2>
      <p>Jobitech Hostel provides a secure, student-focused accommodation environment with modern amenities.</p>

      <ul class="modal-list">
        <li>
        <i class="fas fa-book-reader"></i>
        <strong>Study & Recreation:</strong> Dedicated study halls, library corner and recreational lounge.
        </li>

        <li>
        <i class="fas fa-soap"></i>
        <strong>Health & Hygiene:</strong> Laundry services, daily cleaning and sanitation facilities.
        </li>

        <li>
        <i class="fas fa-users"></i>
        <strong>Events & Community:</strong> Student meetups, workshops and cultural activities.
        </li>

        <li>
        <i class="fas fa-shield-alt"></i>
        <strong>24/7 Security & Staff:</strong> CCTV coverage, guards and hostel caretakers.
        </li>
      </ul>

      <button id="closeModal">Close</button>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    const closeBtn = document.getElementById("closeModal");

    closeBtn.addEventListener("click", () => overlay.remove());

    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) overlay.remove();
    });
  });
}
// FAQ Toggle
const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach(item => {
  const question = item.querySelector(".faq-question");
  question.addEventListener("click", () => {
    item.classList.toggle("active");

    // Close other items
    faqItems.forEach(other => {
      if (other !== item) other.classList.remove("active");
    });
  });
});

// ROOM AVAILABILITY ANIMATION
const roomCards = document.querySelectorAll('.room-card');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // Animate only once
    }
  });
}, { threshold: 0.1 });

roomCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 0.1}s`; // Staggered entrance
  observer.observe(card);
});
// FACILITY CARDS ANIMATION
const facilityCards = document.querySelectorAll('.facility-card');

const facilityObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      facilityObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

facilityCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 0.15}s`; // stagger
  facilityObserver.observe(card);
});
// SERVICE CARDS ANIMATION
const serviceCards = document.querySelectorAll('.service-card');

const serviceObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      serviceObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

serviceCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 0.15}s`; // stagger entrance
  serviceObserver.observe(card);
});

document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('.animate-on-scroll');

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // stop observing after animation
      }
    });
  }, { threshold: 0.15 }); // trigger when 15% of section is visible

  elements.forEach(el => observer.observe(el));
});
const elements = document.querySelectorAll(
  ".about-left, .about-right, .how-column.left, .how-column.right, .how-center, .team-card, .testimonial-card"
);

const observe = new IntersectionObserver((entries) => {
  entries.forEach(entry => {

    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    } else {
      entry.target.classList.remove("visible"); // allows replay
    }

  });
}, {
  threshold: 0.25
});

elements.forEach(el => observe.observe(el));

const slider = document.getElementById("heroSlider");
const prevBtn = document.querySelector(".hero-prev");
const nextBtn = document.querySelector(".hero-next");

const slides = document.querySelectorAll("#heroSlider img");
const totalImages = slides.length;

let index = 0;

function updateSlide() {
  slider.style.transform = `translateX(-${index * 100}%)`;
}

nextBtn.addEventListener("click", () => {
  index = (index + 1) % totalImages;
  updateSlide();
});

prevBtn.addEventListener("click", () => {
  index = (index - 1 + totalImages) % totalImages;
  updateSlide();
});

setInterval(() => {
  index++;

  if (index >= totalImages) {
    index = 0;
  }

  updateSlide();
}, 7000);

const paymentBtn = document.getElementById("paymentBtn");
const paymentModal = document.getElementById("paymentModal");
const closePayment = document.getElementById("closePayment");

if (paymentBtn) {

  paymentBtn.addEventListener("click", () => {

    paymentModal.style.display = "flex";

  });

}

if (closePayment) {

  closePayment.addEventListener("click", () => {

    paymentModal.style.display = "none";

  });

}

window.addEventListener("click", (e) => {

  if (e.target === paymentModal) {

    paymentModal.style.display = "none";

  }

});

/* ===========================
   ROOM WEBSOCKET
=========================== */

const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

const roomSocket = new WebSocket(

  protocol +
  window.location.host +
  "/ws/rooms/"

);

roomSocket.onopen = function () {

  console.log("Connected to Room Server");

};

roomSocket.onclose = function () {

  console.log("Room Server Disconnected");

};

roomSocket.onerror = function (error) {

  console.error("WebSocket Error:", error);

};

roomSocket.onmessage = function (event) {

  const data = JSON.parse(event.data);
  if (data.room_type !== "FemaleRoom") {
    return;
  }

  console.log("Live Update:", data);

  const card = document.getElementById(`room-${data.room_id}`);

  if (!card) return;

  // =========================
  // STATUS BADGE
  // =========================

  const status = card.querySelector(".room-status");

  status.textContent =
    data.status.charAt(0).toUpperCase() +
    data.status.slice(1);

  status.className =
    "availability room-status " + data.status;

  // =========================
  // PROGRESS BAR
  // =========================

  const progress = card.querySelector(".room-progress");

  progress.style.width = data.progress + "%";

  // Remove previous color classes
  progress.classList.remove(
    "low",
    "mid-low",
    "medium",
    "high",
    "full"
  );

  // Add the correct one
  if (data.progress >= 100) {

    progress.classList.add("full");

  }
  else if (data.progress >= 75) {

    progress.classList.add("high");

  }
  else if (data.progress >= 50) {

    progress.classList.add("medium");

  }
  else if (data.progress >= 25) {

    progress.classList.add("mid-low");

  }
  else {

    progress.classList.add("low");

  }

  // =========================
  // OCCUPANCY TEXT
  // =========================

  const capacityText =
    card.querySelector(".room-capacity small:first-child");

  capacityText.textContent =
    `${data.occupied_beds}/${data.capacity} Beds Occupied`;

  // =========================
  // REMAINING BEDS
  // =========================

  const remaining =
    card.querySelector(".remaining-beds");

  if (data.status === "full") {

    remaining.textContent = "Room Full";

  }

  else if (data.remaining_beds === 1) {

    remaining.textContent = "1 Bed Left";

  }

  else {

    remaining.textContent =
      `${data.remaining_beds} Beds Left`;

  }

};