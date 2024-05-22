# vts_controller.py
from rich.console import Console
import websockets
from utils.auth import authenticate
from utils.model_operations import get_available_models, load_model, move_model

class VTSLive2dPythonController:
    def __init__(self, vts_api_url: str, 
                 plugin_name: str, 
                 plugin_developer: str, 
                 plugin_icon_base64encoded: str = None):
        self.console = Console()
        self.vts_api_url = vts_api_url
        self.plugin_name = plugin_name
        self.plugin_developer = plugin_developer
        self.plugin_icon_base64encoded = plugin_icon_base64encoded
        self.websocket = None

        self.console.print(f"[bold cyan]VTS API URL: {self.vts_api_url}[/bold cyan]")
        self.console.print(f"[bold cyan]Plugin Name: {self.plugin_name}[/bold cyan]")
        self.console.print(f"Plugin Developer: {self.plugin_developer}")
        self.console.print(f"Plugin Icon Base64 Encoded: {self.plugin_icon_base64encoded}")

    async def connect(self):
        self.websocket = await websockets.connect(self.vts_api_url)

    async def close(self):
        if self.websocket:
            await self.websocket.close()

    async def authenticate(self):
        if await authenticate(self.websocket, self.plugin_name, self.plugin_developer, self.plugin_icon_base64encoded):
            self.console.print("[bold green]Authentication successful[/bold green]")
            return True
        else:
            self.console.print("[bold red]Authentication failed[/bold red]")
            return False

    async def get_available_models(self):
        models = await get_available_models(self.websocket)
        self.console.print("Available models:")
        for idx, model in enumerate(models):
            self.console.print(f"{idx + 1}: {model['modelName']} (ID: {model['modelID']})")
        return models

    async def load_model(self, model_id):
        response = await load_model(self.websocket, model_id)
        self.console.print(f"Load Model Response: {response}")

    async def move_model(self, position_x, position_y, rotation, size):
        response = await move_model(self.websocket, position_x, position_y, rotation, size)
        self.console.print(f"Move Model Response: {response}")
