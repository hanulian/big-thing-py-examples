from big_thing_py.utils.common_util import *
from big_thing_py.utils.json_util import *

# from matter_server.server.server import MatterServer
# from matter_server.client.client import MatterClient

from func_timeout import func_timeout, FunctionTimedOut
from dataclasses import dataclass


import websockets
import sys
import tty
import termios
import asyncio


DEFAULT_STORAGE_PATH = os.path.join(get_project_root(), '.test_matter_server')
DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1
DEFAULT_WEBSOCKET_PORT = 5580


def getch() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


@dataclass
class WebsocketRequest:
    command: str
    id: str
    async_result_queue: asyncio.Queue
    result_queue: Queue


class WebSocketClient:
    def __init__(self, loop: asyncio.AbstractEventLoop, url: str) -> None:
        self._loop = loop
        self._url = url
        self._connected = False

        self._request_id = 0

    def connect(self, timeout: float = 0.5) -> bool:
        async def connect_async():
            try:
                async with websockets.connect(self._url):
                    return True
            except Exception as e:
                print(f"Connection failed: {e}")
                self._connected = False
                return False

        try:
            return asyncio.run(asyncio.wait_for(connect_async(), timeout))
        except asyncio.TimeoutError:
            print("Connection attempt timed out")
            self._connected = False
            return False
        except Exception as e:
            print(f"Connection failed: {e}")
            self._connected = False
            return False

    def sync_send_request(self, command: dict, timeout: float = 10) -> Union[dict, bool]:
        def wrapper(command: dict) -> Union[dict, bool]:
            self._request_id += 1

            while not self._loop.is_running():
                time.sleep(THREAD_TIME_OUT)

            command_str = json.dumps(command)
            request = WebsocketRequest(command_str, self._request_id, asyncio.Queue(), Queue())
            self._loop.call_soon_threadsafe(self._loop.create_task, self.async_send_request(request))
            self._loop.call_soon_threadsafe(self._loop.create_task, self.async_get_request_result(request))
            result = request.result_queue.get()
            return result

        try:
            return func_timeout(timeout, wrapper, args=(command,))
        except FunctionTimedOut:
            return False
        except Exception as e:
            print(e)
            return False

    async def async_send_request(self, request: WebsocketRequest):
        async with websockets.connect(self._url) as websocket:
            # Send your WebSocket request here
            await websocket.send(request.command)
            print(f"Send response for Request ID: {request.id}")

            # Receive the response
            await websocket.recv()
            result = await websocket.recv()
            await request.async_result_queue.put(result)

    async def async_get_request_result(self, request: WebsocketRequest):
        result = await request.async_result_queue.get()
        print(f"Get response for Request ID: {request.id}, Result: {result}")
        request.result_queue.put(result)


# def run_matter_server(
#     storage_path: str = DEFAULT_STORAGE_PATH,
#     vendor_id: int = DEFAULT_VENDOR_ID,
#     fabric_id: int = DEFAULT_FABRIC_ID,
#     websocket_port: int = DEFAULT_WEBSOCKET_PORT,
#     clean_start: bool = False,
# ) -> Tuple[MatterServer, WebSocket]:
#     def wrapper(
#         matter_server: MatterServer,
#         storage_path: str = DEFAULT_STORAGE_PATH,
#         vendor_id: int = DEFAULT_VENDOR_ID,
#         fabric_id: int = DEFAULT_FABRIC_ID,
#         websocket_port: int = DEFAULT_WEBSOCKET_PORT,
#         clean_start: bool = False,
#     ) -> None:
#         try:
#             logging.basicConfig(level='INFO')
#             coloredlogs.install(level='INFO')

#             if os.path.isdir(storage_path) and clean_start:
#                 shutil.rmtree(storage_path)

#             if not os.path.isdir(storage_path):
#                 os.makedirs(storage_path, exist_ok=True)

#             default_http_url = f'http://127.0.0.1:{websocket_port}/ws'
#             matter_server = MatterServer(storage_path, vendor_id, fabric_id, websocket_port)

#             async def run_matter():
#                 await matter_server.start()

#                 url = default_http_url
#                 async with aiohttp.ClientSession() as session:
#                     async with MatterClient(url, session) as client:
#                         await client.start_listening()

#             # async def handle_stop(loop: asyncio.AbstractEventLoop):
#             #     """Handle server stop."""
#             #     await matter_server.stop()

#             asyncio.run(run_matter())
#         except Exception as e:
#             print(e)
#             return

#     matter_server: MatterServer = None
#     matter_server_thread = MXThread(
#         target=wrapper,
#         args=(
#             matter_server,
#             storage_path,
#             vendor_id,
#             fabric_id,
#             websocket_port,
#             clean_start,
#         ),
#     )
#     matter_server_thread.start()

#     while True:
#         try:
#             websocket_client = create_sync_websocket_client(f"ws://127.0.0.1:{websocket_port}/ws")
#             websocket_client.recv()
#             break
#         except Exception as e:
#             print(e)
#             time.sleep(0.5)
#             continue

#     return matter_server, websocket_client


def convert_to_int(value):
    try:
        if isinstance(value, str) and value.startswith("0x"):
            return int(value, 16)
        return int(value)
    except (ValueError, TypeError):
        return None


def get_ipv4_address(addresses: List[str]) -> str:
    for addr in addresses:
        addr: str = addr
        if addr.count('.') == 3:
            return addr


if __name__ == '__main__':
    pass
