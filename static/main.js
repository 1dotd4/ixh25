var socket = io();
var username = prompt("Enter your name:");  // Ask for username
socket.emit("join", username);  // Notify server of new user

var training = 0;

// Listen for messages from server
socket.on("message", function(message) {
    console.log(message);
    data = JSON.parse(message);
    let messages = document.getElementById("messages");
    messages.innerHTML = `<p>${data.username}: ${data.message}</p>` + messages.innerHTML;
});

// Function to send messages
function sendMessage(action) {
    // var msgInput = document.getElementById("msg");
    // var message = msgInput.value;
    let status = document.getElementById("action");
    
    if (action === 'buy') {
	let buybutton = document.getElementById("buy");
	buybutton.disabled = true;
	buybutton.className = "disabled";
	status.innerHTML = "You bought a car";
    } else if (action === 'race') {
	status.innerHTML = "You are racing";
    } else if (action === 'train') {
	training += 1;
	status.innerHTML = `You are training (${training})`;
    }
    data = {
	action: action,
    };
    message = JSON.stringify(data);
    socket.send(message);
   //  msgInput.value = "";
}
