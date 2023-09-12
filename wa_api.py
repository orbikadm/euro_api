import requests
import json


def send_message(message, wa_tel, wa_id_instans, wa_api_token_instance):
    url = f'https://api.green-api.com/waInstance{wa_id_instans}/sendMessage/{wa_api_token_instance}'
    chat_id = wa_tel + '@c.us'
    
    payload = {
        'chatId': chat_id,
        'message': message
        }
    
    json_payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json_payload)
    return response.text

