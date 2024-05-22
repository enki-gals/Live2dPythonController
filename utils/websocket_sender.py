# utils/websocket_sender.py
import json
from typing import Dict, Any
import websockets

class VTubeStudioAPIWebsocketSender:
    @staticmethod
    async def send_request(websocket: websockets.WebSocketClientProtocol,
                           payload: Dict[str, Any]) -> Dict[str, Any]:
        if payload is None:
            raise ValueError("payload is necessary")

        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        return json.loads(response)
