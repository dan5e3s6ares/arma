import asyncio
import logging


import uvicorn

from app.api import app as app_fastapi
from functions.syncronize import scheduler


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        """Handle exit signal"""
        print("@@@@@@@@@ Exit signal received @@@@@@@@@")
        return super().handle_exit(sig, frame)


async def main():

    server = Server(
        config=uvicorn.Config(
            app_fastapi, workers=1, loop="asyncio", use_colors=True, reload=True
        )
    )

    api = asyncio.create_task(
        server.serve()
    )  # esse pode ser duplicado com outro async task

    try:
        await asyncio.wait([api])  # aqui se adiciona outro async task
    except asyncio.CancelledError:
        api.cancel()  # Cancel the server task if a CancelledError is caught
        await api  # Wait for the server task to be cancelled


if __name__ == "__main__":
    # Print Rocketry's logs to terminal
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())

    # Run both applications
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, shutting down gracefully")
