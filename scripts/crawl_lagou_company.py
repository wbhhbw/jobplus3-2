import requests
from requests.exceptions import RequestException
import json
import time


def get_one_page(url, page_num):
    data = {
        'first': 'false',
        'pn': page_num,
        'sortField': 0,
        'havemark': 0
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '39',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=ABAAABAAAFCAAEG44F469D9693F938B6981446500EB3532; _ga=GA1.2.535831419.1515669228; user_trace_token=20180111191351-80aa82e3-f6c0-11e7-8908-525400f775ce; LGUID=20180111191351-80aa85b9-f6c0-11e7-8908-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=index_navigation; _gid=GA1.2.559955599.1516280033; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515669229,1516280034; LGSID=20180118215449-263c5077-fc57-11e7-a4eb-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F80-0-0; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516285295; LGRID=20180118222142-e7e2d73f-fc5a-11e7-ab3d-525400f775ce',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/gongsi/80-0-0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print('connect error')


def parse_one_page(data):
    url_origin = 'www.lgstatic.com/thumbnail_200x200/'
    company_list = data['result']
    for company in company_list:
        yield {
            'logo_url': url_origin + company['companyLogo'],
            'company_name': company['companyShortName'],
            'field': company['industryField'],
            'financeStage': company['financeStage'],
            'companyFeatures': company['companyFeatures']
        }

def save_to_file(json_data):
    with open('company_detail.json', 'a') as f:
        f.write(json.dumps(json_data)+',')


def main():
    url = 'https://www.lagou.com/gongsi/80-0-0.json'
    count = 1
    with open('company_detail.json', 'a') as f:
        f.write('[')
    while count < 11:
        print('第%d批公司，抓取中...' % count)
        data = get_one_page(url, count)
        for company in parse_one_page(data):
            save_to_file(company)
        count += 1
        time.sleep(1)
    with open('company_detail.json', 'a') as f:
        f.write(']')
    print('抓取成功')


if __name__ == '__main__':
    main()
