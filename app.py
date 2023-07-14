from flask import Flask, request
from modules.gpt_handler import GptHandler
import os

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test_endpoint():
    return 'Success!', 200


@app.route('/incoming-sms', methods=['OPTIONS'])
def validate_webhook():
    response_headers = {
        'WebHook-Allowed-Origin': 'eventgrid.azure.net'
    }
    
    return '', 200, response_headers


@app.route('/incoming-sms', methods=['POST'])
def incoming_sms():
    data = request.get_json()
    sender_number = data['data']['from']
    sender_message = data['data']['message']
    auth_number = os.environ.get('AUTH_NUMBER')
    
    if sender_number == auth_number:
        try:    
            # Parse received messages 
            functions = {
                'email': GptHandler.email_gpt_response,
                'gpt4': GptHandler.gpt4_gpt_response if 'gpt4' in sender_message else GptHandler.default_gpt_response,
            }
            final = functions.get(sender_message, GptHandler.default_gpt_response)
            final(sender_number, sender_message)
            return '', 200
        except Exception as e:
            print(f"An error occurred: {e} data: {data}")
            return 'Error', 500
    else:
        try:
            GptHandler.default_gpt_response(sender_number, sender_message)
            return '', 200
        except Exception as e:
            print(f"An error occurred: {e} data: {data}")
            return 'Error', 500


if __name__ == '__main__':
    app.run()