import json
import os

from functions.endpoints_functions import FunctionsToEndpoints
from functions.syncronize import Jobs, scheduler
from functions.url_handle import UrlHandler

jobs = Jobs()


class ReadSettingsFile:

    @classmethod
    async def read_file(cls):
        f = open("./a_real_settings.json", "r", encoding="utf-8")
        data = json.loads(f.read())
        f.close()
        return data

    @classmethod
    async def read(cls):
        try:
            data = await cls.read_file()
            jobs.set_data(data)
            FunctionsToEndpoints.set_data(data)
            os.environ["TIME_TO_UPDATE"] = str(
                data.get("update_time_interval", "86400")
            )
            if int(os.environ["TIME_TO_UPDATE"]) > 0:
                scheduler.add_job(
                    jobs.scheduled_job_2_update,
                    "interval",
                    seconds=int(os.environ.get("TIME_TO_UPDATE", "86400")),
                    id="update_time_interval",
                )
                scheduler.start()
            data["update_on_start"] = data.get("update_on_start", False)
            if data["update_on_start"]:
                await cls.update_on_startup()
            else:
                UrlHandler.sync()

        except FileNotFoundError:
            print("Settings file not found")

    @classmethod
    async def update_on_startup(cls):
        print("Updating on startup")
        await jobs.scheduled_job_2_update()
