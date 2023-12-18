import json
import requests
from bs4 import BeautifulSoup
import pprint
import re
import boto3
from datetime import datetime

def get_url(url):
        
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        next_page = soup.find('li', class_='next')
        if next_page and next_page.find('a'):
            next_page_url = next_page.find('a').get('href')
            
            return next_page_url
        
        else:
            return False
    

def get_events(url):
            
    response = requests.get(url)
    events_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        events = soup.find_all('div', class_='scdBox')
        
        for event in events:
            event_data = {
                'id': clean_text(event.get('id')),
                'title': clean_text(event.find('p', class_='title').get_text()) if event.find('p', class_='title') else 'No Title',
                'date': clean_text(event.find('p', class_='date').get_text()) if event.find('p', class_='date') else 'No Date',
                'venue': clean_text(event.find('h3', class_='place').get_text()) if event.find('h3', class_='place') else 'No Venue'
            }
            table = event.find('table')
            if table:
                event_data['info'] = clean_text(table.find('th', string='INFO').find_next_sibling('td').get_text()) if table.find('th', string='INFO') else 'No Info'
                event_data['time'] = clean_text(table.find('th', string='TIME').find_next_sibling('td').get_text()) if table.find('th', string='TIME') else 'No Time'
                event_data['ticket'] = clean_text(table.find('th', string='TICKET').find_next_sibling('td').get_text()) if table.find('th', string='TICKET') else 'No Ticket'
                event_data['act'] = clean_text(table.find('th', string='ACT').find_next_sibling('td').get_text()) if table.find('th', string='ACT') else 'No Act'
            else:
                event_data['info'] = event_data['time'] = event_data['ticket'] = event_data['act'] = 'Not Available'

            events_data.append(event_data)  
            
        return events_data
    
    else:
        return {'status': 'failed', 'message': f'Error : get_events'}

def clean_text(text):
    # Remove newline characters
    text = text.replace('\n', ' ')
    # Remove other special characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def put_s3(json_data):
    
    s3 = boto3.client('s3')
    
    BUCKET_NAME = "scraping-morimoto"

    now = datetime.now()
    file_name = now.strftime("kolokol/data_%Y-%m-%d_%H-%M-%S.json")
    
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json_data)
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def hello(event, context):

    urls = ["https://kolokol-official.com/schedule/"]
    
    # 対象リンクの取得
    for i in range(5):
        
        result_url = get_url(urls[i])
        
        if result_url != False:
            urls.append(result_url)
        else:
            # print("break",i)
            break
    
    # 対象リンクのイベント情報の取得
    result = []
    for url in urls:
        result += get_events(url)
        
    json_data = json.dumps(result, ensure_ascii=False, indent=2, default=str)

    # S3に保存
    status = put_s3(json_data)
    
    if status:
        return {
            'statusCode': 200,
            'body': json_data
        }
    else:
        return {
            'statusCode': 500,
            'body': json_data
        }

if __name__ == "__main__":
    # ローカルテスト用
    hello('', '')