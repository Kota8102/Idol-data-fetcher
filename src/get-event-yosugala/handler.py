import re
import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
import pprint

def get_event_links(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # イベント情報のリンクを取得
    live_url_list = []
    for link in soup.find_all('a'):
        if re.search('/live/', link.get('href')):
            live_url_list.append(base_url + link.get('href'))

    return live_url_list

def get_ticket_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ticket_link_element = soup.find('a', {'class': 'select_color_linktext'})
    if ticket_link_element:
        return ticket_link_element['href']
    else:
        return ""

def get_event_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h3')

    return title_element.text.strip()


def hello(event, context):

    try:
        base_url = 'https://yosugala2022.ryzm.jp'
        url = base_url + '/live?category_id=13477'

        all_event_links = []

        # ページのリンクを取得
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        event_links = soup.find_all('a', {'class': 'event-card__link'})
        for event_link in event_links:
            all_event_links.append(event_link['href'])

        while url:
            all_event_links.extend(get_event_links(url, base_url))

            # 次のページのリンクを取得
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            next_page = soup.find('button', {'aria-label': 'Go to next page'})
            
            if next_page:
                current_page = re.search(r'page=(\d+)', url)
                if current_page:
                    next_page_number = int(current_page.group(1)) + 1
                else:
                    next_page_number = 2
                url = f"{base_url}/live?category_id=13477&page={next_page_number}"
            else:
                url = None
            
        result = []
        for link in all_event_links:
            info = {}
            html_text = requests.get(link).text
            soup = BeautifulSoup(html_text, 'html.parser')
            tableview = soup.find('ul', class_='tableview')

            for li in tableview.find_all('li', class_='w20'):
                key = li.text.strip()
                value = li.find_next_sibling('li', class_='w80').text.strip()
                info[key] = value
                
             # タイトルを取得
            info['title'] = get_event_title(link)
            
            info['link'] = get_ticket_link(link)
            result.append(info)


        json_data = json.dumps(result, ensure_ascii=False, indent=2, default=str)

        pprint.pprint(json_data)

        # S3にput
        s3 = boto3.client('s3')
        BUCKET_NAME = "scraping-morimoto"

        now = datetime.now()
        file_name = now.strftime("yosugala/data_%Y-%m-%d_%H-%M-%S.json")
        
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json_data)

        # Lambdaのレスポンス
        response_body = json.dumps(result, ensure_ascii=False, indent=2)
        response = {
                'statusCode': 200,
                'body': response_body
        }

    except Exception as e:
        # construct error response object
        response_body = f'Error: {str(e)}'
        response = {
            'statusCode': 500,
            'body': response_body
        }


    return response

if __name__ == "__main__":

    # ローカルでテストする際に使えるサンプルイベントとコンテキスト
    sample_event = {}  # サンプルイベントデータを入力
    sample_context = None  # サンプルコンテキストデータを入力

    # ローカルで関数をテスト
    result = hello(sample_event, sample_context)
    print(result)