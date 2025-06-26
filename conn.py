import requests
from config import DefaultConfig
from botbuilder.schema import Activity, ActivityTypes, Attachment

def init_sessions(user_id):
    url = DefaultConfig.get_url(user_id)
    response = requests.post(url, headers=DefaultConfig.HEADERS)
    return response


def delete_sessions(user_id):
    url = DefaultConfig.get_url(user_id)
    response = requests.delete(url, headers=DefaultConfig.HEADERS)
    return response


def _handle_func_resp(name, response):
    if name == "plot_tool" and response.get('status', 'error') == "success":
        return response.get('data_url')
    
         
def prompt(user_id, message):
    
    response = requests.post(
        url=DefaultConfig.PROMPT_ENDPOINT,
        headers=DefaultConfig.HEADERS,
        json={
        "appName": DefaultConfig.AGENT_NAME,
        "userId": user_id,
        "sessionId": DefaultConfig.SESSION_ID,
        "newMessage": {
            "role": "user",
            "parts": [{
            "text": message
            }]
        }
    })
    
    if response.status_code != 200:
        raise Exception(response.content)

    reply = Activity(type=ActivityTypes.message)

    results = []
    for r in response.json():
        
        contents = r['content']['parts'][0]
        author = r['author']

        if 'functionResponse' in contents.keys():
            function_response = contents['functionResponse']
            name = function_response['name']
            result = function_response['response']
            out = _handle_func_resp(name, result)
                        
            if out:
                event = {
                    "author": author,
                    "type": name,
                    "value": out
                }
                
                reply.attachments = [
                    Attachment(
                        name="architecture-resize.png",
                        content_type="image/png",
                        content_url=out,
                    )
                ]

        elif 'text' in contents.keys():
            text = contents['text']
            event = {
                "author": author,
                "type": "text",
                "value": text
            }
            reply.text = text               
            results.append(event)
    
    
    return reply
    

if __name__ == "__main__":
    r = init_sessions("maju-mds9")
    print(r.json())

    r = prompt("maju-mds9", "Can you plot me the volume forecast for retail in 2023?")
    print(r)
    
    r = delete_sessions("maju-mds9")
    