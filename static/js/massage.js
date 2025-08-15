  // Message 5 seconds (5000 milliseconds) ke baad hide ho jaye
  setTimeout(function () {
    var messageBox = document.getElementById("message-container");
    if (messageBox) {
      messageBox.style.display = "none";
    }
  }, 5000); // 5000 = 5 seconds