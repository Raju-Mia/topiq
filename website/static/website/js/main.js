/* Initialize all interactive behavior once the DOM is ready. */
document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initChatPanel();
  initFeedback();
  initBookmark();
  initToasts();
});

/* Set up search form behavior, loading states, and autofocus. */
function initSearch() {
  const searchForms = document.querySelectorAll('form[action*="/search/"]');

  searchForms.forEach((form) => {
    const input = form.querySelector('input[name="q"]');
    const button = form.querySelector(".search-btn");

    if (!input || !button) {
      return;
    }

    form.addEventListener("submit", () => {
      button.dataset.originalText = button.textContent.trim();
      button.disabled = true;
      button.classList.add("loading");
      button.innerHTML = '<span class="spinner"></span><span>Searching</span>';
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        form.requestSubmit();
      }
    });
  });

  if (document.body.dataset.pageTitle.includes("Results")) {
    const resultsSearchInput = document.querySelector('.hero-search-row input[name="q"]');
    if (resultsSearchInput) {
      resultsSearchInput.focus();
      resultsSearchInput.setSelectionRange(resultsSearchInput.value.length, resultsSearchInput.value.length);
    }
  }
}

/* Wire up chat toggling, message sending, and AI response fetching. */
function initChatPanel() {
  const overlay = document.getElementById("chatOverlay");
  const panel = document.getElementById("chatPanel");
  const input = document.getElementById("chatInput");
  const sendButton = document.querySelector("[data-send-message]");
  const toggles = document.querySelectorAll("[data-chat-toggle]");

  if (!overlay || !panel || !input || !sendButton) {
    return;
  }

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const isOpen = panel.classList.contains("open");
      overlay.classList.toggle("open");
      panel.classList.toggle("open");
      
      if (!isOpen) {
        input.focus();
      }
    });
  });

  const submitMessage = async () => {
    const message = input.value.trim();
    if (!message) {
      showToast("Please enter a question first.", "error");
      return;
    }

    input.disabled = true;
    sendButton.disabled = true;

    appendMessage("user", message);
    input.value = "";

    const typingEl = appendTypingIndicator();

    try {
      const response = await fetch("/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({
          message: message,
          topic_context: getCurrentTopicContext(),
        }),
      });

      const data = await response.json();
      typingEl.remove();

      if (!response.ok) {
        throw new Error(data.error || "Unable to get AI response.");
      }

      appendMessage("ai", data.reply || "I could not generate an answer right now.");
    } catch (error) {
      if (typingEl.isConnected) {
        typingEl.remove();
      }
      appendMessage("ai", "Sorry, the AI assistant is unavailable right now.");
      showToast(error.message || "Chat request failed.", "error");
    } finally {
      input.disabled = false;
      sendButton.disabled = false;
      input.focus();
      scrollChatToBottom();
    }
  };

  sendButton.addEventListener("click", submitMessage);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submitMessage();
    }
  });

  // Add copy buttons to messages
  initMessageCopy();
}

/* Return the CSRF token from the browser cookie string. */
function getCsrfToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1] || "";
}

/* Read the current topic context from body data attributes. */
function getCurrentTopicContext() {
  return document.body.dataset.topic || "";
}

/* Attach click handlers for helpful and not-helpful feedback buttons. */
function initFeedback() {
  const buttons = document.querySelectorAll(".feedback-btn");

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const resourceType = button.dataset.resourceType;
      const resourceId = button.dataset.resourceId;
      const topicId = button.dataset.topicId;
      const feedbackType = button.classList.contains("not-helpful") ? "not_helpful" : "helpful";

      if (!resourceType || !resourceId || !topicId) {
        showToast("Missing feedback data.", "error");
        return;
      }

      const row = button.closest(".feedback-row");
      const siblingButtons = row ? row.querySelectorAll(".feedback-btn") : [];
      siblingButtons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");

      const originalText = button.textContent;
      button.disabled = true;
      button.innerHTML = '<span class="spinner"></span>';

      try {
        const response = await fetch("/feedback/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            resource_type: resourceType,
            resource_id: resourceId,
            feedback_type: feedbackType,
            topic_id: topicId,
          }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Could not save feedback.");
        }

        updateHelpfulCount(button, data.helpful_count);
        showToast(feedbackType === "helpful" ? "Marked as helpful." : "Feedback saved.", "success");
      } catch (error) {
        button.classList.remove("active");
        showToast(error.message || "Feedback request failed.", "error");
      } finally {
        button.disabled = false;
        button.textContent = originalText;
      }
    });
  });
}

/* Update the visible helpful count badge for a resource card. */
function updateHelpfulCount(button, helpfulCount) {
  const card = button.closest(".video-card, .article-card");
  if (!card) {
    return;
  }

  let badge = card.querySelector("[data-helpful-display]");
  if (!badge && Number(helpfulCount) > 0) {
    badge = document.createElement("div");
    badge.className = "why-badge";
    badge.setAttribute("data-helpful-display", "");

    const metaRow = card.querySelector(".meta-row");
    if (metaRow) {
      metaRow.insertAdjacentElement("beforebegin", badge);
    } else {
      const content = card.querySelector(".video-body, .article-content");
      if (content) {
        content.appendChild(badge);
      }
    }
  }

  if (!badge) {
    return;
  }

  badge.innerHTML = `👍 <span class="helpful-count">${helpfulCount}</span> students found this helpful`;

  if (Number(helpfulCount) <= 0) {
    badge.remove();
  }
}

/* Attach click handlers for bookmark buttons and sync their state. */
function initBookmark() {
  const buttons = document.querySelectorAll(".bookmark-btn");

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const topicId = button.dataset.topicId;
      if (!topicId) {
        showToast("Missing topic information.", "error");
        return;
      }

      button.classList.add("bounce");
      window.setTimeout(() => button.classList.remove("bounce"), 360);

      button.disabled = true;

      try {
        const response = await fetch("/bookmark/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({ topic_id: topicId }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Could not update bookmark.");
        }

        const isActive = data.action === "added";
        syncBookmarkButtons(topicId, isActive);
        showToast(isActive ? "Topic Saved!" : "Bookmark Removed", isActive ? "success" : "error");
      } catch (error) {
        showToast(error.message || "Bookmark request failed.", "error");
      } finally {
        button.disabled = false;
      }
    });
  });
}

/* Keep all bookmark buttons for the same topic visually in sync. */
function syncBookmarkButtons(topicId, active) {
  const buttons = document.querySelectorAll(`.bookmark-btn[data-topic-id="${CSS.escape(String(topicId))}"]`);

  buttons.forEach((button) => {
    button.classList.toggle("active", active);
    button.textContent = `${active ? "⭐" : "☆"} Save Topic`;
  });
}

/* Prepare global toast behavior. */
function initToasts() {
  window.showToast = showToast;
}

/* Render a toast notification and remove it after a delay. */
function showToast(message, type = "success", duration = 3000) {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    requestAnimationFrame(() => toast.classList.add("show"));
  });

  window.setTimeout(() => {
    toast.classList.remove("show");
    window.setTimeout(() => toast.remove(), 300);
  }, duration);
}

/* Scroll the chat message list to the newest message. */
function scrollChatToBottom() {
  const messagesEl = document.getElementById("chatMessages");
  if (messagesEl) {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
}

/* Append a message bubble to the chat area. */
function appendMessage(role, text) {
  const messagesEl = document.getElementById("chatMessages");
  if (!messagesEl) {
    return;
  }

  const div = document.createElement("div");
  div.className = `msg ${role}`;
  
  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = role === "ai" ? "AI" : "U";
  
  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  
  // Format message with markdown-like structure
  const formattedText = formatMessage(text);
  bubble.innerHTML = formattedText;
  
  // Add copy button for AI messages
  if (role === "ai") {
    const copyBtn = document.createElement("button");
    copyBtn.className = "msg-copy-btn";
    copyBtn.innerHTML = `
      <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"></rect>
        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" fill="none" stroke="currentColor" stroke-width="2"></path>
      </svg>
    `;
    copyBtn.title = "Copy message";
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(text).then(() => {
        copyBtn.classList.add("copied");
        copyBtn.innerHTML = `
          <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
            <polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" stroke-width="2"></polyline>
          </svg>
        `;
        setTimeout(() => {
          copyBtn.classList.remove("copied");
          copyBtn.innerHTML = `
            <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"></rect>
              <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" fill="none" stroke="currentColor" stroke-width="2"></path>
            </svg>
          `;
        }, 2000);
      });
    });
    bubble.appendChild(copyBtn);
  }
  
  div.appendChild(avatar);
  div.appendChild(bubble);
  messagesEl.appendChild(div);
  scrollChatToBottom();
}

/* Append a temporary typing indicator while waiting for AI output. */
function appendTypingIndicator() {
  const messagesEl = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = "msg ai";
  div.innerHTML = `
    <div class="msg-avatar">AI</div>
    <div class="msg-bubble typing"><span></span><span></span><span></span></div>
  `;
  messagesEl.appendChild(div);
  scrollChatToBottom();
  return div;
}

/* Escape unsafe HTML from dynamic message text before rendering. */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

/* Format message text with basic markdown-like structure. */
function formatMessage(text) {
  // Escape HTML first
  let formatted = escapeHtml(text);
  
  // Convert code blocks
  formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre class="code-block">$1</pre>');
  
  // Convert inline code
  formatted = formatted.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
  
  // Convert bold
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Convert italic
  formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  
  // Convert line breaks to <br>
  formatted = formatted.replace(/\n/g, '<br>');
  
  return formatted;
}

/* Initialize copy functionality for existing messages. */
function initMessageCopy() {
  // This will be called when messages are loaded
}
