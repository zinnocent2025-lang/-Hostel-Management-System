// page loadMoreBtn(real load detection)
window.addEventListener("load", function () {
  const loader = document.getElementById("pageLoader");
  loader.classList.add("fade-out");
  document.body.classList.add("reveal");
});

// ===============================
// SETTINGS
// ===============================
let currentIndex = 0;
const hostelsPerLoad = 6; // loads 6 at a time

// ===============================
// ELEMENTS
// ===============================
const hostelList = document.querySelector(".hostel-list");
const loadMoreBtn = document.getElementById("loadMoreBtn");
const gearIcon = document.getElementById("gearIcon");

const body = document.body;

const isAuthenticated =
  body.dataset.authenticated === "True";

const bookingStatus =
  body.dataset.bookingStatus;

const bookedRoomId = body.dataset.bookedRoom;
console.log(bookingStatus, bookedRoomId);

// Modal elements

const insideImg = document.getElementById("insideImg");

// Your single inside image (change this to your file name)
const insideImageFile = "/static/images/inside.jfif";


// ===============================
// FUNCTION TO CREATE HOSTEL CARD
// ===============================
function createHostelCard(hostel) {
  const card = document.createElement("div");
  card.classList.add("hostel-card");

  card.innerHTML = `
    <img src="${hostel.image}">

    <div class="hostel-info">
        <h3>${hostel.name}</h3>

        <p class="location">
            <i class="fa-solid fa-location-dot"></i>
            ${hostel.location}
        </p>

        <p class="desc">
    Affordable and secure hostel with good amenities.
</p>

<p class="hostel-hidden-type" style="display:none;">
    ${hostel.hostel_type}
</p>

<p class="price">${hostel.price}</p>

        <button 
class="details-btn"

data-rooms='${JSON.stringify(hostel.rooms)}'

>

View Details

</button>
    </div>
`;

  // add click event to view button


  return card;
}

function openModal(imageSrc) {
  const insideImg = document.getElementById("insideImg");
  insideImg.src = imageSrc;   //  IMPORTANT
  viewModal.classList.add("show");
}

// ===============================
// MODAL CLOSE FUNCTION
// ===============================
function closeModalFunc() {
  viewModal.classList.remove("show");
}


// ===============================
// LOAD MORE BUTTON EVENT
// ===============================

function spinGear(event) {
  event.preventDefault();

  const gear = document.getElementById("gearIcon");
  gear.classList.add("spin");

  setTimeout(() => {
    window.location.href = event.currentTarget.href;
  }, 600);
}



let currentPage = 1;

loadMoreBtn.addEventListener("click", () => {
  currentPage++;

  gearIcon.classList.add("spin");

  fetch(`/load-more-hostels/?page=${currentPage}`)
    .then(response => response.json())
    .then(data => {

      data.hostels.forEach(hostel => {
        const card = createHostelCard(hostel);
        hostelList.appendChild(card);
      });

      reAttach(); // VERY IMPORTANT

      // reattach View Details buttons for new cards
      attachDetailsButtons();

      gearIcon.classList.remove("spin");

      if (!data.has_next) {
        loadMoreBtn.innerHTML = "No More Hostels";
        loadMoreBtn.disabled = true;
      }

    })
    .catch(error => {
      console.log("Error loading hostels:", error);
      gearIcon.classList.remove("spin");
    });
});
// ===============================
// DETAILS VIEW LOGIC
// ===============================

const detailsSection = document.getElementById("hostelDetails");
const backBtn = document.getElementById("backBtn");
const pageHeader = document.querySelector(".page-header");
const loadMoreSection = document.querySelector(".load-more-container");

const hostelLocations = {
  "Blessed Home Lodge": [6.1498, 6.7857],
  "Divine Hostel": [6.1510, 6.7890],
  "Peace Lodge": [6.1475, 6.7832],
  "Victory Hostel": [6.1530, 6.7810],
  "Royal Palace Hostel": [6.1552, 6.7904]
};
// attach click to all buttons
function attachDetailsButtons() {
  const buttons = document.querySelectorAll(".details-btn");

  buttons.forEach((btn, index) => {
    btn.addEventListener("click", () => {

      const card = btn.closest(".hostel-card");

      const name = card.querySelector("h3").innerText;
      const location = card.querySelector(".location").innerText;
      const hostelTypeElement = card.querySelector(".hostel-hidden-type") || card.querySelector(".hostel-badge");
      const hostelType = hostelTypeElement ? hostelTypeElement.innerText : "Hostel";
      const capacity = btn.dataset.capacity;
      const totalRooms = btn.dataset.totalrooms;
      // const price = card.querySelector(".price").innerText;
      const insideImage = "/static/images/inside.jfif";

      document.getElementById("detailImage").src = insideImage;


      // fill details
      document.getElementById("detailName").innerText = name;
      document.getElementById("detailLocation").innerText = location;
      document.getElementById("detailType").innerText = hostelType;
      document.getElementById("detailDescription").innerText = "Affordable and secure hostel with good facilities and easy access to school.";
      const rooms = JSON.parse(btn.dataset.rooms);
      

      const roomsContainer = document.getElementById("roomsContainer");

      roomsContainer.innerHTML = "";

      if (rooms.length === 0) {

        roomsContainer.innerHTML = `
  
    <div class="no-room">
        No rooms available.
    </div>

  `;

      } else {

        rooms.forEach(room => {

          let buttonHTML = "";

          if (!isAuthenticated) {

            buttonHTML = `
        <a href="/register/" class="book-btn">
            Register to Book
        </a>
    `;
          }

          // EXPIRED → ALLOW SAME ROOM ONLY
          else if (
            bookingStatus === "expired" &&
            bookedRoomId == room.id
          ) {

            buttonHTML = `
        <a href="/external-booking/${room.id}/"
           class="book-btn">
           Rebook
        </a>
    `;
          }

          // EXPIRED → BLOCK OTHER ROOMS
          else if (
            bookingStatus === "expired"
          ) {

            buttonHTML = `
        <span class="occupied-btn">
            Rebook Original Room
        </span>
    `;
          }

          // ACTIVE BOOKING
          else if (
            bookingStatus === "pending" ||
            bookingStatus === "approved"
          ) {

            buttonHTML = `
        <span class="occupied-btn">
            Booking Exists
        </span>
    `;
          }

          // ROOM OCCUPIED
          else if (
            room.status === "occupied"
          ) {

            buttonHTML = `
        <span class="occupied-btn">
            Occupied
        </span>
    `;
          }

          else if (
            bookingStatus === "expired"
          ) {

            buttonHTML = `
        <span class="occupied-btn">
            Rebook Original Room
        </span>
    `;
          }

          else {

            buttonHTML = `
        <a href="/external-booking/${room.id}/"
           class="book-btn">
           Book Now
        </a>
    `;
          }


          roomsContainer.innerHTML += `

      <div class="room-box">

          <div class="room-left">

              <h4>${room.number}</h4>

              <p>
                  ${room.type}
                  • Capacity ${room.capacity}
              </p>

          </div>

          <div class="room-center">

              <span class="room-price">
                  ₦${room.price} / year
              </span>

          </div>

          <div class="room-right">

              ${buttonHTML}

          </div>

      </div>

    `;
        });
      }

      const owners = [
        "Mr. Chukwudi",
        "Mrs. Adaeze",
        "Mr. Emeka",
        "Mrs. Ifeoma",
        "Mr. Obinna"
      ];

      document.getElementById("detailOwner").innerText =
        owners[Math.floor(Math.random() * owners.length)];
      // switch view

      hostelList.style.display = "none";
      detailsSection.style.display = "block";

      pageHeader.style.display = "none";
      loadMoreSection.style.display = "none";

      const coords = hostelLocations[name] || [6.1498, 6.7857];

      setTimeout(() => {
        loadMap(coords[0], coords[1], name);
      }, 300);

      window.scrollTo(0, 0);


      window.scrollTo(0, 0);
    });
  });
}

// run on load
window.addEventListener("DOMContentLoaded", attachDetailsButtons);

// also run after load more
function reAttach() {
  attachDetailsButtons();
}

backBtn.addEventListener("click", () => {
  detailsSection.style.display = "none";
  hostelList.style.display = "grid";

  pageHeader.style.display = "block";
  loadMoreSection.style.display = "block";

  window.scrollTo(0, 0);
});


let map = null;

function loadMap(lat, lng, hostelName) {

  if (map) {
    map.remove();
  }

  map = L.map('map').setView([lat, lng], 16);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map);

  L.marker([lat, lng]).addTo(map)
    .bindPopup(hostelName)
    .openPopup();

  setTimeout(() => {
    map.invalidateSize();
  }, 300);
}