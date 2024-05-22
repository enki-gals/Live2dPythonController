# example.py
import os
import asyncio
from dotenv import load_dotenv
from typing import List
from vts_controller import VTSLive2dPythonController
from rich.console import Console

async def main():
    console = Console()
    
    load_dotenv()
    VTS_API_URL = os.getenv("VTS_API_URL")
    PLUGIN_NAME = os.getenv("PLUGIN_NAME")
    PLUGIN_DEVELOPER = os.getenv("PLUGIN_DEVELOPER")
    PLUGIN_ICON_BASE64 = os.getenv("PLUGIN_ICON_BASE64", "")
    controller = VTSLive2dPythonController(
        vts_api_url=VTS_API_URL,
        plugin_name=PLUGIN_NAME,
        plugin_developer=PLUGIN_DEVELOPER,
        plugin_icon_base64encoded=PLUGIN_ICON_BASE64
    )

    await controller.connect()
    if await controller.authenticate():
        models = await controller.get_available_models()
        if models:
            selected_model_id = models[0]['modelID']  # Automatically select the first model for example
            console.log(selected_model_id)

            await controller.load_model(selected_model_id)
            await controller.move_model(position_x=0, position_y=0, rotation=30, size=-60)
            
            hotkeys = await controller.get_hotkeys(selected_model_id)
            print("Available hotkeys:")
            for hotkey in hotkeys:
                print(f"Name: {hotkey['name']}, Type: {hotkey['type']}, ID: {hotkey['hotkeyID']}")

            # Trigger the first hotkey as an example
            if hotkeys:
                hotkey_to_trigger = hotkeys[1]
                print(f"triggering hotkey {hotkey_to_trigger['name']}")
                await controller.trigger_hotkey(hotkey_id=hotkey_to_trigger["hotkeyID"])

    await controller.close()

if __name__ == "__main__":
    asyncio.run(main())
