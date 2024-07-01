import json
import os

from functions.syncronize import Jobs, scheduler

jobs = Jobs()


class ReadSettingsFile:

    @classmethod
    async def read(cls):
        try:
            f = open("./a_real_settings.json", "r", encoding="utf-8")
            data = json.loads(f.read())
            f.close()
            print("Settings file found")

            jobs.set_data(data)
            os.environ["TIME_TO_UPDATE"] = str(data["update_time_interval"])
            if data["update_time_interval"] > 0:
                scheduler.add_job(
                    jobs.scheduled_job_2_update,
                    "interval",
                    seconds=int(os.environ.get("TIME_TO_UPDATE", "86400")),
                    id="update_time_interval",
                )
                scheduler.start()
            if data["update_on_start"]:
                await cls.update_on_startup()

        except FileNotFoundError:
            print("Settings file not found")

    @classmethod
    async def update_on_startup(cls):
        print("Updating on startup")
        await jobs.scheduled_job_2_update()
