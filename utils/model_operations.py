# utils/model_operations.py
from utils.websocket_sender import VTubeStudioAPIWebsocketSender

async def get_available_models(websocket):
    models_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "getModels",
        "messageType": "AvailableModelsRequest"
    }
    models_response = await VTubeStudioAPIWebsocketSender.send_request(
        websocket, models_request)
    return models_response["data"]["availableModels"]

async def load_model(websocket, model_id):
    load_model_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "loadModel",
        "messageType": "ModelLoadRequest",
        "data": {
            "modelID": model_id
        }
    }
    load_model_response = await VTubeStudioAPIWebsocketSender.send_request(
        websocket, load_model_request)
    return load_model_response

async def move_model(websocket, position_x, position_y, rotation, size, time_in_seconds=0.2, values_are_relative=False):
    move_model_request = {
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
    move_model_response = await VTubeStudioAPIWebsocketSender.send_request(
        websocket, move_model_request)
    return move_model_response
