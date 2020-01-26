import requests, json
import crawler
import schedule
import time


backend_pwd =''
app_username = ''
app_pwd = ''
appkey = ''
appid = ''
api_base = ''
token = None


def get_header(token=None):
    headers = {'Content-type': 'application/json',
                'X-LC-Id': appid,
                'X-LC-Key': appkey}
    if token:
        headers['X-LC-Session'] = token
    return headers

def login(username, pwd):
    data_json = json.dumps({"username":username, "password":pwd})
    r = requests.post('{}/1.1/login'.format(api_base), data_json, headers=get_header())
    result = json.loads(r.text)
    return result['sessionToken']


def get_batch_op_str(method, path, body):
    dict_op = dict()
    dict_op['method'] = method
    dict_op['path'] = path
    dict_op['body'] = body
    return dict_op


def postNews(news, token):
    all_requests = []
    for each_news in news:
        all_requests.append(get_batch_op_str('POST', '/1.1/classes/News', each_news))

    body = json.dumps({'requests':all_requests})
    headers = get_header(token)
    r = requests.post('{}/1.1/batch'.format(api_base), body, headers=headers)
    result = json.loads(r.text)
    print(result)


def job():
    token = login(app_username, backend_pwd)
    news = crawler.crawler_all()
    postNews(news, token)


def run():
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)



