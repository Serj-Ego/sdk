import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36"
    }

    # region request
    # req = requests.get(url, headers)
    # print(req.text)

    # with open("lesson_03.html", "w") as file:
    #     file.write(req.text)
    # endregion

    with open("lesson_03.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    lis = soup.find_all("li", class_="news-listing__item")
    # print(lis)

    posts_urls = []
    # Получение тега "li"[пункт] из тега "ul"[лист] и сохранение ссылки в список
    for li in lis:
        post_url = li.find("a", class_="news-listing__item-link").get("href")
        # print(post_url)
        posts_urls.append(post_url)

    for url_one in posts_urls[0:1]:
        req = requests.get(url_one, headers=headers)
        post_name = url_one.split('/')[-1].split('.')[-2]

        # Запись новостной html страницы в каталог "data" и присвоение имени "post_name"
        with open(f"data/{post_name}.html", "w") as file:
            file.write(req.text)

        # Чтение записанной новостной html страницы с названием "post_name" из каталога "data"
        with open(f"data/{post_name}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        article__title = soup.find('h1', class_='article__title')
        article__body = soup.find_all('div', class_='article__body')

        print(article__title)
        print(article__body)


get_html("https://www.mk.ru/news/")
