# utils/websocket_sender.py
# Send requests to the VTube Studio API using websockets

import json
from typing import Dict, Any
import websockets

class VTubeStudioAPIWebsocketSender:

    @staticmethod
    async def send_request(websocket: websockets.WebSocketClientProtocol,
                           payload: Dict[str, Any]) -> Dict[str, Any]:
        if payload is None:
            raise ValueError("payload is necessary to send a request to the VTube Studio API.")

        await websocket.send(json.dumps(payload))
        response:str = await websocket.recv()
        return json.loads(response)
