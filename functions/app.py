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

        # Configurar el cliente de Bedrock
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ['REGION'])
        
        # Preparar el payload para el agente
        payload = {
            "input": {
                "text": message
            }
        }
        
        logger.info(f"Sending message to agent: {message}")
        
        # Invocar el agente
        response = bedrock_runtime.invoke_agent(
            agentId=os.environ['AGENT_ID'],
            contentType='application/json',
            body=json.dumps(payload)
        )
        
        logger.info("Received response from agent")
        
        # Procesar la respuesta
        agent_response = json.loads(response['body'].read().decode())
        
        if 'output' not in agent_response or 'text' not in agent_response['output']:
            logger.error(f"Invalid response format: {agent_response}")
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
                },
                'body': json.dumps({
                    'error': 'Invalid response from agent'
                })
            }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'
            },
            'body': json.dumps({
                'response': agent_response['output']['text']
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
                'error': 'Internal server error'
            })
        }
