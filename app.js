// Configuración de AWS
const AWS = require('aws-sdk');
const axios = require('axios');

// Configuración de la región
AWS.config.update({
    region: 'us-east-1'
});

// Configuración de la API Gateway
const API_GATEWAY_URL = 'TU_API_GATEWAY_URL'; // Reemplazar con la URL de tu API Gateway

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
        const response = await axios.post(`${API_GATEWAY_URL}/chat`, {
            message: message,
            agentId: 'U24XNO9ZZZ'
        });
        
        const agentResponse = response.data.response;
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
