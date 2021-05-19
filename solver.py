from getpass import getpass
from os import environ

import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.webdriver import ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def init_driver():
    drivers_data = [
        ("Chrome", webdriver.Chrome, ChromeOptions),
        ("Firefox", webdriver.Firefox, FirefoxOptions),
        # etc
    ]

    for name, browser, options in drivers_data:
        try:
            options.headless = True
            driver = browser(options=options)
            return driver
        except Exception:
            continue
    raise Exception("Поддерживаемый браузер не найден")


def set_text(input_form_id, value):
    global driver

    email_elem = driver.find_element_by_id(input_form_id)
    email_elem.click()
    email_elem.clear()
    email_elem.send_keys(value)


def sign_in():
    global driver

    set_text("login-email", login)
    set_text("login-password", password)
    submit = driver.find_element_by_css_selector(".button--full-width[type='submit']")
    submit.click()


def get_tasks_count(trainer_url):
    global driver

    driver.get(trainer_url)

    count_elem = driver.find_element_by_css_selector(".course-nav__stat")
    parts = count_elem.text.split('/')
    return int(parts[1])


def solve_task(task_url):
    global driver

    driver.get(task_url)

    waiter15 = WebDriverWait(driver, 15)
    waiter40 = WebDriverWait(driver, 40)

    locator = (By.CSS_SELECTOR, ".course-theory__close.icon-close")
    close = waiter15.until(EC.visibility_of_element_located(locator))
    close.click()

    locator = (By.CSS_SELECTOR, ".course-editor-controls__item--answer")
    show_answer = waiter15.until(EC.visibility_of_element_located(locator))
    # warning: костыль против "element is not clickable because another element obscures it"
    driver.execute_script("arguments[0].click();", show_answer)

    waiter40.until(EC.text_to_be_present_in_element(locator, "Показать ответ"))


def solve_trainer_tasks(count, trainer_url):
    global driver

    for i in range(1, count + 1):
        task_url = f"{trainer_url}/{i}"
        print(task_url)
        try:
            solve_task(task_url)
        except TimeoutException:
            print("Время ожидания элемента вышло")
        except Exception as e:
            print(f"Произошла ошибка при решении: {e}")


def get_trainer_links_id():
    global driver

    print("Собираю ссылки на все тренажёры...")
    driver.get("https://htmlacademy.ru/courses")

    courses_links = (a.get_attribute("href") for a in driver.find_elements_by_tag_name("a"))
    courses_links = (course_link for course_link in courses_links if course_link.find("courses/") != -1)
    courses_links = set(courses_links)

    trainers_links = []
    for course_link in courses_links:
        driver.get(course_link)

        page_links = (a.get_attribute("href") for a in driver.find_elements_by_tag_name("a"))
        page_links = (page_link for page_link in page_links if page_link.find("continue/course/") != -1)

        trainers_links.extend(page_links)

    links_id = (int(link[link.rfind('/') + 1:]) for link in trainers_links)

    print("Будто бы всё собрал...")
    return sorted(set(links_id))


def solve():
    global driver

    print("Логинюсь")
    sign_in()

    print("Давай короче я погнал")

    trainer_template = "https://htmlacademy.ru/continue/course"

    links_id = [
        39, 42, 44, 45, 46, 50, 51, 53, 55, 57, 58, 65, 66, 70, 71, 73, 74, 76, 79, 80, 84, 85, 86, 88, 96, 97, 98,
        102, 103, 104, 113, 125, 128, 129, 130, 156, 157, 158, 165, 187, 195, 197, 199, 207, 209, 211, 213, 215, 217,
        219, 259, 269, 273, 297, 299, 301, 303, 305, 307, 309, 337, 339, 341, 343, 345, 347, 349, 351, 353, 355, 357,
        359, 365, 367
    ]

    for link_id in links_id:
        trainer_url = f'{trainer_template}/{link_id}'
        try:
            count_tasks = get_tasks_count(trainer_url)
        except Exception:
            print(f"Невозможно найти кол-во заданий ({trainer_url})")
            continue

        trainer_url = driver.current_url
        trainer_url = trainer_url[:trainer_url.rfind('/')]

        solve_trainer_tasks(count_tasks, trainer_url)


if __name__ == "__main__":
    login = environ.get("LOGIN", None)
    password = environ.get("PASSWORD", None)

    if login is None:
        login = input("Введите логин HTML Academy: ")
    if password is None:
        password = getpass("Введите пароль HTML Academy: ")

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = init_driver()
    driver.get("https://htmlacademy.ru/login")

    solve()
