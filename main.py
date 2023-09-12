import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import binance_api, tickers, telegram_bot_token
from functions import *

# Инициализация бота и диспетчера
bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Создаем кнопку с командой /get_prices
get_prices_button = types.KeyboardButton('/get_prices', )
# Создаем инлайн-клавиатуру и добавляем в нее кнопку
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(get_prices_button)


# Команда /get_prices
@dp.message_handler(commands=['get_prices'])
async def get_prices(message: types.Message):
    try:
        # Выполняем ваш код
        spot_client = get_client(binance_api)
        user_prices = get_user_prices(spot_client, tickers)

        # Преобразуем результат в строку для отправки пользователю
        result_string = '\n'.join(
            [f"<b>{symbol}</b> : {round(float(price), 2)}" for symbol, price in user_prices.items()])

        # Отправляем результат пользователю
        await message.reply(result_string, parse_mode='HTML')

    except Exception as e:
        logging.exception(e)
        await message.reply("Произошла ошибка при выполнении команды.")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
