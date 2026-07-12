const form = document.querySelector(".contact-form");
const button = document.querySelector(".btn-primary");
const plane = document.getElementById("planeAnimation");
const successState = document.getElementById("successState");
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

form.addEventListener("submit", function (e) {
    e.preventDefault();

    // button loading
    button.innerHTML = "Sending...";
    button.disabled = true;

    const formData = new FormData(form);

    fetch("/contact/", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCSRFToken()
        }
    })
        .then(res => res.json())
        .then(data => {

            button.innerHTML = "Send Message";
            button.disabled = false;

            if (data.success) {

                // ✈️ START ANIMATION
                plane.classList.add("fly");

                setTimeout(() => {
                    form.style.display = "none";
                    successState.classList.add("show");
                }, 1000);

            } else {
                alert(data.message || "Something went wrong");
            }

        })
        .catch(() => {
            button.innerHTML = "Send Message";
            button.disabled = false;
            alert("Network error");
        });
});