import asyncio
import websockets
import json

VTS_API_URL = "ws://localhost:33333"
PLUGIN_NAME = "My Cool Plugin"
PLUGIN_DEVELOPER = "My Name"
PLUGIN_ICON = ""  # Optionally, provide a base64 encoded icon

async def send_request(websocket, request):
    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    return json.loads(response)

async def authenticate(websocket):
    # Request an authentication token
    auth_token_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "requestToken",
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": PLUGIN_NAME,
            "pluginDeveloper": PLUGIN_DEVELOPER,
            "pluginIcon": PLUGIN_ICON
        }
    }
    auth_token_response = await send_request(websocket, auth_token_request)
    authentication_token = auth_token_response["data"]["authenticationToken"]

    # Authenticate with the token
    auth_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "authenticate",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": PLUGIN_NAME,
            "pluginDeveloper": PLUGIN_DEVELOPER,
            "authenticationToken": authentication_token
        }
    }
    auth_response = await send_request(websocket, auth_request)
    if auth_response.get("data", {}).get("authenticated", False):
        print("Authentication successful")
    else:
        print("Authentication failed")
        return False
    return True

async def get_available_models(websocket):
    models_request = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "getModels",
        "messageType": "AvailableModelsRequest"
    }
    models_response = await send_request(websocket, models_request)
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
    load_model_response = await send_request(websocket, load_model_request)
    print(f"Load Model Response: {load_model_response}")

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
    move_model_response = await send_request(websocket, move_model_request)
    print(f"Move Model Response: {move_model_response}")

async def main():
    async with websockets.connect(VTS_API_URL) as websocket:
        # Authenticate
        if not await authenticate(websocket):
            return

        # Get available models
        models = await get_available_models(websocket)
        print("Available models:")
        for idx, model in enumerate(models):
            print(f"{idx + 1}: {model['modelName']} (ID: {model['modelID']})")

        # Select a model
        model_index = int(input("Enter the number of the model you want to load: ")) - 1
        selected_model = models[model_index]

        # Load the selected model
        await load_model(websocket, selected_model["modelID"])

        # Move the selected model
        position_x = float(input("Enter the X position to move the model to (-1000 to 1000): "))
        position_y = float(input("Enter the Y position to move the model to (-1000 to 1000): "))
        rotation = float(input("Enter the rotation angle for the model (-360 to 360): "))
        size = float(input("Enter the size for the model (-100 to 100): "))
        await move_model(websocket, position_x, position_y, rotation, size)

# Run the main function
asyncio.run(main())
