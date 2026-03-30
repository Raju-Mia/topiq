function toggleChat() {
    const overlay = document.getElementById("chatOverlay");
    const panel = document.getElementById("chatPanel");

    if (!overlay || !panel) {
        return;
    }

    overlay.classList.toggle("open");
    panel.classList.toggle("open");
}

function sendMsg() {
    const input = document.getElementById("chatInput");
    const messages = document.getElementById("chatMessages");

    if (!input || !messages) {
        return;
    }

    const value = input.value.trim();
    if (!value) {
        return;
    }

    const typingMessage = messages.querySelector(".msg.ai:last-child");
    if (typingMessage && typingMessage.querySelector(".typing")) {
        typingMessage.remove();
    }

    const userMsg = document.createElement("div");
    userMsg.className = "msg user";
    userMsg.innerHTML = `<div class="msg-avatar">U</div><div class="msg-bubble">${value}</div>`;
    messages.appendChild(userMsg);

    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    window.setTimeout(() => {
        const aiMsg = document.createElement("div");
        aiMsg.className = "msg ai";
        aiMsg.innerHTML = `<div class="msg-avatar">AI</div><div class="msg-bubble">Thanks for your question! This is a placeholder response. In the full version, I'll provide a detailed, university-level answer tailored to your query. 📚</div>`;
        messages.appendChild(aiMsg);
        messages.scrollTop = messages.scrollHeight;
    }, 800);
}

document.querySelectorAll("[data-chat-toggle]").forEach((button) => {
    button.addEventListener("click", toggleChat);
});

const chatInput = document.getElementById("chatInput");
if (chatInput) {
    chatInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendMsg();
        }
    });
}

const sendButton = document.querySelector("[data-send-message]");
if (sendButton) {
    sendButton.addEventListener("click", sendMsg);
}
