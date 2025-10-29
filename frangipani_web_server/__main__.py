import sys
from datetime import datetime
import json
import os
import uuid

from aiohttp import web


with open("controls.json", "r") as f:
    controls_definitions = json.load(f)


# Store connected clients
clients = {}


def generate_client_id():
    """Generate a unique client ID"""
    timestamp = int(datetime.now().timestamp() * 1000)
    unique_id = str(uuid.uuid4())[:8]
    return f"client-{timestamp}-{unique_id}"


def update_control(control_id, value):
    """Update control value in state"""

    def find_and_update(controls):
        for control in controls:
            if control.get("id") == control_id:
                if isinstance(value, dict):
                    control.update(value)
                else:
                    control["value"] = value
                return True

            if "controls" in control and isinstance(control["controls"], list):
                if find_and_update(control["controls"]):
                    return True

        return False

    find_and_update(controls_definitions["controls"])


async def broadcast_update(msg, sender_id):
    """Broadcast update to all connected clients except sender"""
    broadcast_msg = json.dumps({
        "type": "update",
        "controlId": msg.get("controlId"),
        "value": msg.get("value"),
        "senderId": sender_id
    })

    disconnected_clients = []
    for ws, client_id in list(clients.items()):
        if client_id != sender_id:
            try:
                await ws.send_str(broadcast_msg)
            except Exception:
                disconnected_clients.append(ws)

    # Clean up disconnected clients
    for ws in disconnected_clients:
        if ws in clients:
            del clients[ws]


async def websocket_handler(request):
    """Handle WebSocket connections"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client_id = generate_client_id()
    clients[ws] = client_id

    print(f"Client connected: {client_id}")

    try:
        # Send initial state to new client
        init_msg = json.dumps({
            "type": "init",
            "clientId": client_id,
            "data": controls_definitions
        })
        await ws.send_str(init_msg)

        # Handle messages from client
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)

                    if data.get("type") == "update":
                        # Update the control state
                        update_control(data.get("controlId"), data.get("value"))

                        # Broadcast update to all clients except sender
                        await broadcast_update(data, client_id)

                        print(
                            f"Control updated: {data.get('controlId')} = {json.dumps(data.get('value'))} by {client_id}")

                except json.JSONDecodeError:
                    print("Error parsing message: Invalid JSON")
                except Exception as e:
                    print(f"Error processing message: {e}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f'WebSocket error: {ws.exception()}')

    finally:
        if ws in clients:
            del clients[ws]
        print(f"Client disconnected: {client_id}")

    return ws


async def static_handler(request):
    """Serve static files"""
    path = request.match_info.get('path', 'index.html')

    if path == '':
        path = 'index.html'

    file_path = os.path.join(sys.argv[1], path)

    if os.path.isfile(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(status=404, text="File not found")


async def init_app():
    """Initialize the web application"""
    app = web.Application()

    # Add routes
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/', static_handler)
    app.router.add_get('/{path:.*}', static_handler)

    return app


if __name__ == "__main__":
    web.run_app(init_app(), host='0.0.0.0', port=8080)
