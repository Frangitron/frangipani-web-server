import json
import logging
import os
import uuid
from datetime import datetime

from aiohttp import web
from aiohttp.web_request import BaseRequest

from frangipani_web_server.configuration import WebServerConfiguration
from frangipani_web_server.control.store import ControlStore
from frangipani_web_server.message.base import BaseMessage
from frangipani_web_server.message.init import InitMessage
from frangipani_web_server.message.update import UpdateMessage

_logger = logging.getLogger("WebServer")


class FrangipaniWebServer:
    def __init__(self, configuration: WebServerConfiguration):
        self._public_folder = configuration.public_folder
        self._control_store = ControlStore(configuration.root_control_definition)
        self._message_callback = configuration.message_callback
        self._clients = {}

    def start(self):
        web.run_app(self._init_app(), host='0.0.0.0', port=8080)

    async def _init_app(self):
        """Initialize the web application"""
        app = web.Application()

        # Add routes
        app.router.add_get('/ws', self._websocket_handler)
        app.router.add_get('/', self._static_handler)
        app.router.add_get('/{path:.*}', self._static_handler)

        return app

    async def _broadcast_update(self, message: BaseMessage, current_client_id):
        """Broadcast update to all connected clients except sender"""
        disconnected_clients = []
        message_str = message.to_json()
        for ws, client_id in list(self._clients.items()):
            if client_id != current_client_id:
                try:
                    await ws.send_str(message_str)
                except Exception:
                    disconnected_clients.append(ws)

        for ws in disconnected_clients:
            if ws in self._clients:
                del self._clients[ws]

    async def _websocket_handler(self, request: BaseRequest):
        """Handle WebSocket connections"""
        websocket_response = web.WebSocketResponse()
        await websocket_response.prepare(request)

        client_id = self._generate_client_id()
        self._clients[websocket_response] = client_id

        _logger.info(f"Client connected: {client_id}")

        try:
            # Send initial state to the new client
            init_message = InitMessage(
                client_id = client_id,
                root_control_definition = self._control_store.get_updated_root_control()
            )
            await websocket_response.send_str(init_message.to_json())

            # Handle messages from the client
            async for raw_message in websocket_response:
                if raw_message.type == web.WSMsgType.TEXT:
                    message_data = json.loads(raw_message.data)
                    try:
                        if message_data['type'] == UpdateMessage.__name__:
                            update_message: UpdateMessage = UpdateMessage.from_dict(message_data)
                            self._control_store.update_control(
                                address=update_message.address,
                                value=update_message.value
                            )
                            if self._message_callback is not None:
                                self._message_callback(update_message)

                            await self._broadcast_update(update_message, client_id)

                        """
                        except json.JSONDecodeError:
                            _logger.warning("Error parsing message: Invalid JSON")
                        except Exception as e:
                            _logger.warning(f"Error processing message: {e}")
                        """
                    finally:
                        pass

                elif raw_message.type == web.WSMsgType.ERROR:
                    _logger.warning(f'WebSocket error: {websocket_response.exception()}')

        finally:
            if websocket_response in self._clients:
                del self._clients[websocket_response]

            _logger.info(f"Client disconnected: {client_id}")

        return websocket_response

    async def _static_handler(self, request):
        """Serve static files"""
        path = request.match_info.get('path', 'index.html')

        if path == '':
            path = 'index.html'

        file_path = os.path.join(self._public_folder, path)

        if os.path.isfile(file_path):
            return web.FileResponse(file_path)
        else:
            return web.Response(status=404, text="File not found")

    @staticmethod
    def _generate_client_id():
        """Generate a unique client ID"""
        timestamp = int(datetime.now().timestamp() * 1000)
        unique_id = str(uuid.uuid4())[:8]
        return f"client-{timestamp}-{unique_id}"
