import glob
import os
import urllib
import requests
import json
import pandas as pd
import xmltodict

url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
     
api_holiday_csv = {
    2016: '?'+ \
          'ServiceKey=' + 'OwKQ5qz1ZKYKUXeQQaq7u7yjxkj1WxKGs1viDKJXyTx6Nf4X7Wp1WAs4VjJwzZSj6kBVvdPELWBjheNSucXvlA%3D%3D' + \
          '&solYear=' + '2016'+'&numOfRows='+'100',
    2017: '?' + \
          'ServiceKey=' + 'OwKQ5qz1ZKYKUXeQQaq7u7yjxkj1WxKGs1viDKJXyTx6Nf4X7Wp1WAs4VjJwzZSj6kBVvdPELWBjheNSucXvlA%3D%3D' + \
          '&solYear=' + '2017'+'&numOfRows='+'100',
    2018: '?' + \
          'ServiceKey=' + 'OwKQ5qz1ZKYKUXeQQaq7u7yjxkj1WxKGs1viDKJXyTx6Nf4X7Wp1WAs4VjJwzZSj6kBVvdPELWBjheNSucXvlA%3D%3D' + \
          '&solYear=' + '2018'+'&numOfRows='+'100'}


def download_csv(start_year, end_year):
    for year in range(start_year, end_year + 1):
        # api 트래픽 초과 문제를 방지하기 위해서 csv 파일이있으면 다운받지않는다.
        if not os.path.isfile('./csv/holiday_temp/original/' + 'holiday_' + str(year) + '.csv') :
            result = requests.get(url + api_holiday_csv[year])
            resultcon = result.content
            jsonString = json.dumps(xmltodict.parse(resultcon), indent=4)
            js = json.loads(jsonString)
            data = pd.DataFrame(js["response"]['body']['items']['item'])
            data.to_csv('./csv/holiday_temp/original/' + 'holiday_' + str(year) + '.csv', index=False, encoding='UTF-8')


def data_processing(start_year, end_year):
    for year in range(start_year, end_year + 1):
        # 데이터 읽어오기
        data = pd.read_csv('./csv/holiday_temp/original/' + 'holiday_' + str(year) + '.csv', encoding='UTF-8')
        # 필요 없는 데이터 삭제
        data = data.drop(['dateKind'], axis=1)
        data = data.drop(['isHoliday'], axis=1)
        data = data.drop(['seq'], axis=1)

        data = data.rename({'locdate': 'date'}, axis='columns')
        data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')
        # CSV 파일 생성

        data.to_csv('./csv/holiday_temp/processed/' + 'holiday_' + str(year) + '.csv', index=False, encoding='UTF-8')


def merge_csv():
    input_file = r'./csv/holiday_temp/processed/'  # csv 파일들이 있는 디렉토리 위치
    output_file = r'./csv/holiday.csv'  # 병합하고 저장하려는 파일명
    all_file_list = glob.glob(os.path.join(input_file, '*'))  # glob 함수로 *로 시작하는 파일들을 모은다
    # print('합쳐질 CSV 파일 목록 : ' + str(all_file_list))
    all_data = []  # 읽어 들인 csv 파일 내용을 저장할 빈 리스트를 하나 만든다
    for file in all_file_list:
        df = pd.read_csv(file)  # for 구문으로 csv 파일들을 읽어 들인다
        all_data.append(df)  # 빈 리스트에 읽어 들인 내용을 추가한다

    data_combine = pd.concat(all_data, axis=0, ignore_index=True)  # concat 함수를 이용해서 리스트의 내용을 병합
    # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True 는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
    data_combine.to_csv(output_file, index=False, encoding='UTF-8')  # to_csv 함수로 저장한다. 인데스를 빼려면 False 로 설정
