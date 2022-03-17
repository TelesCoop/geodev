var navbar = document.getElementById("navbar");

function updateNavbarSuccinctStatus() {
    if (window.scrollY > 150) {
        navbar.classList.add("is-succinct");
    } else {
        navbar.classList.remove("is-succinct");
    }
}

window.addEventListener('scroll', updateNavbarSuccinctStatus);
