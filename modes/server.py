
import threading
import time
import uvicorn

from modes.api import app


def start_api_server():
    """Start FastAPI in a background thread."""

    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="error",
        access_log=False,
        log_config=None
    )

    server = uvicorn.Server(config)

    thread = threading.Thread(
        target=server.run,
        daemon=True
    )

    thread.start()

    # Wait for the API server to start
    for _ in range(100):
        if server.started:
            print("API server started successfully!")
            return True

        if not thread.is_alive():
            print("API server failed to start!")
            return False

        time.sleep(0.1)

    print("API server startup timed out!")
    return False
