import time
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

login = input("Введите логин HTML Academy: ")
password = getpass.getpass("Введите пароль HTML Academy: ")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://htmlacademy.ru/login")


def set_text(input_form_id, value):
    email_elem = driver.find_element_by_id(input_form_id)
    email_elem.clear()
    email_elem.send_keys(value)


def sign_in():
    print('Логинюсь')
    set_text("login-email", login)
    set_text("login-password", password)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/input[3]').click()


def get_tasks_count():
    count = driver.find_element_by_xpath("/html/body/header/div/div/nav/div/div/span").text
    parts = count.split('/')
    return int(parts[1])


def solve_task():
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
        print('Произошла ошибка при решении')
        pass


def run_solve(count, trainer_url):
    for i in range(1, count):
        current_position = i
        now_url = trainer_url + "/" + str(current_position)
        print(now_url)
        driver.get(now_url)
        solve_task()


def get_trainer_links():
    print('Собираю ссылки на все тренажёры...')
    driver.get('https://htmlacademy.ru/courses')

    trainers_links = []
    all_links = driver.find_elements_by_tag_name('a')
    courses_links = []

    for link in all_links:
        courses_links.append(str(link.get_attribute('href')))

    courses_links = list(set(courses_links))

    for course_href in courses_links:
        if course_href.find('courses/') != -1:
            driver.get(course_href)
            course_page_links = driver.find_elements_by_tag_name('a')

            for page_link in course_page_links:
                href_page_link = str(page_link.get_attribute('href'))
                if href_page_link.find('continue/course/') != -1:
                    trainers_links.append(href_page_link)

    print('Будто бы всё собрал...')
    return list(set(trainers_links))


def solve():
    sign_in()
    print('Давай короче я погнал')
    for trainer_link in ['https://htmlacademy.ru/continue/course/79', 'https://htmlacademy.ru/continue/course/128',
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
                         'https://htmlacademy.ru/continue/course/213', 'https://htmlacademy.ru/continue/course/65']:
        driver.get(trainer_link)
        url = driver.current_url
        trainer_url = url[0:url.rfind('/')]
        count_tasks = get_tasks_count()
        run_solve(count_tasks, trainer_url)


solve()
