// Configuración de la API Gateway
const API_GATEWAY_URL = 'https://mvpnys48v5.execute-api.us-east-1.amazonaws.com/prod/chat';

// Elementos del DOM
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Función para agregar un mensaje al chat
function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para enviar el mensaje al agente
async function sendMessage(message) {
    try {
        const response = await fetch(API_GATEWAY_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                agentId: 'U24XNO9ZZZ'
            })
        });
        
        if (!response.ok) {
            throw new Error('Error al enviar el mensaje');
        }
        
        const data = await response.json();
        const agentResponse = data.response;
        addMessage(agentResponse);
    } catch (error) {
        console.error('Error:', error);
        addMessage('Lo siento, ocurrió un error al procesar tu mensaje.');
    }
}

// Evento de envío de mensaje
sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';
        sendMessage(message);
    }
});

// Enviar mensaje con Enter
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
});
