
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const chatMessages = document.getElementById("chat-messages");
const sendButton = document.getElementById("send-button");


function getCSRFToken() {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith("csrftoken=")) {
            return decodeURIComponent(
                cookie.substring("csrftoken=".length)
            );
        }
    }

    return "";
}


function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}-message`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = text;

    message.appendChild(content);
    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "user");

    questionInput.value = "";
    sendButton.disabled = true;

    try {
        const response = await fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            credentials: "same-origin",
            body: JSON.stringify({
                question: question
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.error || "Something went wrong."
            );
        }

        addMessage(result.answer, "bot");

    } catch (error) {
        addMessage(
            "Sorry, I couldn't process your question. Please try again.",
            "bot"
        );

        console.error(error);

    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
});
