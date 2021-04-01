import time
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

login = input("Введите логин HTML Academy: ")
password = getpass.getpass("Введите пароль HTML Academy: ")
trainer = input("Введите ссылку на тренажер, котоорый хотите пройти: ")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://htmlacademy.ru/login")

def set_text(input_form_id, value):
    email_elem = driver.find_element_by_id(input_form_id)
    email_elem.clear()
    email_elem.send_keys(value)

def sign_in():
    set_text("login-email", login)
    set_text("login-password", password)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/input[3]').click()

def get_trainer_path():
    url_parts = trainer.split('/')
    if url_parts[len(url_parts) - 1].isdigit():
        del url_parts[-1]
        return '/'.join(url_parts)
    else:
        return trainer

def get_tasks_count():
    count = driver.find_element_by_xpath("/html/body/header/div/div/nav/div/div/span").text
    parts = count.split('/')
    return int(parts[1])

def solve_task():
    try:
        driver.find_element_by_xpath("/html/body/main/div[1]/article/div[2]/div/button").click()     
        driver.find_element_by_css_selector("body > main > div.course-container__inner > article > div.course-layout__column.course-layout__column--left > div.course-editor-controls > button.course-editor-controls__item.course-editor-controls__item--answer").click()
        time.sleep(30)
    except:
        print('Пороизошла ошибка при решении')
        pass

def open_task(position):
    trainer_url = get_trainer_path()
    now_url = trainer_url + "/" + str(position)
    print('Открываю первую страницу курса')
    driver.get(now_url)

def run_solve(count):
    trainer_url = get_trainer_path()
    for i in range(1, count):
        current_position = i
        now_url = trainer_url + "/" + str(current_position)
        print(now_url)
        driver.get(now_url)
        solve_task()
        is_last = i == count
        print("Решил задачу #" + str() + "Иду дальше" if is_last else "Закончил")

sign_in()
open_task(1)
count_tasks = get_tasks_count()
run_solve(count_tasks)