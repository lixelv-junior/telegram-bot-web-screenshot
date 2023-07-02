from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import db
from url import *

sql = db.SQL('data.db')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--force-dark-mode')

driver = webdriver.Chrome(options=chrome_options)

bot = Bot(token='6208866169:AAHTOFINke2k21UzkkQHiBdkfUQPuVTtwR4')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    if sql.is_new_user(message.from_user.id):
        sql.add_user(message.from_user.id, message.from_user.username)
    await message.reply("Привет! Я бот.")


@dp.message_handler(commands=['d', 'doc', 'document', 'p', 'ph', 'photo'])
async def handle_text(message: types.Message):
    msg = await message.reply('Обработка запроса...')
    try:
        screenshot = capture_full_page_screenshot(driver, message.get_args(),
                                     path=f'image/{message.from_user.id}',
                                     width=sql.select_width(message.from_user.id))
        await msg.delete()

        if message.get_command() in ['/p', '/ph', '/photo']:
            await message.reply_photo(photo=open(screenshot[0], 'rb'),
                                      caption=f'[{screenshot[2]}]({screenshot[1]})\n' \
                                      f'Время выполнения: {screenshot[3]}', parse_mode='MarkDown')
        else:
            await message.reply_document(document=open(screenshot[0], 'rb'), thumb=open(screenshot[0], 'rb'),
                                      caption=f'[{screenshot[2]}]({screenshot[1]})\n' \
                                      f'Время выполнения: {screenshot[3]}', parse_mode='MarkDown')
    except:

        await msg.delete()
        await message.reply('Ошибка')


if __name__ == '__main__':
    create_folder_if_not_exists('image')
    executor.start_polling(dp, skip_updates=True)
    driver.quit()
