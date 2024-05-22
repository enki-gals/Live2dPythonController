# utils/auth.py
from utils.websocket_sender import VTubeStudioAPIWebsocketSender

async def request_auth_token(websocket, plugin_name, plugin_developer, plugin_icon):
    auth_token_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "requestToken",
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": plugin_name,
            "pluginDeveloper": plugin_developer,
            "pluginIcon": plugin_icon
        }
    }
    auth_token_response = await VTubeStudioAPIWebsocketSender.send_request(
        websocket, auth_token_request)
    return auth_token_response["data"]["authenticationToken"]

async def authenticate(websocket, plugin_name, plugin_developer, plugin_icon):
    authentication_token = await request_auth_token(websocket, plugin_name, plugin_developer, plugin_icon)
    auth_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "authenticate",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": plugin_name,
            "pluginDeveloper": plugin_developer,
            "authenticationToken": authentication_token
        }
    }
    auth_response = await VTubeStudioAPIWebsocketSender.send_request(
        websocket, auth_request)
    
    return auth_response.get("data", {}).get("authenticated", False)
