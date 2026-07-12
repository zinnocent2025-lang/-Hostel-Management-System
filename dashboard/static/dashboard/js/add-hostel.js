document.addEventListener("DOMContentLoaded", () => {

const fileInput = document.querySelector('input[type="file"]');
const submitBtn = document.querySelector("button");
const form = document.querySelector("form");

/* Image Preview */
if(fileInput){

    const preview = document.createElement("img");
    preview.style.width = "100%";
    preview.style.height = "220px";
    preview.style.objectFit = "cover";
    preview.style.borderRadius = "14px";
    preview.style.marginTop = "12px";
    preview.style.display = "none";

    fileInput.parentElement.appendChild(preview);

    fileInput.addEventListener("change", function(){

        const file = this.files[0];

        if(file){
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        }
    });
}


/* Submit Animation */
form.addEventListener("submit", () => {

    submitBtn.innerHTML = "Adding Hostel...";
    submitBtn.style.opacity = "0.8";
    submitBtn.disabled = true;

});


/* Input Hover Effect */
document.querySelectorAll("input, textarea").forEach(input => {

    input.addEventListener("focus", () => {
        input.style.transform = "scale(1.01)";
    });

    input.addEventListener("blur", () => {
        input.style.transform = "scale(1)";
    });

});

});