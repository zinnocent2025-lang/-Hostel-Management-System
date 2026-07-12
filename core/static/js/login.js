const password = document.getElementById("password");
const toggle = document.getElementById("togglePassword");

toggle.addEventListener("click", function () {

    const icon = toggle.querySelector("i");

    if (password.type === "password") {
        password.type = "text";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    } else {
        password.type = "password";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    }

});

const logoutBtn = document.getElementById("logoutBtn");
const logoutForm = document.getElementById("logoutForm");

logoutBtn.addEventListener("click", function () {

    const confirmLogout = confirm("Are you sure you want to logout?");

    if (confirmLogout) {
        logoutForm.submit();
    }

});