
//References: JavaScript Tutorial Full Course - Beginner to Pro - https://www.youtube.com/watch?v=EerdGm-ehJQ


document.addEventListener('DOMContentLoaded', function() {
    
    // Interface objects from the host web page
    const chatMessages = document.getElementById('chat-messages');
    const chatBotContainer = document.getElementById('chat-container');
    const chatLaunchButton = document.getElementById('chat-launch-button');
    const chatMinimizeButton = document.getElementById('chat-minimize-button');
    
    // Toggle chat visibility - if opening the chat and it's empty, initialize it
    function toggleChat() {
        chatBotContainer.classList.toggle('minimized');     // Toggle minimized state
        chatLaunchButton.classList.toggle('hidden');        // Toggle hidden state
        if (!chatBotContainer.classList.contains('minimized') && chatMessages.children.length === 0) {
            handleUserInput('', 'greeting');                // Launch with a greeting message from the chatbot
        }
    }
    
    // Open the chatbot - chatLaunchButton is not visible when chatbot is open
    chatLaunchButton.addEventListener('click', toggleChat);
    
    // Minimize the chatbot - chatMinimizeButton is not visible when chatbot is closed
    chatMinimizeButton.addEventListener('click', toggleChat);
    
    // Present each new text message (from the user or the chatbot) to the user in the chatbox display
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');       // Create a message for display
        messageDiv.classList.add('message');                    // Register the message for CSS support
        if (isUser) {
            messageDiv.classList.add('user-message');           // Register as a user's message for CSS support
        } else {
            messageDiv.classList.add('bot-message');            // Register as a chatbot message for CSS support
        }
        messageDiv.textContent = text;                          // Add the message text
        chatMessages.appendChild(messageDiv);                   // Append it to the chat messages
        chatMessages.scrollTop = chatMessages.scrollHeight;     // Scroll to the bottom of the chat messages
    }
    
    // Present text input field to the user to enable order number input for checking order status
    function addOrderInput() {
       const orderInputContainer = document.createElement('div');  // Create an order input container
       orderInputContainer.classList.add('order-input-container'); // Register the container for CSS support
       orderInputContainer.id = 'order-input-container';           // ID the container for easy lookup
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
       })
       orderInputContainer.appendChild(orderInput);                // Append text input box to a container
       orderInputContainer.appendChild(submitButton);              // Append the submit button to the same container
       chatMessages.appendChild(orderInputContainer);              // Display the whole container in the chat stream
       orderInput.focus();                                         // Shift UI focus to text input box enabling the user to type
       chatMessages.scrollTop = chatMessages.scrollHeight;         // Scroll to the bottom of the chat messages to make it show
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
            orderInputContainer.remove();              // Remove the order input text box from the chat
        }
    }

    // Remove the buttons from the chat stream
    function removeButtonsFromChat() {
        const buttonsContainer = document.getElementById('buttons-container');
        if (buttonsContainer) {                 // If present...
            buttonsContainer.remove();          // Remove the buttons container from the chat
        }
    }

    // Clear all Prior User input elements from the chat stream, leaving only the user and chatbot text messages
    function clearPriorUIElements() {
        removeButtonsFromChat();
        removeTextInputBoxFromChat();
    }

    // Present the userIntent buttons that were provided in a chatbot response (menu-driven chat) to the user
    function addButtons(buttons) {
        if (!buttons || buttons.length === 0) return;               // if there are no buttons, then skip all below
        const buttonsContainer = document.createElement('div');     // Create a buttonsContainer
        buttonsContainer.classList.add('buttons-container');        // Register the container to enable CSS support
        buttonsContainer.id = 'buttons-container';                  // ID the container for easy lookup
        buttons.forEach(button => {                                 // Create all buttons requested by the chatbot
            const buttonElement = document.createElement('button'); // Create a new button
            buttonElement.classList.add('option-button');           // Register each button to enable CSS support
            buttonElement.textContent = button.text;                // Label each button
            buttonElement.addEventListener('click', () => {         // Add a click handler for each button
                addMessage(button.text, true);                      // Start monitoring each button (by label)
                handleUserInput('', button.value);                  // msg to chatbot - if clicked, value = userIntent
            });
            buttonsContainer.appendChild(buttonElement);            // Append each new button to the buttonsContainer
        });
        chatMessages.appendChild(buttonsContainer);                 // Display the buttons as a chat message
        chatMessages.scrollTop = chatMessages.scrollHeight;         // Scroll to the bottom of the chat messages
    }

    // Handle user input (button click) and the chatbot's response
    function handleUserInput(text, buttonValue) {
        const messageToChatbot = {              // Prep the user's message
            userTypedText: text,
            userIntent: buttonValue
        };
        fetch('/api/chat', {                    // Send the user's message to the chatbot & fetch its response
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(messageToChatbot)
        })
        .then(response => response.json())      // Then process the chatbot's response
        .then(data => {
            clearPriorUIElements();            // Remove previous UI elements (text input and buttons)
            addMessage(data.response, false); // Present the chatbot's text response message
            if (data.enableTextInput) {
                addOrderInput();
            }   
            addButtons(data.buttons);           // Present user intent buttons if provided by the chatbot
        })
        .catch(error => {                       // Something didn't work right - investigate
            console.error('Error:', error);
            addMessage('Sorry, something went wrong. Please try again.', false);
        });
    }

}); 