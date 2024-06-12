import boto3
import os

def lambda_handler(event, context):
    # Initialize a Pinpoint client
    pinpoint_client = boto3.client('pinpoint', region_name='us-east-1')

    # Define the message parameters
    application_id = os.environ['PINPOINT_APPLICATION_ID']  # Set this in the Lambda environment variables
    destination_number = event['destination_number']
    message = event['message']

    try:
        # Send the message
        response = pinpoint_client.send_messages(
            ApplicationId=application_id,
            MessageRequest={
                'Addresses': {
                    destination_number: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message,
                        'MessageType': 'TRANSACTIONAL'
                    }
                }
            }
        )

        # Log the response
        print(response)

        return {
            'statusCode': 200,
            'body': f"Message sent to {destination_number}"
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': f"Failed to send message: {str(e)}"
        }
