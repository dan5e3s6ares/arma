import datetime
import json

import aiofiles
import aiohttp
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import yaml
from functions.url_handle import UrlHandler
from yaml import Loader

jobstores = {"default": MemoryJobStore()}

# Initialize an AsyncIOScheduler with the jobstore
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Asia/Kolkata")


async def download_file(download_url: str, file_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as response:
            if response.status != 200:
                raise Exception("Got non-200 response!")

            async with aiofiles.open("files/" + file_name, "wb") as file:
                async for data, _ in response.content.iter_chunks():
                    await file.write(data)


def convert_datetime(obj):
    """
    Custom function to convert datetime objects to strings
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


class Jobs:
    data = {}

    @classmethod
    def set_data(cls, data: dict):
        cls.data = data

    @classmethod
    async def scheduled_job_2_update(cls):
        if "mock_api_swaggerUrl" in cls.data:
            await download_file(
                cls.data["mock_api_swaggerUrl"], file_name="openapi.json"
            )
        elif "mock_api_swaggerYamlUrl" in cls.data:
            await download_file(
                cls.data["mock_api_swaggerYamlUrl"], file_name="openapi.yaml"
            )

        with open('files/openapi.yaml') as fpi:
            data = yaml.load(fpi, Loader)
        # Apply the conversion function recursively
        json_data = json.dumps(data, default=convert_datetime, indent=4)

        with open("files/openapi.json", 'w') as fpo:
            fpo.write(json_data)

        print("Job scheduled")
        UrlHandler.sync()
