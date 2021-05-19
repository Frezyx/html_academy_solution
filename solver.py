import getpass
from os import environ

import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

login = environ.get('LOGIN', None)
password = environ.get('PASSWORD', None)

if login is None:
    login = input("Введите логин HTML Academy: ")
if password is None:
    password = getpass.getpass("Введите пароль HTML Academy: ")

# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Firefox()
driver.get("https://htmlacademy.ru/login")


def set_text(input_form_id, value):
    global driver

    email_elem = driver.find_element_by_id(input_form_id)
    email_elem.click()
    email_elem.clear()
    email_elem.send_keys(value)


def sign_in():
    global driver

    print('Логинюсь')
    set_text("login-email", login)
    set_text("login-password", password)
    submit = driver.find_element_by_css_selector(".button--full-width[type='submit']")
    submit.click()


def get_tasks_count():
    global driver

    count_elem = driver.find_element_by_css_selector(".course-nav__stat")
    count_text = count_elem.text
    parts = count_text.split('/')
    return int(parts[1])


def solve_task():
    global driver

    waiter15 = WebDriverWait(driver, 15)
    waiter40 = WebDriverWait(driver, 40)

    locator = ('UNDEFINED', 'UNDEFINED')

    try:
        locator = (By.CSS_SELECTOR, ".course-theory__close.icon-close")
        close = waiter15.until(EC.visibility_of_element_located(locator))
        close.click()

        locator = (By.CSS_SELECTOR, ".course-editor-controls__item--answer")
        show_answer = waiter15.until(EC.visibility_of_element_located(locator))
        # warning: костыль против "element is not clickable because another element obscures it"
        driver.execute_script("arguments[0].click();", show_answer)

        waiter40.until(EC.text_to_be_present_in_element(locator, "Показать ответ"))
    except TimeoutException:
        print(f"Время ожидания элемента '{locator[1]}' вышло")
    except Exception as e:
        print(f"Произошла ошибка при решении: {e}")


def run_solve(count, trainer_url):
    global driver

    for i in range(1, count + 1):
        now_url = f"{trainer_url}/{i}"
        print(now_url)
        driver.get(now_url)
        solve_task()


def get_trainer_links():
    global driver

    print('Собираю ссылки на все тренажёры...')
    driver.get('https://htmlacademy.ru/courses')

    trainers_links = []
    all_links = driver.find_elements_by_tag_name('a')
    courses_links = []

    for link in all_links:
        courses_links.append(link.get_attribute('href'))

    courses_links = list(set(courses_links))

    for course_href in courses_links:
        if course_href.find('courses/') == -1:
            continue

        driver.get(course_href)
        course_page_links = driver.find_elements_by_tag_name('a')

        for page_link in course_page_links:
            href_page_link = page_link.get_attribute('href')
            if href_page_link.find('continue/course/') != -1:
                trainers_links.append(href_page_link)

    print('Будто бы всё собрал...')
    return list(set(trainers_links))


def solve():
    global driver

    sign_in()
    print('Давай короче я погнал')

    trainer_link = 'https://htmlacademy.ru/continue/course'

    links_id = [
        39, 42, 44, 45, 46, 50, 51, 53, 55, 57, 58, 65, 66, 70, 71, 73, 74, 76, 79, 80, 84, 85, 86, 88, 96, 97, 98,
        102, 103, 104, 113, 125, 128, 129, 130, 156, 157, 158, 165, 187, 195, 197, 199, 207, 209, 211, 213, 215, 217,
        219, 259, 269, 273, 297, 299, 301, 303, 305, 307, 309, 337, 339, 341, 343, 345, 347, 349, 351, 353, 355, 357,
        359, 365, 367
    ]

    for link_id in links_id:
        url = f'{trainer_link}/{link_id}'
        driver.get(url)

        url = driver.current_url
        count_tasks = get_tasks_count()

        trainer_url = url[:url.rfind('/')]
        run_solve(count_tasks, trainer_url)


if __name__ == '__main__':
    solve()
