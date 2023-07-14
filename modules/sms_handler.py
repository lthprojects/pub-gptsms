# sms_handler.py

import os
import time
from azure.communication.sms import SmsClient

class SmsHandler:
    def send_sms_response(phone_number, message):
        try:
            endpoint_url = os.environ.get('COM_ENDPOINT')
            sms_client = SmsClient.from_connection_string(endpoint_url)
            message_groups = []

            if len(message) <= 160:
                # Send the message as is if it is 160 characters or less
                message_groups.append(message)
            elif len(message) / 160 > 5:
                # Return an error message if the message count is over five. Helps reduce sms cost
                error_message = "Error: Chat GPT's response was too long. Try refining your message."
                sms_responses = sms_client.send(
                    from_=os.environ.get('SMS_NUMBER'),
                    to=phone_number,
                    message=error_message
                )
                sms_response = sms_responses[0]

                if sms_response.successful:
                    print("Error message with message id {} was successfully sent to {}"
                        .format(sms_response.message_id, sms_response.to))
                else:
                    print("Error message failed to send to {} with the status code {} and error: {}"
                        .format(sms_response.to, sms_response.http_status_code, sms_response.error_message))
                
            else:
                # Split the message into ordered groups of no more than 160 characters
                num_groups = len(message) // 160 + 1
                for i in range(num_groups):
                    start_idx = i * 160
                    end_idx = (i + 1) * 160
                    sub_message = message[start_idx:end_idx]
                    message_groups.append(sub_message)
            
            for i, sub_message in enumerate(message_groups):
                sms_responses = sms_client.send(
                    from_=os.environ.get('SMS_NUMBER'),
                    to=phone_number,
                    message=sub_message
                )
                sms_response = sms_responses[0]
                
                if sms_response.successful:
                    print("Group {} of {} - Message with message id {} was successfully sent to {}"
                        .format(i+1, len(message_groups), sms_response.message_id, sms_response.to))
                else:
                    print("Group {} of {} - Message failed to send to {} with the status code {} and error: {}"
                        .format(i+1, len(message_groups), sms_response.to, sms_response.http_status_code, sms_response.error_message))
                
                # Pause for 1 second between sending each message to allow proper ordered delivery 
                time.sleep(1)
                
        except Exception as ex:
            print('Exception:')
            print(ex)