# utils/auth.py
# Proceed authentication with the VTube Studio API at the initial phasei of the connection.

import websockets
from utils.websocket_sender import VTubeStudioAPIWebsocketSender
from typing import Dict, Any

class VTSAuthenticator:

    # Request an authentication token from the VTube Studio API
    @staticmethod
    async def request_auth_token(websocket: websockets.WebSocketClientProtocol, 
                                 plugin_name: str,
                                 plugin_developer: str, 
                                 plugin_icon: str) -> str:
        auth_token_request:Dict[str, Any] = {
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
        auth_token_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=auth_token_request)
        return auth_token_response["data"]["authenticationToken"]

    @staticmethod
    async def authenticate(websocket: websockets.WebSocketClientProtocol, 
                           plugin_name: str, 
                           plugin_developer: str, 
                           plugin_icon: str) -> bool:
        authentication_token:str = await VTSAuthenticator.request_auth_token(websocket=websocket, 
                                                                             plugin_name=plugin_name, 
                                                                             plugin_developer=plugin_developer, 
                                                                             plugin_icon=plugin_icon)
        auth_request:Dict[str, Any] = {
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
        auth_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=auth_request)

        return auth_response.get("data", {}).get("authenticated", False)
