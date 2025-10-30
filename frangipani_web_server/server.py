import json
import logging
import os
import uuid
from datetime import datetime

from aiohttp import web

from frangipani_web_server.configuration import WebServerConfiguration
from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.control.definition import WebControlDefinition
from frangipani_web_server.control.group import WebControlGroupDefinition

_logger = logging.getLogger("WebServer")


class FrangipaniWebServer:
    def __init__(self, configuration: WebServerConfiguration):
        self._configuration = configuration
        self._control_map: dict[str, WebControlDefinition] = {}
        self._clients = {}

        self._make_control_map(configuration.control_definitions)

    def _make_control_map(self, controls: list[BaseWebControlDefinition]):
        for control in controls:
            if isinstance(control, WebControlGroupDefinition):
                self._make_control_map(control.controls)

            elif isinstance(control, WebControlDefinition):
                if control.address in self._control_map:
                    raise ValueError(f"Control address '{control.address}' already exists in map")
                self._control_map[control.address] = control

    @staticmethod
    def _generate_client_id():
        """Generate a unique client ID"""
        timestamp = int(datetime.now().timestamp() * 1000)
        unique_id = str(uuid.uuid4())[:8]
        return f"client-{timestamp}-{unique_id}"

    async def _broadcast_update(self, message, sender_id):
        """Broadcast update to all connected clients except sender"""
        broadcast_msg = json.dumps({
            "type": "update",
            "address": message.address,
            "value": message.value,
            "senderId": sender_id
        })

        disconnected_clients = []
        for ws, client_id in list(self._clients.items()):
            if client_id != sender_id:
                try:
                    await ws.send_str(broadcast_msg)
                except Exception:
                    disconnected_clients.append(ws)

        # Clean up disconnected clients
        for ws in disconnected_clients:
            if ws in self._clients:
                del self._clients[ws]

    async def _websocket_handler(self, request):
        """Handle WebSocket connections"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        client_id = self._generate_client_id()
        self._clients[ws] = client_id

        _logger.info(f"Client connected: {client_id}")

        try:
            # Send initial state to new client
            init_msg = json.dumps({
                "type": "init",
                "clientId": client_id,
                "data": self._make_initial_data_from_state()
            })
            await ws.send_str(init_msg)

            # Handle messages from client
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)

                        if data.get("type") == "update":
                            # Update the control state
                            self._control_map[data.get("address")] = data.get("value")

                            # Broadcast update to all clients except sender
                            await self._broadcast_update(data, client_id)
                            _logger.debug(
                                f"Control updated: {data.get('controlId')} = "
                                f"{json.dumps(data.get('value'))} by {client_id}"
                            )

                    except json.JSONDecodeError:
                        print("Error parsing message: Invalid JSON")
                    except Exception as e:
                        print(f"Error processing message: {e}")

                elif msg.type == web.WSMsgType.ERROR:
                    _logger.warning(f'WebSocket error: {ws.exception()}')

        finally:
            if ws in self._clients:
                del self._clients[ws]

            _logger.info(f"Client disconnected: {client_id}")

        return ws

    async def _static_handler(self, request):
        """Serve static files"""
        path = request.match_info.get('path', 'index.html')

        if path == '':
            path = 'index.html'

        file_path = os.path.join(self._configuration.public_folder, path)

        if os.path.isfile(file_path):
            return web.FileResponse(file_path)
        else:
            return web.Response(status=404, text="File not found")

    async def init_app(self):
        """Initialize the web application"""
        app = web.Application()

        # Add routes
        app.router.add_get('/ws', self._websocket_handler)
        app.router.add_get('/', self._static_handler)
        app.router.add_get('/{path:.*}', self._static_handler)

        return app

    def _make_initial_data_from_state(self) -> dict:
        return {}

    def start(self):
        web.run_app(self.init_app(), host='0.0.0.0', port=8080)
