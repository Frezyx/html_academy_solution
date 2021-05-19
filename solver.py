import threading
import time
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

bad_urls = []

urls = ['https://htmlacademy.ru/continue/course/79', 'https://htmlacademy.ru/continue/course/128',
        'https://htmlacademy.ru/continue/course/349', 'https://htmlacademy.ru/continue/course/84',
        'https://htmlacademy.ru/continue/course/217', 'https://htmlacademy.ru/continue/course/80',
        'https://htmlacademy.ru/continue/course/53', 'https://htmlacademy.ru/continue/course/343',
        'https://htmlacademy.ru/continue/course/157', 'https://htmlacademy.ru/continue/course/337',
        'https://htmlacademy.ru/continue/course/74', 'https://htmlacademy.ru/continue/course/299',
        'https://htmlacademy.ru/continue/course/351', 'https://htmlacademy.ru/continue/course/359',
        'https://htmlacademy.ru/continue/course/199', 'https://htmlacademy.ru/continue/course/73',
        'https://htmlacademy.ru/continue/course/85', 'https://htmlacademy.ru/continue/course/44',
        'https://htmlacademy.ru/continue/course/219', 'https://htmlacademy.ru/continue/course/303',
        'https://htmlacademy.ru/continue/course/113', 'https://htmlacademy.ru/continue/course/129',
        'https://htmlacademy.ru/continue/course/259', 'https://htmlacademy.ru/continue/course/269',
        'https://htmlacademy.ru/continue/course/66', 'https://htmlacademy.ru/continue/course/88',
        'https://htmlacademy.ru/continue/course/365', 'https://htmlacademy.ru/continue/course/71',
        'https://htmlacademy.ru/continue/course/125', 'https://htmlacademy.ru/continue/course/130',
        'https://htmlacademy.ru/continue/course/96', 'https://htmlacademy.ru/continue/course/98',
        'https://htmlacademy.ru/continue/course/51', 'https://htmlacademy.ru/continue/course/103',
        'https://htmlacademy.ru/continue/course/195', 'https://htmlacademy.ru/continue/course/50',
        'https://htmlacademy.ru/continue/course/211', 'https://htmlacademy.ru/continue/course/45',
        'https://htmlacademy.ru/continue/course/341', 'https://htmlacademy.ru/continue/course/305',
        'https://htmlacademy.ru/continue/course/357', 'https://htmlacademy.ru/continue/course/273',
        'https://htmlacademy.ru/continue/course/76', 'https://htmlacademy.ru/continue/course/156',
        'https://htmlacademy.ru/continue/course/209', 'https://htmlacademy.ru/continue/course/215',
        'https://htmlacademy.ru/continue/course/197', 'https://htmlacademy.ru/continue/course/86',
        'https://htmlacademy.ru/continue/course/353', 'https://htmlacademy.ru/continue/course/339',
        'https://htmlacademy.ru/continue/course/55', 'https://htmlacademy.ru/continue/course/42',
        'https://htmlacademy.ru/continue/course/97', 'https://htmlacademy.ru/continue/course/104',
        'https://htmlacademy.ru/continue/course/301', 'https://htmlacademy.ru/continue/course/355',
        'https://htmlacademy.ru/continue/course/39', 'https://htmlacademy.ru/continue/course/345',
        'https://htmlacademy.ru/continue/course/102', 'https://htmlacademy.ru/continue/course/367',
        'https://htmlacademy.ru/continue/course/46', 'https://htmlacademy.ru/continue/course/187',
        'https://htmlacademy.ru/continue/course/57', 'https://htmlacademy.ru/continue/course/207',
        'https://htmlacademy.ru/continue/course/70', 'https://htmlacademy.ru/continue/course/165',
        'https://htmlacademy.ru/continue/course/158', 'https://htmlacademy.ru/continue/course/297',
        'https://htmlacademy.ru/continue/course/347', 'https://htmlacademy.ru/continue/course/58',
        'https://htmlacademy.ru/continue/course/307', 'https://htmlacademy.ru/continue/course/309',
        'https://htmlacademy.ru/continue/course/213', 'https://htmlacademy.ru/continue/course/65']
proc_count = os.cpu_count()
splitted = [urls[i:i + proc_count] for i in range(0, len(urls), proc_count)]

login = input("Введите логин HTML Academy: ")
password = getpass.getpass("Введите пароль HTML Academy: ")
print("Введите количество ядер для работы (максимальное кол-во ядер вашей системы - " + str(proc_count) + "):")
t_count = int(input())
if t_count > proc_count:
    t_count = proc_count
if t_count < 1:
    t_count = 1


def set_text(input_form_id, value, driver):
    email_elem = driver.find_element_by_id(input_form_id)
    email_elem.clear()
    email_elem.send_keys(value)


def sign_in(driver):
    print('Логинюсь')
    set_text("login-email", login, driver)
    set_text("login-password", password, driver)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/input[3]').click()


def get_tasks_count(driver):
    try:
        count = driver.find_element_by_xpath("/html/body/header/div/div/nav/div/div/span").text
        parts = count.split('/')
        return int(parts[1])
    except:
        urls.append(driver.current_url)
        return 0


def solve_task(driver):
    try:
        driver.find_element_by_xpath("/html/body/main/div[1]/article/div[2]/div/button").click()
        show_answer = driver.find_element_by_css_selector(
            "body > main > div.course-container__inner > article > "
            "div.course-layout__column.course-layout__column--left > div.course-editor-controls > "
            "button.course-editor-controls__item.course-editor-controls__item--answer")
        show_answer.click()

        while True:
            if show_answer.text == 'Показать ответ':
                break
            time.sleep(1)
    except:
        bad_urls.append(driver.current_url)
        print('Произошла ошибка при решении')
        pass


def run_solve(count, trainer_url, driver):
    for i in range(1, count):
        current_position = i
        now_url = trainer_url + "/" + str(current_position)
        print(now_url)
        driver.get(now_url)
        solve_task(driver)

def do_work_in_thread(cutted_urls):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=2')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get("https://htmlacademy.ru/login")
    sign_in(driver)
    for trainer_link in cutted_urls:
        driver.get(trainer_link)
        url = driver.current_url
        trainer_url = url[0:url.rfind('/')]
        count_tasks = get_tasks_count(driver)
        run_solve(count_tasks, trainer_url, driver)


def solve():
    print('Давай короче я погнал')
    threads = []
    for i in range(0, t_count):
        x = threading.Thread(target=do_work_in_thread, args=(splitted[i],))
        threads.append(x)
        x.start()
    for x in threads:
        x.join()
    print(bad_urls)


solve()
