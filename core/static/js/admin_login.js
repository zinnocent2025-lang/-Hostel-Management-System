const adminPassword =
document.getElementById("adminPassword");

const togglePassword =
document.getElementById("togglePassword");

if (adminPassword && togglePassword) {

    togglePassword.addEventListener("click", () => {

        const icon =
        togglePassword.querySelector("i");

        if (adminPassword.type === "password") {

            // PASSWORD BECOMES VISIBLE
            adminPassword.type = "text";

            icon.className =
            "fa-solid fa-eye";

        } else {

            // PASSWORD BECOMES HIDDEN
            adminPassword.type = "password";

            icon.className =
            "fa-solid fa-eye-slash";
        }

    });

}