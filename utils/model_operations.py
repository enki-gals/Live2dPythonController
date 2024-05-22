# utils/model_operations.py
# Conduct operations with models in VTube Studio using the VTube Studio API.

import websockets
import asyncio
import json
from typing import List, Dict, Any
from utils.websocket_sender import VTubeStudioAPIWebsocketSender

class VTSModelOperations:

    # Get available models from VTube Studio
    @staticmethod
    async def get_available_models(websocket: websockets.WebSocketClientProtocol) -> List[str]:
        models_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "getModels",
            "messageType": "AvailableModelsRequest"
        }
        models_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=models_request)
        return models_response["data"]["availableModels"]

    # Load a model in VTube Studio
    @staticmethod
    async def load_model(websocket: websockets.WebSocketClientProtocol, model_id: str) -> Dict[str, Any]:
        load_model_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "loadModel",
            "messageType": "ModelLoadRequest",
            "data": {
                "modelID": model_id
            }
        }
        load_model_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=load_model_request)
        return load_model_response

    # Move a model in VTube Studio
    @staticmethod
    async def move_model(websocket: websockets.WebSocketClientProtocol, 
                         position_x: float = 0, 
                         position_y: float = 0, 
                         rotation: float = 0, 
                         size: float = 0, 
                         time_in_seconds: float = 0.2, 
                         values_are_relative: bool = False) -> Dict[str, Any]:
        move_model_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "moveModel",
            "messageType": "MoveModelRequest",
            "data": {
                "timeInSeconds": time_in_seconds,
                "valuesAreRelativeToModel": values_are_relative,
                "positionX": position_x,
                "positionY": position_y,
                "rotation": rotation,
                "size": size
            }
        }
        move_model_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=move_model_request)
        return move_model_response

    # Requesting list of hotkeys available in current or other VTS model
    @staticmethod
    async def get_action_list(websocket: websockets.WebSocketClientProtocol,
                              model_id: str) -> List[Dict[str, str]]:
        hotkeys_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "getHotkeys",
            "messageType": "HotkeysInCurrentModelRequest",
            "data": {
                "modelID": model_id
            }
        }
        hotkeys_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=hotkeys_request)
        hotkeys_response = dict(hotkeys_response)
        response = hotkeys_response["data"]["availableHotkeys"]
        return response

    # Requesting activation of a hotkey in VTube Studio (action)
    @staticmethod 
    async def activate_hotkey(websocket: websockets.WebSocketClientProtocol,
                              expression_file_name: str) -> Dict[str, Any]:
        hotkey_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "triggerHotkey",
            "messageType": "ExpressionActivationRequest",
            "data": {
                "expressionFile": expression_file_name,
                "active": True
            }
        }

        hotkey_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=hotkey_request)
        return hotkey_response
    
    # Requesting deactivation of a hotkey in VTube Studio (action)
    @staticmethod
    async def deactivate_hotkey(websocket: websockets.WebSocketClientProtocol,
                                expression_file_name: str) -> Dict[str, Any]:
        hotkey_request:Dict[str, Any] = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "triggerHotkey",
            "messageType": "ExpressionActivationRequest",
            "data": {
                "expressionFile": expression_file_name,
                "active": False
            }
        }

        hotkey_response:Dict[str, Any] = await VTubeStudioAPIWebsocketSender.send_request(
            websocket=websocket,
            payload=hotkey_request)
        return hotkey_response