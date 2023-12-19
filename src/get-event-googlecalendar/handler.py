import json
import pprint
import datetime
import boto3
from google.oauth2 import service_account
from googleapiclient.discovery import build

REGION = "ap-northeast-1"
PARAM_KEY = "Google-API-Credential"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def write_S3(file_name, result):
    
    s3 = boto3.client('s3')
    BUCKET_NAME = "scraping-morimoto"
    
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json.dumps(result, indent=4, ensure_ascii=False))

def get_parameters(param_key):
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']


def hello(event, context):
    
    param_value = get_parameters(PARAM_KEY)

    service_account_info = json.loads(param_value)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    
    # Get data
    now = datetime.datetime.now()
    one_month_ago = (now - datetime.timedelta(days=30)).replace(day=1)
    timefrom = one_month_ago.strftime('%Y/%m/%d')
    
    # Call the Calendar API
    # timefrom = '2022/12/01'
    # timeto = '2023/10/01'
    timefrom = datetime.datetime.strptime(timefrom, '%Y/%m/%d').isoformat()+'Z'
    # timeto = datetime.datetime.strptime(timeto, '%Y/%m/%d').isoformat()+'Z'
    
    # calendarId = 'titlemitei0516@gmail.com'
    calendarlist = {
        'titlemitei0516@gmail.com' : 'titlemitei', 
        'ae2otho4itddl355860ln6v9pk@group.calendar.google.com': 'fishbowl', 
        'norarikurari.idol.official@gmail.com':'norarikurari',
        'ringwanderungofficial@gmail.com':'ringwanderung',
        'de66k8m4kmclrvep77k72aqap8@group.calendar.google.com': 'satorimonster',
        'situasion.cal@gmail.com': 'situasion',
        '0aqcmh216ds0io58kt6nu43g2s@group.calendar.google.com': 'theorchestratokyo',
        'tiptoe.open.schedule@gmail.com': 'tiptoe',
        'vonoba20210216live@gmail.com': 'mirrormirror',
        'kastella.info@gmail.com': 'kasumisoutostella',
        'js18vn28l7sarq2euv74fv5gho@group.calendar.google.com': 'inuwasi'
        }

    for key, value in calendarlist.items():
        calendarId = key

        events_result = service.events().list(calendarId=calendarId,
                                            timeMin=timefrom,
                                            # timeMax=timeto,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
    
        file_name = now.strftime(value + "/data_%Y-%m-%d_%H-%M-%S.json")
        write_S3(file_name, events)

if __name__ == "__main__":
    # ローカルテスト用
    hello('', '')