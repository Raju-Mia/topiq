# Prompt 07 — CSS & JavaScript (`style.css` + `main.js`)

## Your Task

You are a senior frontend developer. I am building **Topiq** — a dark-themed, modern web app for university students to find learning resources. Write the **complete `website/static/website/css/style.css`** and **complete `website/static/website/js/main.js`** files. Every line must be copy-paste ready. Do not write partial code.

---

## CSS Design Reference

**Font Stack:**
```css
--font-body: 'Sora', sans-serif;
--font-display: 'DM Serif Display', serif;
```

**Color Variables:**
```css
--bg: #0a0a0f;
--bg-card: #111118;
--bg-card-hover: #16161f;
--border: rgba(255, 255, 255, 0.08);
--border-hover: rgba(255, 255, 255, 0.15);
--text-primary: #e8e8f0;
--text-secondary: #888899;
--text-muted: #55556a;
--accent-purple: #6366f1;
--accent-violet: #8b5cf6;
--accent-red: #DC2626;
--accent-blue: #1E88E5;
--accent-green: #059669;
--gradient: linear-gradient(135deg, #6366f1, #8b5cf6);
--gradient-red: linear-gradient(135deg, #DC2626, #ef4444);
--shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
--shadow-hover: 0 8px 40px rgba(99, 102, 241, 0.2);
--radius: 14px;
--radius-sm: 8px;
```

---

## CSS Sections to Write

### 1. Reset & Base
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text-primary); font-family: var(--font-body); }
```

### 2. Header
- Fixed top, full width, blur backdrop
- `background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(20px);`
- Height: 64px
- Logo: gradient text effect on the "iq" part
- Search bar in center: pill-shaped, dark input, purple search button
- AI button: circular, gradient background, pulsing badge dot

### 3. Hero Section
- Centered, padded top (120px top to account for fixed header)
- Hero badge: small pill with star icon and gradient border
- H1: large font, DM Serif Display, `<em>` tag in italic with gradient color
- Subtitle: muted text, max-width 540px

### 4. Stats Bar
- Horizontal scrollable row of chips
- Each chip: dark pill background, small dot, text

### 5. Results Grid
- CSS Grid: `grid-template-columns: 1fr 1fr;` on desktop
- Gap: 24px
- On tablet: single column

### 6. Section Header
- Flex row: icon + title + count badge
- Icon: colored circle background, SVG inside
- Count badge: small, muted

### 7. Video Card
```css
.video-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.video-card:hover {
  border-color: var(--border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}
```

Video thumb:
- Aspect ratio 16:9 or fixed height 180px
- Dark placeholder background with gradient overlay
- Play button: circular, centered, white with transparency
- Duration badge: bottom-right, dark pill
- Difficulty badge: top-left, colored by level:
  - `.beginner` → green background
  - `.intermediate` → orange/amber background  
  - `.advanced` → red background

Video body:
- Padding: 16px
- Title: bold, 15px, 2-line clamp with `overflow: hidden`
- Description: muted, 13px, 3-line clamp
- YouTube button: full-width, red gradient, YouTube icon + "Open on YouTube"

### 8. Article Card
```css
.article-card {
  display: flex;
  gap: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  /* same hover effect as video card */
}
```

- Icon: 48×48px circle, colored by type:
  - `.pdf` → red circle, PDF icon
  - `.blog` → purple circle, blog icon
  - `.note` → green circle, notes icon
- Type badge: small colored pill above title
- Title: bold, 14px
- Description: muted, 13px, 3-line clamp
- Read link: inline with arrow, hover underline

### 9. Feedback Row
```css
.feedback-row {
  display: flex;
  gap: 8px;
  margin: 12px 0;
}
.feedback-btn {
  flex: 1;
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}
.feedback-btn.helpful:hover, .feedback-btn.helpful.active {
  border-color: var(--accent-green);
  color: var(--accent-green);
  background: rgba(5, 150, 105, 0.1);
}
.feedback-btn.not-helpful:hover, .feedback-btn.not-helpful.active {
  border-color: var(--accent-red);
  color: var(--accent-red);
  background: rgba(220, 38, 38, 0.1);
}
```

### 10. AI Chat Panel
- Fixed right side panel, width 380px
- Slides in from right: `transform: translateX(100%)` → `translateX(0)` with transition
- Chat overlay: full-screen dark transparent backdrop
- Chat header: gradient background, avatar, title, close button
- Messages area: scrollable, padding, gap between messages
- Message bubble: rounded, max-width 85%
  - AI messages: dark card background, left-aligned
  - User messages: purple gradient, right-aligned
- Typing indicator: 3 pulsing dots animation
- Input row: sticky bottom, dark input + send button

### 11. Toast Notifications
```css
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  border-radius: var(--radius-sm);
  color: white;
  font-size: 14px;
  z-index: 9999;
  transform: translateY(100px);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast.show {
  transform: translateY(0);
  opacity: 1;
}
.toast.success { background: var(--accent-green); }
.toast.error { background: var(--accent-red); }
```

### 12. Bookmark Button
- Star icon that fills on active state
- Active state: golden yellow color
- Animation: scale bounce on click

### 13. Similar Topics Chips
- Horizontal flex wrap
- Each chip: pill shape, purple border, hover → purple fill

### 14. No Results State
- Centered, with large search icon
- Suggested searches grid

### 15. Loading Spinner
```css
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-top-color: var(--accent-purple);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
```

### 16. Responsive Breakpoints
```css
/* Tablet */
@media (max-width: 900px) {
  .results-grid { grid-template-columns: 1fr; }
}
/* Mobile */
@media (max-width: 600px) {
  .header-inner { /* stack elements */ }
  .search-wrap { /* full width */ }
  .chat-panel { width: 100%; }
}
```

---

## JavaScript (`main.js`) — Complete

Write the complete `main.js` with these features:

### 1. DOM Ready
```javascript
document.addEventListener('DOMContentLoaded', () => {
  initSearch();
  initChatPanel();
  initFeedback();
  initBookmark();
  initToasts();
});
```

### 2. `initSearch()` — Search Bar Behavior
- On Enter keypress → submit the form
- Show loading spinner inside search button on submit
- Disable button while loading
- On results page, auto-focus the search input

### 3. `initChatPanel()` — AI Chat
- All elements with `[data-chat-toggle]` → toggle panel open/close
- `[data-send-message]` button + Enter key → send message
- On send:
  1. Disable input + button
  2. Append user message bubble to chat
  3. Show typing indicator (3 dots)
  4. Fetch POST to `/api/chat/` with CSRF token:
     ```javascript
     const response = await fetch('/api/chat/', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': getCsrfToken(),
       },
       body: JSON.stringify({
         message: message,
         topic_context: getCurrentTopicContext(),
       }),
     });
     ```
  5. Remove typing indicator
  6. Append AI reply bubble
  7. Scroll chat to bottom
  8. Re-enable input + button
  9. On error → show error toast

### 4. `getCsrfToken()` helper
```javascript
function getCsrfToken() {
  return document.cookie.split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}
```

### 5. `getCurrentTopicContext()` helper
```javascript
function getCurrentTopicContext() {
  // Read from data attribute set in results.html:
  // <body data-topic="{{ matched_topic.name }}" data-subject="{{ subject_name }}">
  return document.body.dataset.topic || '';
}
```

### 6. `initFeedback()` — Helpful / Not Helpful Buttons
- All `.feedback-btn` elements → click handler
- On click:
  1. Add `.active` class to clicked button, remove from sibling
  2. Show loading state on button
  3. POST to `/feedback/` with resource type, id, feedback type
  4. On success: update button state permanently, show toast
  5. Update helpful count display if present

### 7. `initBookmark()` — Save Topic Button
- All `.bookmark-btn` elements → click handler
- On click:
  1. Animate button (scale bounce)
  2. POST to `/bookmark/` with topic_id
  3. On success:
     - If action === 'added': fill star ⭐, show "Topic Saved!" toast
     - If action === 'removed': empty star ☆, show "Bookmark Removed" toast

### 8. Toast System
```javascript
function showToast(message, type = 'success', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  // Force reflow then show
  requestAnimationFrame(() => {
    requestAnimationFrame(() => toast.classList.add('show'));
  });
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
```

### 9. Scroll Chat to Bottom
```javascript
function scrollChatToBottom() {
  const messagesEl = document.getElementById('chatMessages');
  if (messagesEl) {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
}
```

### 10. Append Message Bubble
```javascript
function appendMessage(role, text) {
  const messagesEl = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="msg-avatar">${role === 'ai' ? 'AI' : 'U'}</div>
    <div class="msg-bubble">${escapeHtml(text)}</div>
  `;
  messagesEl.appendChild(div);
  scrollChatToBottom();
}
```

### 11. `escapeHtml(text)` — Security
```javascript
function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}
```

---

## Output Requirements

- Complete `style.css` — every selector, every property, every animation
- Complete `main.js` — every function, every event listener, fully working
- CSS must use variables throughout — no hardcoded color hex values except in `:root`
- JS must have no external dependencies — pure vanilla JavaScript
- All fetch calls must handle errors properly
- CSS must be mobile responsive
- Add section comments in CSS: `/* ═══ HEADER ═══ */`, `/* ═══ VIDEO CARD ═══ */` etc.
- Add function comments in JS explaining what each function does
