# Chat Interface para Agente de Bedrock

Esta aplicación web proporciona una interfaz de chat sencilla para interactuar con un agente de AWS Bedrock.

## Configuración

1. Clonar el repositorio
2. Instalar las dependencias:
   ```bash
   npm install
   ```

3. Configurar la URL de API Gateway en `app.js`:
   ```javascript
   const API_GATEWAY_URL = 'TU_API_GATEWAY_URL';
   ```

## Despliegue en AWS Amplify

1. Crear un nuevo repositorio en GitHub
2. Subir los archivos del proyecto
3. En AWS Amplify:
   - Crear una nueva aplicación
   - Conectar con el repositorio de GitHub
   - Configurar los siguientes entornos de construcción:
     ```yaml
     version: 1
     frontend:
       phases:
         preBuild:
           commands:
             - npm install
         build:
           commands:
             - npm run build
       artifacts:
         baseDirectory: /Users/karlos/CascadeProjects/Web
         files:
           - '**/*'
       cache:
         paths: []
     ```

## Requisitos

- Node.js
- AWS SDK
- API Gateway configurado
- Agente de Bedrock configurado (ID: U24XNO9ZZZ)
