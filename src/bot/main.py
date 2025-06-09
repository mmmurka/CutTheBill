from constrains import TELEGRAM_BOT_TOKEN

from aiogram import Bot, Router, Dispatcher

bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()
router = Router()


@router.message()
async def echo(message):
    await message.answer(message.text)


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
