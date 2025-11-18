//console.log("Frontend loaded successfully!");
// Main JavaScript for Student Placement System

document.addEventListener("DOMContentLoaded", () => {
    console.log("Frontend loaded successfully!");

    // Mobile menu toggle (for responsive navbar)
    const menuBtn = document.querySelector(".menu-btn");
    const navLinks = document.querySelector(".nav-links");

    if (menuBtn) {
        menuBtn.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });
    }
});

