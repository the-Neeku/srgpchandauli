document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("toggleButton");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function() {
            this.classList.toggle("horizontal");
            document.getElementById("noticeBoard").classList.toggle("show-notice");
        });
    }
});