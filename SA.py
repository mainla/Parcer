from multiprocessing import Pool
import xlrd
import xlwt
from datetime import datetime
import requests
from bs4 import BeautifulSoup
g_links = []
g_data= []
wb = xlwt.Workbook()
ws = wb.add_sheet('data')
 


def get_html(url):
    response = requests.get(url)
    return response.text

# 1
def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('section', class_='section_allnews').find_all('div', class_='allnews_item')
    
    for td in tds:
        a = td.find('a', class_='ani-postname').get('href')
        link =  a
        g_links.append(link)
 
    return g_links


def text_before_word(text, word):
    line = text.split(word)[0].strip()
    return line


def get_page_data(html,link):
    soup = BeautifulSoup(html, 'lxml')
    try:
        article = soup.find('article', class_='news_container') 
        dec1 = article.select_one('div', class_='article-menu_base')
        dec1.decompose()
        dec1 = article.select_one('div', class_='article_date')
        dec1.decompose()
        dec1 = article.select_one('section', class_='comments_all')
        dec1.decompose()
        #tag = article.find_all(text='\n')
        #tag.replace_with(" ")
    except:
        article = soup.find('div', class_='double_right')
    try:
        name = article.find('h1').text
    except:
        name = ''
    try:
        data =  article.text
        data=data.replace( '\n', " ")
        data=data.replace( '  ', " ")
    except:
        data = ''

    data = {'name': name,
            'link': link,
            'data': data}
    g_data.append(data)
    return data


def write_xls(data):
 
    global_iterator=1
    for rec in data:
        ws.write(global_iterator,1,rec['name'])
        ws.write(global_iterator,2,rec['link'])
        ws.write(global_iterator,3,rec['data'])
        global_iterator =  global_iterator+1

    wb.save('xl_rec.xls') 

#    with open('coinmarketcap.xlsx', 'a') as f:
#            writer = csv.writer(f)
#   
#            writer.writerow((data['name'],
#                             data['link'],
#                             data['data'])) 


def make_all(link):
    html = get_html(link)
    data = get_page_data(html,link)
    


def main():
    start = datetime.now()
    for number in range(1 , 47):
        url = 'https://banks.cnews.ru/archive/date_01.01.2019_31.12.2019/type_top_lenta_articles/section_54/page_'+ str(number)
        all_links = get_all_links(get_html(url))
 
    c=1
    for l in all_links:
        print(c)
        make_all(l)
        c=c+1
    
    end = datetime.now()
    write_xls(g_data)
    total = end - start
    
    print(str(total))
     


if __name__ == '__main__':
     main()