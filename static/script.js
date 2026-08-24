async function sendMessage() {

    const input = document.getElementById("messageInput");
    const chatBox = document.getElementById("chatBox");
    const sendButton = document.getElementById("sendButton");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Add user message
    addMessage(message, "user");

    // Clear input
    input.value = "";

    // Disable send button
    sendButton.disabled = true;
    sendButton.innerText = "Thinking...";


    // Create thinking message
    const typing = document.createElement("div");

    typing.className = "message bot";
    typing.id = "typing";

    typing.innerHTML = `
        <div class="avatar">🎤</div>

        <div class="bubble">
            <strong>InterviewPrep AI</strong>
            <p>Thinking...</p>
        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        // Get response as text first
        const responseText = await response.text();

        let data;

        try {
            data = JSON.parse(responseText);
        } catch (jsonError) {

            console.error(
                "Invalid JSON response:",
                responseText
            );

            throw new Error(
                "Server returned an invalid response."
            );
        }


        // Remove thinking message
        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }


        // Handle server errors
        if (!response.ok) {

            addMessage(
                data.reply ||
                "Sorry, something went wrong. Please try again.",
                "bot"
            );

            return;
        }


        // Add AI response
        addMessage(
            data.reply ||
            "Sorry, I could not generate a response.",
            "bot"
        );


    } catch (error) {

        console.error("Chat error:", error);


        // Remove thinking message
        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }


        addMessage(
            "Unable to connect to the server. Please try again.",
            "bot"
        );

    } finally {

        // Enable send button
        sendButton.disabled = false;
        sendButton.innerText = "Send ➤";

        input.focus();

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}


/* --------------------------------
   ADD MESSAGE
-------------------------------- */

function addMessage(text, type) {

    const chatBox =
        document.getElementById("chatBox");

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        `message ${type}`;


    if (type === "user") {

        messageDiv.innerHTML = `
            <div class="bubble">
                <strong>You</strong>
                <p></p>
            </div>
        `;

    } else {

        messageDiv.innerHTML = `
            <div class="avatar">🎤</div>

            <div class="bubble">
                <strong>InterviewPrep AI</strong>
                <p></p>
            </div>
        `;
    }


    // Safely display text
    const paragraph =
        messageDiv.querySelector("p");

    paragraph.textContent = text;


    chatBox.appendChild(messageDiv);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


/* --------------------------------
   QUICK QUESTIONS
-------------------------------- */

function quickQuestion(question) {

    const input =
        document.getElementById("messageInput");

    input.value = question;

    sendMessage();
}


/* --------------------------------
   ENTER KEY
-------------------------------- */

document
    .getElementById("messageInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }

    });