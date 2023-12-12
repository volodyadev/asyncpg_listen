import asyncio
import asyncpg
import asyncpg_listen

from settings import settings


async def handle_notifications(
    notification: asyncpg_listen.NotificationOrTimeout,
) -> None:
    print(f"{notification} has been received")


async def main():
    listener = asyncpg_listen.NotificationListener(
        asyncpg_listen.connect_func(str(settings.db_url))
    )
    listener_task = asyncio.create_task(
        listener.run(
            {"simple": handle_notifications},
            policy=asyncpg_listen.ListenPolicy.LAST,
            notification_timeout=5,
        )
    )

    await asyncio.sleep(1)

    connection = await asyncpg.connect(str(settings.db_url))
    try:
        for i in range(1):
            await connection.execute(f"NOTIFY simple, '{i}'")
    finally:
        await connection.close()

    await asyncio.sleep(1)

    listener_task.cancel()


asyncio.run(main())
