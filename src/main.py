from constants import TELEGRAM_BOT_TOKEN

from aiogram import Bot, Router, Dispatcher

from loguru import logger

bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()
router = Router()


@router.message()
async def echo(message):
    await message.answer(message.text)


dp.include_router(router)


async def main():
    logger.debug(f'start_polling')
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    logger.info(f'success')

    asyncio.run(main())
