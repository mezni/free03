import uuid
import asyncio


from src.database import init_db, get_session


async def main():
    await init_db()
    session = await get_session()


new_post_dto = PostDTO(
    user_id=1, title="First Post", content="This is the content of the first post"
)
asyncio.run(main())
