var socket = io();
var username = prompt("Enter your name:");  // Ask for username
socket.emit("join", username);  // Notify server of new user

// Listen for messages from server
socket.on("message", function(data) {
    var messages = document.getElementById("messages");
    messages.innerHTML = `<p>${data}</p>` + messages.innerHTML;
});

// Function to send messages
function sendMessage(message) {
    // var msgInput = document.getElementById("msg");
    // var message = msgInput.value;
    if (message === 'buy') {
	let buybutton = document.getElementById("buy");
	buybutton.className = "disabled";
    }
    socket.send(message);
    msgInput.value = "";
}
