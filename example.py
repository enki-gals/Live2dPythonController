# example.py
# An example code that uses the VTSLive2dPythonController class to connect to the VTube Studio API, authenticate, get available models, and load a model.

import os
import asyncio
from dotenv import load_dotenv
from typing import List
from vts_controller import VTSLive2dPythonController

async def main():
    load_dotenv()
    VTS_API_URL = os.getenv("VTS_API_URL")
    PLUGIN_NAME = os.getenv("PLUGIN_NAME")
    PLUGIN_DEVELOPER = os.getenv("PLUGIN_DEVELOPER")
    PLUGIN_ICON_BASE64 = os.getenv("PLUGIN_ICON_BASE64", "")

    controller:VTSLive2dPythonController = VTSLive2dPythonController(
        vts_api_url=VTS_API_URL,
        plugin_name=PLUGIN_NAME,
        plugin_developer=PLUGIN_DEVELOPER,
        plugin_icon_base64encoded=PLUGIN_ICON_BASE64
    )

    await controller.connect()
    if await controller.authenticate():
        models:List[str] = await controller.get_available_models()
        if models:
            selected_model_id:str = models[0]['modelID']  # Automatically select the first model for example
            await controller.load_model(selected_model_id)
            await controller.move_model(position_x=0, position_y=0, rotation=0, size=-60)
            action_list = await controller.get_action_list()
            await controller.activate_hotkey(expression_file_name=action_list[1]["file"])

            # Wait for 5 seconds
            await asyncio.sleep(5)
    await controller.close()

if __name__ == "__main__":
    asyncio.run(main())
