# vts_controller.py
from rich.console import Console
from rich import print_json
import json
import sys
import websockets
from typing import List, Dict, Any
from utils.auth import VTSAuthenticator
from utils.model_operations import VTSModelOperations

# VTSLive2dPythonController class to connect to the VTube Studio API, authenticate, get available models, and load a model.
# The users utilize this class to interact with the VTube Studio API conveniently.
class VTSLive2dPythonController:
    def __init__(self, vts_api_url: str, 
                 plugin_name: str, 
                 plugin_developer: str, 
                 plugin_icon_base64encoded: str = None) -> None:
        self.console = Console()

        # VTS API URL, Plugin Name, and Plugin Developer are required.
        # If not, it's unable to continue the process.
        if not vts_api_url or not plugin_name or not plugin_developer:
            self.console.log("[bold red]VTS API URL, Plugin Name, and Plugin Developer are required[/bold red]")
            sys.exit(1)
        
        self.vts_api_url:str                                        = vts_api_url               # VTube Studio API URL
        self.plugin_name:str                                        = plugin_name               # Plugin Name
        self.plugin_developer:str                                   = plugin_developer          # Plugin Developer
        self.plugin_icon_base64encoded:str                          = plugin_icon_base64encoded # Plugin Icon Base64 Encoded
        self.websocket:websockets.BasicAuthWebSocketServerProtocol  = None                      # Websocket connection to the VTube Studio API
        self.model_id:str                                           = None                      # Model ID that this controller is handling

        self.console.print(f"[bold cyan]VTS API URL: {self.vts_api_url}[/bold cyan]")
        self.console.print(f"[bold cyan]Plugin Name: {self.plugin_name}[/bold cyan]")
        self.console.print(f"Plugin Developer: {self.plugin_developer}")
        self.console.print(f"Plugin Icon Base64 Encoded: {self.plugin_icon_base64encoded}")

    # Connect to the VTube Studio API
    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.vts_api_url)

    # Close the connection to the VTube Studio API
    async def close(self) -> None:
        if self.websocket:
            await self.websocket.close()

    # Authenticate with the VTube Studio API
    async def authenticate(self) -> bool:
        if await VTSAuthenticator.authenticate(self.websocket, self.plugin_name, self.plugin_developer, self.plugin_icon_base64encoded):
            self.console.print("[bold green]Authentication successful[/bold green]")
            return True
        else:
            self.console.print("[bold red]Authentication failed[/bold red]")
            return False

    # Get available models from VTube Studio
    async def get_available_models(self) -> List[str]:
        models = await VTSModelOperations.get_available_models(websocket=self.websocket)
        self.console.print("Available models:")
        for idx, model in enumerate(models):
            self.console.print(f"{idx + 1}: {model['modelName']} (ID: {model['modelID']})")
        return models

    # Load a model in VTube Studio
    async def load_model(self, model_id:str) -> None:
        response = await VTSModelOperations.load_model(websocket=self.websocket, 
                                                       model_id=model_id)
        self.model_id = model_id
        print_json(json.dumps(response))

    # Move a model in VTube Studio
    async def move_model(self, position_x:float, position_y:float, rotation:float, size:float) -> None:
        response = await VTSModelOperations.move_model(websocket=self.websocket, 
                                                       position_x=position_x, 
                                                       position_y=position_y, 
                                                       rotation=rotation, 
                                                       size=size)
        self.console.print(f"Move Model Response: {response}")  

    # Get the hotkeys from VTube Studio
    async def get_action_list(self) -> List[Dict[str, str]]:
        response = await VTSModelOperations.get_action_list(websocket=self.websocket,
                                                            model_id=self.model_id)
        return response

    # Requesting activation of a hotkey in VTube Studio (activate action)
    async def activate_hotkey(self, expression_file_name:str) -> None:
        response = await VTSModelOperations.activate_hotkey(websocket=self.websocket,
                                                            expression_file_name=expression_file_name)
        self.console.log(f"Activating action: {expression_file_name}")
        self.console.print(f"Trigger Action Response: {response}")

    # Requesting deactivation of a hotkey in VTube Studio (deactivate action)
    async def deactivate_hotkey(self, expression_file_name:str) -> None:
        response = await VTSModelOperations.deactivate_hotkey(websocket=self.websocket,
                                                              expression_file_name=expression_file_name)
        self.console.log(f"Deactivating action: {expression_file_name}")
        self.console.print(f"Trigger Action Response: {response}")