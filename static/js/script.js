// Theme Apply Function (page load hone par)
function loadTheme() {
    const themeLink = document.getElementById("theme-css");
    const icon = document.getElementById("icon");

    const savedTheme = localStorage.getItem("theme");
    const savedIcon = localStorage.getItem("icon");

    if (savedTheme && savedIcon) {
        themeLink.href = savedTheme;
        icon.src = savedIcon;
    }
}

// Theme Toggle Function
function toggleTheme() {
    const themeLink = document.getElementById("theme-css");
    const icon = document.getElementById("icon");

    let newTheme, newIcon;

    if (themeLink.href.includes("light.css")) {
        newTheme = "../static/css/dark.css";
        newIcon = "../static/images/sun.png";
    } else {
        newTheme = "../static/css/light.css";
        newIcon = "../static/images/moon.png";
    }

    themeLink.href = newTheme;
    icon.src = newIcon;

    // Save to localStorage
    localStorage.setItem("theme", newTheme);
    localStorage.setItem("icon", newIcon);
}

// Mobile Menu Toggle
function toggleMenu() {
    var nav = document.getElementById("navLinks");
    nav.classList.toggle("active");
}

// Page load hote hi saved theme apply karo
document.addEventListener("DOMContentLoaded", loadTheme);
