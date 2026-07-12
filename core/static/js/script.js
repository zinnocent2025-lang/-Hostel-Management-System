document.addEventListener("DOMContentLoaded", () => {



    const hamburger = document.getElementById("hamburger");
    const navlinks = document.getElementById("navLinks");
    const navoverlay = document.getElementById("navOverlay");

    if (hamburger && navlinks && navoverlay) {
        hamburger.addEventListener("click", () => {
            hamburger.classList.toggle("active");
            navlinks.classList.toggle("active");
            navoverlay.classList.toggle("active");
        });

        navoverlay.addEventListener("click", () => {
            hamburger.classList.remove("active");
            navlinks.classList.remove("active");
            navoverlay.classList.remove("active");
        });
    }



    /* =========================================
   LOGIN MODAL SYSTEM
========================================= */

    const loginBtn =
        document.getElementById("loginBtn");

    const loginModal =
        document.getElementById("loginModal");

    const closeLoginModal =
        document.getElementById("closeLoginModal");

    const studentLoginBtn =
        document.getElementById("studentLoginBtn");

    const adminLoginBtn =
        document.getElementById("adminLoginBtn");

    /* OPEN */

    if (loginBtn && loginModal) {

        loginBtn.addEventListener("click", (e) => {

            e.preventDefault();

            loginModal.classList.add("active");

        });

    }

    /* CLOSE BUTTON */

    if (closeLoginModal && loginModal) {

        closeLoginModal.addEventListener("click", () => {

            loginModal.classList.remove("active");

        });

    }

    /* CLICK OUTSIDE */

    if (loginModal) {

        loginModal.addEventListener("click", (e) => {

            if (e.target === loginModal) {

                loginModal.classList.remove("active");

            }

        });

    }

    /* STUDENT LOGIN */

    if (studentLoginBtn) {

        studentLoginBtn.addEventListener("click", () => {

            window.location.href = "/login/";

        });

    }

    /* ADMIN LOGIN */

    if (adminLoginBtn) {

        adminLoginBtn.addEventListener("click", () => {

            window.location.href = "/admin-login/";

        });

    }

});


/* =========================================
   HOSTEL MODAL SYSTEM
========================================= */

const viewHostelBtn =
    document.getElementById("viewHostelBtn");

const hostelModal =
    document.getElementById("hostelModal");

const maleHostel =
    document.getElementById("maleHostel");

const femaleHostel =
    document.getElementById("femaleHostel");

const closeHostelModal =
    document.getElementById("closeHostelModal");

/* OPEN MODAL */

if (viewHostelBtn && hostelModal) {

    viewHostelBtn.addEventListener("click", (e) => {

        e.preventDefault();

        hostelModal.classList.add("active");

    });

}

/* CLOSE MODAL */

if (closeHostelModal && hostelModal) {

    closeHostelModal.addEventListener("click", () => {

        hostelModal.classList.remove("active");

    });

}

/* CLICK OUTSIDE */

if (hostelModal) {

    hostelModal.addEventListener("click", (e) => {

        if (e.target === hostelModal) {

            hostelModal.classList.remove("active");

        }

    });

}

/* REDIRECTS */

if (maleHostel) {

    maleHostel.addEventListener("click", () => {

        window.location.href =
            "/male-hostel/";

    });

}

if (femaleHostel) {

    femaleHostel.addEventListener("click", () => {

        window.location.href =
            "/female-hostel/";

    });

}




/* =========================================
   ULTRA PREMIUM REPLAYABLE REVEAL
========================================= */

const reveals = document.querySelectorAll(
    ".reveal, .reveal-left, .reveal-right, .reveal-scale"
);

function revealOnScroll() {

    const windowHeight = window.innerHeight;

    reveals.forEach((element) => {

        const elementTop =
            element.getBoundingClientRect().top;

        const elementBottom =
            element.getBoundingClientRect().bottom;

        const revealPoint = 120;

        if (
            elementTop < windowHeight - revealPoint &&
            elementBottom > 80
        ) {

            element.classList.add("active");

        } else {

            element.classList.remove("active");

        }

    });

}

window.addEventListener("scroll", revealOnScroll);

revealOnScroll();
/* =========================================
   MOUSE PARALLAX
========================================= */

const hero = document.querySelector(".hero-right");

if (hero) {

    hero.addEventListener("mousemove", (e) => {

        const x =
            (window.innerWidth / 2 - e.pageX) / 40;

        const y =
            (window.innerHeight / 2 - e.pageY) / 40;

        hero.style.transform =
            `translate(${x}px, ${y}px)`;

    });

    hero.addEventListener("mouseleave", () => {

        hero.style.transform =
            `translate(0px, 0px) scale(1)`;

    });

}



/* =========================================
   PREMIUM NAVBAR MORPH
========================================= */

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 40) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});

/* =========================================
   SCROLL PROGRESS BAR
========================================= */

const scrollProgress =
    document.getElementById("scrollProgress");

window.addEventListener("scroll", () => {

    const scrollTop =
        window.scrollY;

    const docHeight =
        document.documentElement.scrollHeight
        - window.innerHeight;

    const progress =
        (scrollTop / docHeight) * 100;

    if (scrollProgress) {

        scrollProgress.style.width =
            `${progress}%`;

    }

});

/* =========================================
   PREMIUM LOADER
========================================= */

const loader =
    document.getElementById("loader");

window.addEventListener("load", () => {

    setTimeout(() => {

        if (loader) {

            loader.classList.add("hide");

        }

        document.body.classList.add("loaded");

    }, 2200);

});

/* =========================================
   LOADER COUNTER 0 - 100
========================================= */

const loaderPercent =
    document.getElementById("loaderPercent");

const loaderProgress =
    document.getElementById("loaderProgress");

let count = 0;

const loading = setInterval(() => {

    count++;

    if (loaderPercent) {

        loaderPercent.innerText =
            `${count}%`;

    }

    if (loaderProgress) {

        loaderProgress.style.width =
            `${count}%`;

    }

    if (count >= 100) {

        clearInterval(loading);

    }

}, 20);



/* =========================================
   NAVBAR SCROLL EFFECT
========================================= */

window.addEventListener("scroll", () => {

    const navbar =
        document.querySelector(".navbar");

    if (!navbar) return;

    if (window.scrollY > 40) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});

document.addEventListener("keydown", function (e) {

    if (
        e.ctrlKey &&
        // e.shiftKey &&
        e.key.toLowerCase() === "i"
    ) {

       window.location.href ="/control-room-7392/";

    }

});

