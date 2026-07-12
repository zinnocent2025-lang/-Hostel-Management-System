// ===============================
// ELEMENTS
// ===============================
const form = document.querySelector("form");
const btn = document.getElementById("registerBtn");
const overlay = document.getElementById("successOverlay");

const emailInput = document.getElementById("emailInput");
const passwordInput = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

const fullName = document.getElementById("fullName");
const phone = document.getElementById("phoneInput");
const gender = document.getElementById("genderInput");

const strengthFill = document.getElementById("strengthFill");

// ===============================
// FORM STATE
// ===============================
let formState = {
    fullName: false,
    email: false,
    phone: false,
    gender: false,
    password: false,
    confirm: false
};

// ===============================
// EMAIL CHECK (AJAX)
// ===============================
let emailTimer = null;

emailInput.addEventListener("input", () => {

    emailInput.classList.remove("valid", "invalid");

    clearTimeout(emailTimer);

    emailTimer = setTimeout(() => {

        const email = emailInput.value;
        if (!email) return;

        emailInput.classList.add("loading");

        fetch(`/check-email/?email=${email}`)
            .then(res => res.json())
            .then(data => {

                emailInput.classList.remove("loading");

                if (data.exists) {
                    showError(emailInput, "Email already exists");
                    formState.email = false;
                } else {
                    clearError(emailInput);
                    emailInput.classList.add("valid");
                    formState.email = true;
                }

                checkFormValidity();
            });

    }, 500);
});

// ===============================
// PASSWORD STRENGTH
// ===============================
passwordInput.addEventListener("input", () => {

    const value = passwordInput.value;
    let strength = 0;

    if (value.length >= 6) strength++;
    if (/[A-Z]/.test(value)) strength++;
    if (/[0-9]/.test(value)) strength++;
    if (/[^A-Za-z0-9]/.test(value)) strength++;

    strengthFill.className = "";

    if (strength <= 1) {
        strengthFill.classList.add("weak");
        passwordInput.classList.add("invalid");
        passwordInput.classList.remove("valid");
        formState.password = false;

    } else if (strength === 2 || strength === 3) {
        strengthFill.classList.add("medium");
        passwordInput.classList.remove("invalid");
        passwordInput.classList.remove("valid");
        formState.password = false;

    } else {
        strengthFill.classList.add("strong");
        passwordInput.classList.add("valid");
        passwordInput.classList.remove("invalid");
        formState.password = true;
    }

    checkFormValidity();
});

// ===============================
// CONFIRM PASSWORD
// ===============================
confirmPassword.addEventListener("input", () => {

    if (confirmPassword.value !== passwordInput.value) {
        showError(confirmPassword, "Passwords do not match");
        formState.confirm = false;
    } else {
        clearError(confirmPassword);
        confirmPassword.classList.add("valid");
        formState.confirm = true;
    }

    checkFormValidity();
});

// ===============================
// FULL NAME
// ===============================
fullName.addEventListener("input", () => {

    if (fullName.value.trim().length > 2) {
        fullName.classList.add("valid");
        fullName.classList.remove("invalid");
        formState.fullName = true;
    } else {
        fullName.classList.add("invalid");
        formState.fullName = false;
    }

    checkFormValidity();
});

// ===============================
// PHONE
// ===============================
phone.addEventListener("input", () => {

    if (/^\d{10,11}$/.test(phone.value)) {
        phone.classList.add("valid");
        phone.classList.remove("invalid");
        formState.phone = true;
    } else {
        phone.classList.add("invalid");
        formState.phone = false;
    }

    checkFormValidity();
});

// ===============================
// GENDER
// ===============================
gender.addEventListener("change", () => {

    if (gender.value) {
        gender.classList.add("valid");
        gender.classList.remove("invalid");
        formState.gender = true;
    } else {
        gender.classList.add("invalid");
        formState.gender = false;
    }

    checkFormValidity();
});

// ===============================
// PASSWORD TOGGLE (EYE)
// ===============================
const toggles = document.querySelectorAll(".toggle-password");

toggles.forEach(icon => {

    icon.addEventListener("click", () => {

        const inputId = icon.getAttribute("data-target");
        const input = document.getElementById(inputId);

        if (input.type === "password") {
            input.type = "text";
            icon.classList.replace("fa-eye-slash", "fa-eye");
        } else {
            input.type = "password";
            icon.classList.replace("fa-eye", "fa-eye-slash");
        }

    });

});

// ===============================
// ENABLE / DISABLE BUTTON
// ===============================
const registerBtn = document.getElementById("registerBtn");

function checkFormValidity() {

    const allValid = Object.values(formState).every(v => v === true);

    if (allValid) {
        registerBtn.disabled = false;
        registerBtn.style.opacity = "1";
    } else {
        registerBtn.disabled = true;
        registerBtn.style.opacity = "0.6";
    }
}

// disable initially
registerBtn.disabled = true;

// ===============================
// SUBMIT (AJAX)
// ===============================
form.addEventListener("submit", function (e) {

    e.preventDefault();

    const allValid = Object.values(formState).every(v => v === true);

    if (!allValid) {
        form.classList.add("shake");

        setTimeout(() => {
            form.classList.remove("shake");
        }, 400);

        return;
    }

    btn.classList.add("loading");

    const formData = new FormData(form);

    const csrfToken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken
        }
    })
    .then(res => res.json())
    .then(data => {

        btn.classList.remove("loading");

        if (data.success) {

            overlay.classList.add("show");

            setTimeout(() => {
                window.location.href = data.redirect_url;
            }, 2500);

        } else {

            form.classList.add("shake");

            setTimeout(() => {
                form.classList.remove("shake");
            }, 400);

            alert(data.message);
        }

    })
    .catch(() => {
        btn.classList.remove("loading");
        alert("Something went wrong");
    });

});
function showError(input, message) {
    const group = input.closest(".input-group");
    const error = group.querySelector(".error-text");

    error.innerText = message;
    error.classList.add("show");

    input.classList.add("invalid");
}

function clearError(input) {
    const group = input.closest(".input-group");
    const error = group.querySelector(".error-text");

    error.innerText = "";
    error.classList.remove("show");

    input.classList.remove("invalid");
}

document.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", () => {
        clearError(input);
    });
});