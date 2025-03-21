const address = "10.233.4.34"
document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.querySelector(".chat-input");
    const chatBody = document.querySelector(".chat-body");

    // Handle "Enter" key press to send message
    chatInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && chatInput.value.trim() !== "") {
            event.preventDefault(); // Prevent new line
            sendMessage(chatInput.value.trim()); // Send message
        }
    });

    function sendMessage(message) {
        // Create user's message div
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.textContent = message;
        chatBody.appendChild(userMessage);

        // Clear input field
        chatInput.value = "";
        chatBody.scrollTop = chatBody.scrollHeight;

        // Show typing animation
        const typingIndicator = document.createElement("div");
        typingIndicator.classList.add("bot-message", "typing-indicator");
        typingIndicator.innerHTML = "<span>.</span><span>.</span><span>.</span>";
        chatBody.appendChild(typingIndicator);
        chatBody.scrollTop = chatBody.scrollHeight;

        // JSON request data
        const requestData = JSON.stringify({ prompt: message });
        console.log("JSON Request:", requestData);

        // Send message to API
        fetch("http://" + address + ":11434/api/chat", { // Replace with actual API URL
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: requestData
        })
        .then(response => response.json())
        .then(data => {
            chatBody.removeChild(typingIndicator); // Remove typing animation

            console.log("API Response:", data);

            // Extract bot response and format it for display
            let botResponse = data.response || "Sorry, I couldn't process that.";

            // Convert newlines to HTML line breaks for a formatted display
            botResponse = botResponse.replace(/\n/g, '<br>');

            // Create bot's message div
            const botReply = document.createElement("div");
            botReply.classList.add("bot-message");
            botReply.innerHTML = botResponse; // Use innerHTML to preserve formatting
            chatBody.appendChild(botReply);
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            chatBody.removeChild(typingIndicator); // Remove typing animation

            console.error("Error:", error);

            const botReply = document.createElement("div");
            botReply.classList.add("bot-message");
            botReply.textContent = "Error communicating with the server.";
            chatBody.appendChild(botReply);
            chatBody.scrollTop = chatBody.scrollHeight;
        });
    }
}); 