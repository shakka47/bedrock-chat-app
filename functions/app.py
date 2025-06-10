import json
import os
import boto3
import logging
from botocore.exceptions import ClientError

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {event}")
        
        # Extraer el mensaje del evento
        body = json.loads(event['body'])
        message = body.get('message', '')
        
        if not message:
            logger.error("No message found in request")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
                },
                'body': json.dumps({
                    'error': 'No message provided'
                })
            }

        # CORRECCIÓN: Usar el cliente específico para agentes de Bedrock
        bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=os.environ['REGION'])
        
        logger.info(f"Using client: {bedrock_agent_runtime.meta.service_model.service_name}")
        
        # Preparar el payload para el agente
        payload = {
            "input": {
                "text": message
            }
        }
        
        logger.info(f"Sending message to agent: {message}")
        
        # Invocar el agente usando el método correcto
        response = bedrock.invoke_agent(
            agentId='U24XNO9ZZZ',
            input={
                "text": message
            }
        )
        
        logger.info("Received response from Bedrock")
        
        # Procesar la respuesta
        agent_response = json.loads(response['body'].read().decode())
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
            },
            'body': json.dumps({
                'response': agent_response
            })
        }
        
    except ClientError as e:
        logger.error(f"Bedrock API error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
