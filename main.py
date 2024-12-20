import requests 
from bs4 import BeautifulSoup 
from bs4 import Tag
import json

file_json='data.json'
write_list=[]

def parse_hacker_news():
    link = 'https://news.ycombinator.com/'
    response = requests.get(link)
   
    if response.status_code != 200:
        print("Не удалось получить данные с сайта.")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.select('.athing')
    for index,item in enumerate(news_items):
        title_element=item.select_one(".titleline a")
        if title_element is None:
            print(f"Заголовок не найден!Для элемента:",{index+1})
            return 0
        title = title_element.get_text()
        subtext = item.find_next_sibling('tr').select_one('.subtext')
        if subtext:
            comments_link = subtext.find_all('a')[-1]
            comments_text = comments_link.get_text()
            if 'comment' in comments_text:
                comments_count=comments_text.split()[0]
            else:
                comments_count='0'
        else:
            comments_count = '0'  # Если комментариев нет, устанавливаем 0
        print(f"{index + 1}. Title: {title}; Comments: {comments_count};")

        news_mn= {"id":index+1,
                  "title":title,
                  "com": comments_count
                  }
        write_list.append(news_mn)
    with open(file_json, 'w', encoding='utf-8') as out_file:
        json.dump(write_list, out_file,ensure_ascii=False,indent=2)

parse_hacker_news()

def generate_html(data_file="data.json", template_file="template.html", output_file="index.html"):
    with open(data_file, "r", encoding="utf-8") as f:  # Загрузка данных из JSON
        hacker_news= json.load(f)


    with open(template_file, "r", encoding="utf-8") as f:  # Загрузка HTML-шаблона
        template = f.read()


    soup = BeautifulSoup(template, "html.parser")  # Парсинг шаблона
    container = soup.find("div", class_="place-here")  # Нахождение элемента для вставки таблицы

    if not container:
        raise ValueError("В шаблоне отсутствует элемент с классом 'place-here' для вставки таблицы.")
    

    table = Tag(name="table")  # Создание таблицы
    # Создание заголовков таблицы
    thead = Tag(name="thead") 
    tr_head = Tag(name="tr")
    headers = ["№", "News", "Comments"]
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)

    # Создание строк таблицы
    tbody = Tag(name="tbody")
    for idx, news in enumerate(hacker_news, start=1):
        tr = Tag(name="tr")

        td_num = Tag(name="td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_news = Tag(name="td")
        td_news.string = news["title"]
        tr.append(td_news)

        td_comments = Tag(name="td")
        td_comments.string = news["com"]  
        tr.append(td_comments)

        tbody.append(tr)
    table.append(tbody)

    #вставляем таблицу в шаблон
    container.append(table)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())


generate_html()
print("HTML файл создан!(index.html)")