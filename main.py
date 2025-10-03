from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для проверки ника в PUBG по ID. Используй /checkpubgid <ID>, чтобы начать.')

async def check_pubg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text('Пожалуйста, укажите ID после команды /checkpubg. Например: /checkpubg 123456789')
        return

    pubg_id = context.args[0]

    if not pubg_id.isdigit() or len(pubg_id) != 10:
        await update.message.reply_text('ID должен состоять ровно из 10 цифр. Пожалуйста, проверьте введенный ID.')
        return

    driver = None
    start_time = time.time()
    try:
        options = Options()
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.page_load_strategy = 'eager'
        options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.notifications": 2,
            "profile.managed_default_content_settings.media_stream": 2,
            "devtools.sendCdpCommand": [
                "Network.setBlockedURLs", {"urls": ["*midasbuy.com/act/pagedoo/*", "*sdk.js*", "*workbox-core.prod*", "*log_report_new*", "*js?id=G-NQXI2JD8STG*", "*query_midaspay_channel_list*"]}
            ]
        })
        driver = webdriver.Chrome(service=Service('C:/Users/crfyz/Desktop/213/chromedriver-win64/chromedriver.exe'), options=options)
        driver.get("https://www.midasbuy.com/midasbuy/ru/shop/pubgm")


        first_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div'))
        )
        first_button.click()

        id_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[5]/div[2]/div[1]/div[2]/div/div[2]/div/input'))
        )
        id_input.clear()
        id_input.send_keys(pubg_id)

        second_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[5]/div[2]/div[1]/div[3]/div/div'))
        )
        second_button.click()

        nickname_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/span[1]'))
        )
        nickname = nickname_element.text
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        await update.message.reply_text(f'Вы запросили ID: {pubg_id}. Ник в PUBG: {nickname}. Время парсинга: {duration} секунд.')

    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка при попытке взаимодействия с сайтом: {e}')
    finally:
        if driver:
            driver.quit()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Используй /checkpubgid <ID> для проверки ника.')


def main() -> None:
    application = Application.builder().token("8467753781:AAE0x4sDKCa-rmLf9GG6lQs1nT0OENUIClM").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("checkpubgid", check_pubg))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
