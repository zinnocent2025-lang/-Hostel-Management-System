const paymentForm = document.getElementById("paymentForm");

const detailsScreen = document.getElementById("detailsScreen");

const cardScreen =
    document.getElementById("cardScreen");

const processingScreen =
    document.getElementById("processingScreen");

const payNow =
    document.getElementById("payNow");

const processingText =
    document.getElementById("processingText");
const successScreen =
    document.getElementById("successScreen");

const transactionId =
    document.getElementById("transactionId");

const referenceId = document.getElementById("referenceId");

const transferReference =
    document.getElementById("transferReference");

const copyAccount = document.getElementById("copyAccount");
const continueBtn = document.getElementById("continueBtn");

const instructionModal = document.getElementById("instructionModal");

const closeInstruction = document.getElementById("closeInstruction");
transferReference.innerHTML =
    "HMS-DEMO-" +
    Math.floor(100000 + Math.random() * 900000);
paymentForm.addEventListener("submit", function (e) {

    e.preventDefault();

    detailsScreen.style.display = "none";

    cardScreen.style.display = "block";

});


payNow.addEventListener("click", function () {

    cardScreen.style.display = "none";
    processingScreen.style.display = "block";

    processingText.innerHTML = "Connecting to payment gateway...";

    setTimeout(function () {
        processingText.innerHTML = "Encrypting payment details...";
    }, 2000);

    setTimeout(function () {
        processingText.innerHTML = "Authorizing transaction...";
    }, 4000);

    setTimeout(function () {

        processingScreen.style.display = "none";
        successScreen.style.display = "block";

        transactionId.innerHTML =
            "FLW-" + Math.floor(Math.random() * 900000000);

        referenceId.innerHTML =
            "HMS-" + Math.floor(Math.random() * 900000);

    }, 6000);

});

copyAccount.addEventListener("click", function(){

    navigator.clipboard.writeText("0123456789");

    this.innerHTML =
    '<i class="fa fa-check"></i> Copied';

});

continueBtn.addEventListener("click", function(){

    instructionModal.style.display = "flex";

});

closeInstruction.addEventListener("click", function(){

    instructionModal.style.display = "none";

});