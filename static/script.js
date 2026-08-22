async function sendMessage() {

    const input = document.getElementById("messageInput");
    const chatBox = document.getElementById("chatBox");
    const sendButton = document.getElementById("sendButton");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    sendButton.disabled = true;
    sendButton.innerText = "Thinking...";


    const typing = document.createElement("div");

    typing.className = "message bot";
    typing.id = "typing";

    typing.innerHTML = `
        <div class="avatar">🎯</div>

        <div class="bubble">
            <strong>CareerGuide AI</strong>
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


        const data = await response.json();


        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }


        addMessage(data.reply, "bot");


    } catch (error) {

        console.error(error);

        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }

        addMessage(
            "Unable to connect to the server. Please try again.",
            "bot"
        );
    }


    sendButton.disabled = false;
    sendButton.innerText = "Send ➤";

    input.focus();
}


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
                <p>${escapeHTML(text)}</p>
            </div>
        `;

    } else {

        messageDiv.innerHTML = `
            <div class="avatar">🎯</div>

            <div class="bubble">
                <strong>CareerGuide AI</strong>
                <p>${escapeHTML(text)}</p>
            </div>
        `;
    }


    chatBox.appendChild(messageDiv);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function quickQuestion(question) {

    const input =
        document.getElementById("messageInput");

    input.value = question;

    sendMessage();
}


function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


document
    .getElementById("messageInput")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    });