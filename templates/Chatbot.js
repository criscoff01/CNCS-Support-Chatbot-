//References: JavaScript Tutorial Full Course - Beginner to Pro - https://www.youtube.com/watch?v=EerdGm-ehJQ

document.addEventListener('DOMContentLoaded', function() {
    
    // Interface objects from the host web page
    const chatMessages = document.getElementById('chat-messages');
    const chatBotContainer = document.getElementById('chat-container');
    const chatLaunchButton = document.getElementById('chat-launch-button');
    const chatMinimizeButton = document.getElementById('chat-minimize-button');
    
    // Animation timing constants
    const TYPING_DELAY = 650; // Time to show typing indicator
    const MESSAGE_FADE_DURATION = 275; // Fade in duration for messages
    const BUTTON_STAGGER_DELAY = 15; // Delay between each button appearing
    
    // Toggle chat visibility - if opening the chat and it's empty, initialize it
    function toggleChat() {
        chatBotContainer.classList.toggle('minimized');     // Toggle minimized state
        chatLaunchButton.classList.toggle('hidden');        // Toggle hidden state
        if (!chatBotContainer.classList.contains('minimized') && chatMessages.children.length === 0) {
            // Add a small delay before showing the greeting to feel more natural
            setTimeout(() => {
                handleUserInput('', 'greeting');
            }, 300);
        }
    }
    
    // Open the chatbot - chatLaunchButton is not visible when chatbot is open
    chatLaunchButton.addEventListener('click', toggleChat);
    
    // Minimize the chatbot - chatMinimizeButton is not visible when chatbot is closed
    chatMinimizeButton.addEventListener('click', toggleChat);
    
    // Create and show typing indicator
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
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Animate in the typing indicator
        requestAnimationFrame(() => {
            typingDiv.style.opacity = '1';
            typingDiv.style.transform = 'translateY(0)';
        });
        
        return typingDiv;
    }
    
    // Remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.opacity = '0';
            typingIndicator.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (typingIndicator.parentNode) {
                    typingIndicator.remove();
                }
            }, MESSAGE_FADE_DURATION);
        }
    }
    
    // Present each new text message (from the user or the chatbot) to the user in the chatbox display
    function addMessage(text, isUser = false, delay = 0) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const messageDiv = document.createElement('div');       // Create a message for display
                messageDiv.classList.add('message');                    // Register the message for CSS support
                if (isUser) {
                    messageDiv.classList.add('user-message');           // Register as a user's message for CSS support
                } else {
                    messageDiv.classList.add('bot-message');            // Register as a chatbot message for CSS support
                }
                messageDiv.textContent = text;                          // Add the message text
                
                // Set initial state for animation (invisible and slightly offset)
                messageDiv.style.opacity = '0';
                messageDiv.style.transform = 'translateY(20px)';
                messageDiv.style.transition = `all ${MESSAGE_FADE_DURATION}ms ease-out`;
                
                chatMessages.appendChild(messageDiv);                   // Append it to the chat messages
                chatMessages.scrollTop = chatMessages.scrollHeight;     // Scroll to the bottom of the chat messages
                
                // Animate in the message
                requestAnimationFrame(() => {
                    messageDiv.style.opacity = '1';
                    messageDiv.style.transform = 'translateY(0)';
                });
                
                // Resolve after animation completes
                setTimeout(resolve, MESSAGE_FADE_DURATION);
            }, delay);
        });
    }
    
    // Present text input field to the user to enable order number input for checking order status
    function addOrderInput(delay = 0) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const orderInputContainer = document.createElement('div');  // Create an order input container
                orderInputContainer.classList.add('order-input-container'); // Register the container for CSS support
                orderInputContainer.id = 'order-input-container';           // ID the container for easy lookup
                
                // Set initial state for animation
                orderInputContainer.style.opacity = '0';
                orderInputContainer.style.transform = 'translateY(20px)';
                orderInputContainer.style.transition = `all ${MESSAGE_FADE_DURATION}ms ease-out`;
                
                const orderInput = document.createElement('input');         // Create a text input field to get the order number
                orderInput.classList.add('order-input');                    // Register the input field for CSS support
                orderInput.id = 'order-input';                              // ID the text input field for easy lookup
                orderInput.placeholder = 'Enter your order number...';      // Display instructions to user
                orderInput.type = 'number';                                 // Set input type to number (restricts submissions to numbers)
                
                const submitButton = document.createElement('button');      // Create a submit button for use with text input field
                submitButton.classList.add('order-submit-button');          // Register the button for CSS support
                submitButton.textContent = 'Status';                        // Label the button
                submitButton.addEventListener('click', function() {         // Enable text input by clicking the submit button
                    submitOrderNumber();                                          // submit if clicked
                });                                                       
                orderInput.addEventListener('keypress', function(event) {   // Enable text input by pressing the enter key
                    if (event.key == 'Enter') {                                // If Enter key was pressed...
                        submitOrderNumber();                                          // submit number
                    }
                });
                
                orderInputContainer.appendChild(orderInput);                // Append text input box to a container
                orderInputContainer.appendChild(submitButton);              // Append the submit button to the same container
                chatMessages.appendChild(orderInputContainer);              // Display the whole container in the chat stream
                chatMessages.scrollTop = chatMessages.scrollHeight;         // Scroll to the bottom of the chat messages to make it show
                
                // Animate in the input container
                requestAnimationFrame(() => {
                    orderInputContainer.style.opacity = '1';
                    orderInputContainer.style.transform = 'translateY(0)';
                });
                
                // Focus the input after animation
                setTimeout(() => {
                    orderInput.focus();
                    resolve();
                }, MESSAGE_FADE_DURATION);
            }, delay);
        });
    }

    // Handle user submission of an order number via the text input field
    function submitOrderNumber() {
        const orderInput = document.getElementById('order-input');
        const orderNumber = orderInput.value.trim();
        if (orderNumber){
            addMessage(`Order #${orderNumber}`, true); // Add the order number as a user message to the chat display
            handleUserInput(orderNumber, 'order');     // submit msg to chatbot with order# $ 'TrackOrderIntent'
        }
    }

    // Remove the order input text box from the chat stream
    function removeTextInputBoxFromChat() {
        const orderInputContainer = document.getElementById('order-input-container');
        if (orderInputContainer) {                     // if present....
            orderInputContainer.style.opacity = '0';
            orderInputContainer.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (orderInputContainer.parentNode) {
                    orderInputContainer.remove();
                }
            }, MESSAGE_FADE_DURATION);
        }
    }

    // Remove the buttons from the chat stream
    function removeButtonsFromChat() {
        const buttonsContainer = document.getElementById('buttons-container');
        if (buttonsContainer) {                 // If present...
            buttonsContainer.style.opacity = '0';
            buttonsContainer.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (buttonsContainer.parentNode) {
                    buttonsContainer.remove();
                }
            }, MESSAGE_FADE_DURATION);
        }
    }

    // Clear all Prior User input elements from the chat stream, leaving only the user and chatbot text messages
    function clearPriorUIElements() {
        removeButtonsFromChat();
        removeTextInputBoxFromChat();
    }

    // Present the userIntent buttons that were provided in a chatbot response (menu-driven chat) to the user
    function addButtons(buttons, initialDelay = 0) {
        return new Promise((resolve) => {
            if (!buttons || buttons.length === 0) {
                resolve();
                return;
            }
            
            setTimeout(() => {
                const buttonsContainer = document.createElement('div');     // Create a buttonsContainer
                buttonsContainer.classList.add('buttons-container');        // Register the container to enable CSS support
                buttonsContainer.id = 'buttons-container';                  // ID the container for easy lookup
                
                // Set initial container state
                buttonsContainer.style.opacity = '0';
                buttonsContainer.style.transform = 'translateY(20px)';
                buttonsContainer.style.transition = `all ${MESSAGE_FADE_DURATION}ms ease-out`;
                
                let buttonCount = 0;
                buttons.forEach((button, index) => {                                 // Create all buttons requested by the chatbot
                    const buttonElement = document.createElement('button'); // Create a new button
                    buttonElement.classList.add('option-button');           // Register each button to enable CSS support
                    buttonElement.textContent = button.text;                // Label each button
                    
                    // Set initial button state for staggered animation
                    buttonElement.style.opacity = '0';
                    buttonElement.style.transform = 'scale(0.8) translateY(10px)';
                    buttonElement.style.transition = `all ${MESSAGE_FADE_DURATION}ms ease-out`;
                    
                    buttonElement.addEventListener('click', () => {         // Add a click handler for each button
                        // Add subtle click animation
                        buttonElement.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            addMessage(button.text, true);                      // Start monitoring each button (by label)
                            handleUserInput('', button.value);                  // msg to chatbot - if clicked, value = userIntent
                        }, 100);
                    });
                    
                    buttonsContainer.appendChild(buttonElement);            // Append each new button to the buttonsContainer
                });
                
                chatMessages.appendChild(buttonsContainer);                 // Display the buttons as a chat message
                chatMessages.scrollTop = chatMessages.scrollHeight;         // Scroll to the bottom of the chat messages
                
                // Animate in the container first
                requestAnimationFrame(() => {
                    buttonsContainer.style.opacity = '1';
                    buttonsContainer.style.transform = 'translateY(0)';
                });
                
                // Then animate in each button with staggered timing
                const buttonElements = buttonsContainer.querySelectorAll('.option-button');
                buttonElements.forEach((buttonElement, index) => {
                    setTimeout(() => {
                        buttonElement.style.opacity = '1';
                        buttonElement.style.transform = 'scale(1) translateY(0)';
                        buttonCount++;
                        
                        // Resolve when all buttons are animated in
                        if (buttonCount === buttons.length) {
                            setTimeout(resolve, MESSAGE_FADE_DURATION);
                        }
                    }, MESSAGE_FADE_DURATION + (index * BUTTON_STAGGER_DELAY));
                });
                
            }, initialDelay);
        });
    }

    // Handle user input (button click) and the chatbot's response
    function handleUserInput(text, buttonValue) {
        const messageToChatbot = {              // Prep the user's message
            userTypedText: text,
            userIntent: buttonValue
        };
        
        // Clear previous UI elements immediately
        clearPriorUIElements();
        
        // Show typing indicator for bot responses (but not for the initial greeting)
        let typingIndicator = null;
        if (buttonValue !== 'greeting') {
            typingIndicator = showTypingIndicator();
        }
        
        fetch('/api/chat', {                    // Send the user's message to the chatbot & fetch its response
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(messageToChatbot)
        })
        .then(response => response.json())      // Then process the chatbot's response
        .then(data => {
            // Calculate delay based on whether we're showing typing indicator
            const responseDelay = typingIndicator ? TYPING_DELAY : 0;
            
            setTimeout(() => {
                // Remove typing indicator if it exists
                if (typingIndicator) {
                    removeTypingIndicator();
                }
                
                // Add the bot message with a small delay after typing indicator removal
                setTimeout(async () => {
                    await addMessage(data.response, false);
                    
                    // Add input field if needed
                    if (data.enableTextInput) {
                        await addOrderInput(200);
                    }
                    
                    // Add buttons with a slight delay
                    await addButtons(data.buttons, 300);
                    
                }, typingIndicator ? MESSAGE_FADE_DURATION : 0);
                
            }, responseDelay);
        })
        .catch(error => {                       // Something didn't work right - investigate
            console.error('Error:', error);
            if (typingIndicator) {
                removeTypingIndicator();
            }
            setTimeout(() => {
                addMessage('Sorry, something went wrong. Please try again.', false);
            }, typingIndicator ? MESSAGE_FADE_DURATION : 0);
        });
    }

});