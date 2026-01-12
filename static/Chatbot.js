/**
 * CNCS Chatbot - Frontend JavaScript
 * Handles UI interactions and server communication
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const elements = {
        chatMessages: document.getElementById('chat-messages'),
        chatContainer: document.getElementById('chat-container'),
        launchButton: document.getElementById('chat-launch-button'),
        minimizeButton: document.getElementById('chat-minimize-button'),
        themeToggle: document.getElementById('theme-toggle'),
        resizeHandle: null // Will be created dynamically
    };

    // Configuration
    const CONFIG = {
        typingDelay: 600,
        inputFocusDelay: 100,
        minWidth: 300,
        minHeight: 350,
        maxWidth: 600,
        maxHeight: 800
    };

    // State
    const state = {
        currentInputContext: null,
        isDarkMode: true,
        sessionId: generateSessionId(),
        isResizing: false,
        resizeStartX: 0,
        resizeStartY: 0,
        resizeStartWidth: 0,
        resizeStartHeight: 0
    };

    // Initialize
    init();

    /**
     * Initialize event listeners and UI components
     */
    function init() {
        createResizeHandle();
        elements.themeToggle.addEventListener('click', toggleTheme);
        elements.launchButton.addEventListener('click', toggleChat);
        elements.minimizeButton.addEventListener('click', toggleChat);
    }

    /**
     * Create and attach resize handle
     */
    function createResizeHandle() {
        const handle = document.createElement('div');
        handle.classList.add('resize-handle');
        handle.id = 'resize-handle';
        elements.chatContainer.appendChild(handle);
        elements.resizeHandle = handle;

        // Mouse events
        handle.addEventListener('mousedown', startResize);
        document.addEventListener('mousemove', doResize);
        document.addEventListener('mouseup', stopResize);

        // Touch events for mobile
        handle.addEventListener('touchstart', startResizeTouch, { passive: false });
        document.addEventListener('touchmove', doResizeTouch, { passive: false });
        document.addEventListener('touchend', stopResize);
    }

    /**
     * Start resize operation (mouse)
     */
    function startResize(e) {
        e.preventDefault();
        state.isResizing = true;
        state.resizeStartX = e.clientX;
        state.resizeStartY = e.clientY;
        state.resizeStartWidth = elements.chatContainer.offsetWidth;
        state.resizeStartHeight = elements.chatContainer.offsetHeight;
        elements.chatContainer.classList.add('resizing');
    }

    /**
     * Start resize operation (touch)
     */
    function startResizeTouch(e) {
        e.preventDefault();
        const touch = e.touches[0];
        state.isResizing = true;
        state.resizeStartX = touch.clientX;
        state.resizeStartY = touch.clientY;
        state.resizeStartWidth = elements.chatContainer.offsetWidth;
        state.resizeStartHeight = elements.chatContainer.offsetHeight;
        elements.chatContainer.classList.add('resizing');
    }

    /**
     * Perform resize operation (mouse)
     */
    function doResize(e) {
        if (!state.isResizing) return;
        
        // Calculate delta (inverted because we're resizing from top-left)
        const deltaX = state.resizeStartX - e.clientX;
        const deltaY = state.resizeStartY - e.clientY;
        
        applyResize(deltaX, deltaY);
    }

    /**
     * Perform resize operation (touch)
     */
    function doResizeTouch(e) {
        if (!state.isResizing) return;
        e.preventDefault();
        
        const touch = e.touches[0];
        const deltaX = state.resizeStartX - touch.clientX;
        const deltaY = state.resizeStartY - touch.clientY;
        
        applyResize(deltaX, deltaY);
    }

    /**
     * Apply resize dimensions
     */
    function applyResize(deltaX, deltaY) {
        let newWidth = state.resizeStartWidth + deltaX;
        let newHeight = state.resizeStartHeight + deltaY;
        
        // Constrain to min/max bounds
        newWidth = Math.max(CONFIG.minWidth, Math.min(CONFIG.maxWidth, newWidth));
        newHeight = Math.max(CONFIG.minHeight, Math.min(CONFIG.maxHeight, newHeight));
        
        elements.chatContainer.style.width = newWidth + 'px';
        elements.chatContainer.style.height = newHeight + 'px';
    }

    /**
     * Stop resize operation
     */
    function stopResize() {
        if (state.isResizing) {
            state.isResizing = false;
            elements.chatContainer.classList.remove('resizing');
        }
    }

    /**
     * Generate unique session ID
     */
    function generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Toggle between light and dark themes
     */
    function toggleTheme() {
        state.isDarkMode = !state.isDarkMode;
        const addClass = !state.isDarkMode;
        
        elements.chatContainer.classList.toggle('light-mode', addClass);
        elements.launchButton.classList.toggle('light-mode', addClass);
        elements.themeToggle.classList.toggle('light-mode', addClass);
    }

    /**
     * Toggle chat visibility
     */
    function toggleChat() {
        elements.chatContainer.classList.toggle('minimized');
        elements.launchButton.classList.toggle('hidden');

        // Initialize chat on first open
        const isOpen = !elements.chatContainer.classList.contains('minimized');
        const isEmpty = elements.chatMessages.children.length === 0;

        if (isOpen && isEmpty) {
            setTimeout(() => sendToServer('', 'greeting'), 200);
        }
    }

    /**
     * Add a message to the chat
     */
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        elements.chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    /**
     * Scroll chat to bottom
     */
    function scrollToBottom() {
        elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    }

    /**
     * Show typing indicator
     */
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        elements.chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    /**
     * Remove typing indicator
     */
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    /**
     * Add interactive buttons
     */
    function addButtons(buttons) {
        if (!buttons?.length) return;

        const container = document.createElement('div');
        container.classList.add('buttons-container');
        container.id = 'buttons-container';

        buttons.forEach(button => {
            const btn = document.createElement('button');
            btn.classList.add('option-button');
            btn.textContent = button.text;
            btn.addEventListener('click', () => handleButtonClick(button));
            container.appendChild(btn);
        });

        elements.chatMessages.appendChild(container);
        scrollToBottom();
    }

    /**
     * Handle button click
     */
    function handleButtonClick(button) {
        addMessage(button.text, true);
        sendToServer('', button.value);
    }

    /**
     * Remove buttons container
     */
    function removeButtons() {
        const container = document.getElementById('buttons-container');
        if (container) container.remove();
    }

    /**
     * Add text input field
     */
    function addTextInput(context, placeholder, buttonLabel) {
        state.currentInputContext = context;

        const container = document.createElement('div');
        container.classList.add('text-input-container');
        container.id = 'text-input-container';

        const input = document.createElement('input');
        input.classList.add('text-input');
        input.id = 'text-input';
        input.placeholder = placeholder;
        input.type = context === 'order' ? 'number' : 'text';

        const submitBtn = document.createElement('button');
        submitBtn.classList.add('text-submit-button');
        submitBtn.textContent = buttonLabel;
        submitBtn.addEventListener('click', submitTextInput);

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') submitTextInput();
        });

        container.appendChild(input);
        container.appendChild(submitBtn);
        elements.chatMessages.appendChild(container);
        scrollToBottom();

        setTimeout(() => input.focus(), CONFIG.inputFocusDelay);
    }

    /**
     * Submit text input
     */
    function submitTextInput() {
        const input = document.getElementById('text-input');
        const text = input.value.trim();

        if (text) {
            addMessage(text, true);
            sendToServer(text, state.currentInputContext);
        }
    }

    /**
     * Remove text input container
     */
    function removeTextInput() {
        const container = document.getElementById('text-input-container');
        if (container) container.remove();
        state.currentInputContext = null;
    }

    /**
     * Send request to server
     */
    async function sendToServer(text, intent) {
        // Clear previous UI elements
        removeButtons();
        removeTextInput();

        // Show typing indicator (except for greeting)
        const showTyping = intent !== 'greeting';
        if (showTyping) showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userTypedText: text,
                    userIntent: intent,
                    sessionId: state.sessionId
                })
            });

            const data = await response.json();
            const delay = showTyping ? CONFIG.typingDelay : 0;

            setTimeout(() => {
                removeTypingIndicator();
                addMessage(data.response, false);

                // Add text input if enabled
                if (data.enableTextInput) {
                    const inputConfig = getInputConfig(intent);
                    addTextInput(inputConfig.context, inputConfig.placeholder, inputConfig.label);
                }

                // Add buttons
                addButtons(data.buttons);
            }, delay);

        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, something went wrong. Please try again.', false);
        }
    }

    /**
     * Get input configuration based on intent
     */
    function getInputConfig(intent) {
        const configs = {
            order: {
                context: 'order',
                placeholder: 'Enter your order number...',
                label: 'Status'
            },
            freetext: {
                context: 'freetext',
                placeholder: 'Type your question...',
                label: 'Ask'
            }
        };

        return configs[intent] || configs.freetext;
    }
});
