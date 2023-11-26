document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chat-container');
    const chatButton = document.getElementById('chat-button');
    const chatImage = document.getElementById('chat-image');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function getTimeOfDay() {
        const currentHour = new Date().getHours();
        if (currentHour >= 5 && currentHour < 12) {
            return "Morning";
        } else if (currentHour >= 12 && currentHour < 18) {
            return "Afternoon";
        } else {
            return "Evening";
        }
    }

    const welcomeMessage = `Good ${getTimeOfDay()}! I'm Insurance Genie. How may I help you?`;
    appendMessage("Genie", welcomeMessage, "bot-message");

    chatButton.addEventListener('click', function () {
        if (chatContainer.style.display === 'block') {
            chatContainer.style.display = 'none';
            chatButton.style.backgroundColor = '#4CAF50';
        } else {
            chatContainer.style.display = 'block';
            chatButton.style.backgroundColor = '#3498db';
        }
    });

    sendButton.addEventListener('click', function () {
        const userMessage = userInput.value;
        if (userMessage.trim() !== "") {
            appendMessage("You", userMessage, "user-message");
            userInput.value = "";

            // Make an AJAX request to the Flask server
            fetch('/process_input', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'user_input': userMessage,
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Handle the responses received from the server
                const genieResponse = data.responses.length > 0
                    ? formatGenieResponses(data.responses)
                    : "Sorry! I did not understand. Can you please rephrase?";
                appendMessage("Genie", genieResponse, "bot-message");
            })
            .catch(error => {
                console.error('Error processing input:', error);
            });
        }
    });

    function appendMessage(sender, message, messageClass) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageClass);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatGenieResponses(responses) {
        // Format Genie's responses with buttons
        const formattedResponses = responses.map(response => `<button>${response}</button>`).join(' ');
        return `Did you mean - ${formattedResponses}`;
    }
});