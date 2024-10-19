import time
import logging
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from parsel import Selector

logger = logging.getLogger(__name__)
handler = logging.FileHandler('bot.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)s - %(filename)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def task_dscr(auth):
    try:
        auth_username, auth_password, task_id = auth.split(' ')
    except ValueError:
        print('Ошибка поймана (некорректные данные)')
        logger.warning('Пользователь ввёл некорректные данные')
        return ValueError
    options = webdriver.ChromeOptions()
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")

    service = Service(path="./chromedriver-win64/chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://justtryhard.pythonanywhere.com/accounts/login/")
        if "Страница авторизации" not in driver.page_source:
            print('Ошибка поймана (нет соединения)')
            logger.error('Нет соединения с сервером')
            return HTTPError
        else:
            time.sleep(1)
            username_input = driver.find_element("id", "id_username")
            username_input.clear()
            username_input.send_keys(auth_username)
            time.sleep(1)
            password_input = driver.find_element("id", "id_password")
            password_input.clear()
            password_input.send_keys(auth_password)
            time.sleep(1)
            password_input.send_keys(Keys.ENTER)
            time.sleep(1)
            try:
                driver.get("https://justtryhard.pythonanywhere.com/work/%s" % task_id)
                if "Страница авторизации" in driver.page_source:
                    print('Ошибка поймана (авторизация)')
                    logger.warning('Пользователь не прошёл авторизацию')
                    return KeyError
                elif "Not Found" in driver.page_source:
                    print('Ошибка поймана (некорректный номер задачи)')
                    logger.warning('Пользователь ввёл несуществующий id задачи')
                    return KeyboardInterrupt
                else:
                    pass
            except HTTPError:
                logger.error('Отсутствует соединение с сервером')
                return HTTPError
            finally:
                pass

        time.sleep(1)
        sel = Selector(text=driver.page_source)
        parsed_elems = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-4')]")
        task_description = [x.text for x in parsed_elems]
        print('данные получены /', task_description)
        logger.info('Данные успешно получены с сервера')
        return task_description


    except Exception as ex:
        raise ex

    finally:
        driver.close()
        driver.quit()
