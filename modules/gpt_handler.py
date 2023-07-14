# gpt_handler.py

import json
import os
import datetime
import requests
from modules.sms_handler import SmsHandler

class GptHandler:
    def default_gpt_response(sender_number, sender_message):
        # Return default answer 
        try:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": "Keep the response under 800 charactors"}, {"role": "user", "content": sender_message}],
                "temperature": 0.7,
            }
            gpt_prompt = GptHandler.generate_chat_gpt_response(payload)
            gpt_return = gpt_prompt.replace('\n', '').strip()
            SmsHandler.send_sms_response(sender_number, gpt_return)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Query Log, Date/Time: {current_time}, Sender Number: {sender_number}, Received Message: {sender_message}, Response: {gpt_return}")
                
        # Catch exceptions
        except Exception as ex:
            print('Exception:')
            print(ex)
            return 'Error', 500 


    def email_gpt_response(sender_number, sender_message):
        # Return special function if "email" is sent
        try:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": "Keep the response under 800 charactors"}, {"role": "user", "content": sender_message}],
                "temperature": 0.7,
            }
            gpt_prompt = GptHandler.generate_chat_gpt_response(payload)
            gpt_return = gpt_prompt.replace('\n', '').strip()
            SmsHandler.send_sms_response(sender_number, gpt_return)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Query Log, Date/Time: {current_time}, Sender Number: {sender_number}, Received Message: {sender_message}, Response: {gpt_return}")
                
        # Catch exceptions
        except Exception as ex:
            print('Exception:')
            print(ex)
            return 'Error', 500 


    def gpt4_gpt_response(sender_number, sender_message):
        # Return special function if "gpt4" is sent
        try:
            payload = {
                "model": "gpt-3.5-turbo", # change this to gpt4 when my account gets access
                "messages": [{"role": "system", "content": "Keep the response under 800 charactors"}, {"role": "user", "content": sender_message}],
                "temperature": 0.7,
            }
            gpt_prompt = GptHandler.generate_chat_gpt_response(payload)
            gpt_return = gpt_prompt.replace('\n', '').strip()
            SmsHandler.send_sms_response(sender_number, gpt_return)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Query Log, Date/Time: {current_time}, Sender Number: {sender_number}, Received Message: {sender_message}, Response: {gpt_return}")
                
        # Catch exceptions
        except Exception as ex:
            print('Exception:')
            print(ex)
            return 'Error', 500 


    def generate_chat_gpt_response(payload):
        # Send a POST request to the Chat GPT API with the received message
        api_key = os.environ.get('GPT_KEY')
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(payload))
        
        # Retrieve and return the generated response from the API
        if response.status_code == 200:
            generated_message = response.json()['choices'][0]['message']['content']
            complete_message = 'GPT: ' + generated_message
            return complete_message
        else:
            return 'An error occurred while generating the response.'