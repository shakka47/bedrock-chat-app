import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Extraer el mensaje del evento
        body = json.loads(event['body'])
        message = body.get('message', '')
        
        # Configurar el cliente de Bedrock
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ['REGION'])
        
        # Preparar el payload para el agente
        payload = {
            "input": {
                "text": message
            }
        }
        
        # Invocar el agente
        response = bedrock_runtime.invoke_agent(
            agentId=os.environ['AGENT_ID'],
            contentType='application/json',
            body=json.dumps(payload)
        )
        
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
                'response': agent_response['output']['text']
            })
        }
        
    except ClientError as e:
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
