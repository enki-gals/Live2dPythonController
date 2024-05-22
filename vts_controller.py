# vts_controller.py
from rich.console import Console
from rich import print_json
import json
import websockets
from typing import List, Dict
from utils.auth import VTSAuthenticator
from utils.model_operations import VTSModelOperations

class VTSLive2dPythonController:
    def __init__(self, vts_api_url: str, 
                 plugin_name: str, 
                 plugin_developer: str, 
                 plugin_icon_base64encoded: str = None) -> None:
        self.console = Console()

        if not vts_api_url or not plugin_name or not plugin_developer:
            self.console.log("[bold red]VTS API URL, Plugin Name, and Plugin Developer are required[/bold red]")
            raise ValueError("VTS API URL, Plugin Name, and Plugin Developer are required")
        
        self.vts_api_url = vts_api_url
        self.plugin_name = plugin_name
        self.plugin_developer = plugin_developer
        self.plugin_icon_base64encoded = plugin_icon_base64encoded
        self.websocket = None
        self.model_id = None

        self.console.print(f"[bold cyan]VTS API URL: {self.vts_api_url}[/bold cyan]")
        self.console.print(f"[bold cyan]Plugin Name: {self.plugin_name}[/bold cyan]")
        self.console.print(f"Plugin Developer: {self.plugin_developer}")
        self.console.print(f"Plugin Icon Base64 Encoded: {self.plugin_icon_base64encoded}")

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.vts_api_url)

    async def close(self) -> None:
        if self.websocket:
            await self.websocket.close()

    async def authenticate(self) -> bool:
        if await VTSAuthenticator.authenticate(self.websocket, self.plugin_name, self.plugin_developer, self.plugin_icon_base64encoded):
            self.console.print("[bold green]Authentication successful[/bold green]")
            return True
        else:
            self.console.print("[bold red]Authentication failed[/bold red]")
            return False

    async def get_available_models(self) -> List[Dict[str, str]]:
        models = await VTSModelOperations.get_available_models(self.websocket)
        self.console.print("Available models:")
        for idx, model in enumerate(models):
            self.console.print(f"{idx + 1}: {model['modelName']} (ID: {model['modelID']})")
        return models

    async def load_model(self, model_id: str) -> None:
        response = await VTSModelOperations.load_model(self.websocket, model_id)
        self.model_id = model_id
        print_json(json.dumps(response))

    async def move_model(self, position_x: float, position_y: float, rotation: float, size: float) -> None:
        response = await VTSModelOperations.move_model(self.websocket, position_x, position_y, rotation, size)
        self.console.print(f"Move Model Response: {response}")  

    async def get_hotkeys(self, model_id: str = None) -> List[Dict[str, str]]:
        response = await VTSModelOperations.get_hotkeys(self.websocket, model_id)
        return response

    async def trigger_hotkey(self, hotkey_id: str) -> None:
        response = await VTSModelOperations.trigger_hotkey(self.websocket, hotkey_id)
        self.console.print(f"Trigger Hotkey Response: {response}")
