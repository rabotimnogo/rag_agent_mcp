import asyncio
from src.workers.worker import Worker


async def main():
    worker = Worker()
    await worker.run()
    print("Rabotaet")


if __name__ == "__main__":
    asyncio.run(main())
