import aiofiles
import aiohttp
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

jobstores = {"default": MemoryJobStore()}

# Initialize an AsyncIOScheduler with the jobstore
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Asia/Kolkata")


async def download_file(download_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as response:
            if response.status != 200:
                raise Exception("Got non-200 response!")

            async with aiofiles.open("files/openapi.json", "wb") as file:
                async for data, _ in response.content.iter_chunks():
                    await file.write(data)


class Jobs:
    data = {}

    @classmethod
    def set_data(cls, data: dict):
        cls.data = data

    @classmethod
    async def scheduled_job_2_update(cls):
        print(cls.data["mock_api"])
        await download_file(cls.data["mock_api"])
        print("Job scheduled")
