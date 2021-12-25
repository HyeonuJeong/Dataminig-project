import pandas as pd
import glob
import os
import json
import requests

# 사과(400,411) : 후지(05), 상품(04)
# 배(400,412) : 신고(01), 상품(04)

api_apple_csv = {2016: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2016-01-01&p_endday=2016-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=411&p_kindcode=05&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json',
                 2017: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2017-01-01&p_endday=2017-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=411&p_kindcode=05&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json',
                 2018: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2018-01-01&p_endday=2018-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=411&p_kindcode=05&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json'}

api_pear_csv = {2016: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2016-01-01&p_endday=2016-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=412&p_kindcode=01&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json',
                2017: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2017-01-01&p_endday=2017-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=412&p_kindcode=01&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json',
                2018: 'https://www.kamis.or.kr/service/price/xml.do?' \
                    'action=periodProductList&p_productclscode=02&p_' \
                    'startday=2018-01-01&p_endday=2018-12-31&p_itemcategorycode=400' \
                    '&p_itemcode=412&p_kindcode=01&p_productrankcode=04&p_countrycode=1101' \
                    '&p_convert_kg_yn=Y&p_cert_key=941a94af-f1e8-4886-83c1-18123dbb5433' \
                    '&p_cert_id=1694&p_returntype=json'}


def download_csv(fruit_name, start_year, end_year):
    if fruit_name == 'apple':
        for year in range(start_year, end_year + 1):
            result = requests.get(api_apple_csv[year])
            js = json.loads(result.content)
            data = pd.DataFrame(js['data']['item'])
            data.to_csv('./csv/apple_temp/original/' + 'apple_' + str(year) + '.csv', index=False, encoding='UTF-8')

    elif fruit_name == 'pear':
        for year in range(start_year, end_year + 1):
            result = requests.get(api_pear_csv[year])
            js = json.loads(result.content)
            data = pd.DataFrame(js['data']['item'])
            data.to_csv('./csv/pear_temp/original/' + 'pear_' + str(year) + '.csv', index=False, encoding='UTF-8')


def data_processing(fruit_name, start_year, end_year):
    for year in range(start_year, end_year + 1):
        # 데이터 읽어오기
        data = pd.read_csv('./csv/' + str(fruit_name) + '_temp/original/' + str(fruit_name)+'_'
                           + str(year) + '.csv', encoding='UTF-8')

        # 필요 없는 데이터 삭제
        data = data.drop(['kindname'], axis=1)
        data = data.drop(['countyname'], axis=1)
        data = data.drop(['marketname'], axis=1)

        remove = data[data['itemname'] == '[]'].index
        data = data.drop(remove)
        data = data.drop(['itemname'], axis=1)

        # price 를 각 데이터 이름으로 변경
        if fruit_name == 'apple':
            data = data.rename({'price': 'apple_price'}, axis='columns')
        if fruit_name == 'pear':
            data = data.rename({'price': 'pear_price'}, axis='columns')

        # 날짜 형태 변환
        data['test'] = data['yyyy'].map(str) + "-" + data['regday'].map(str)
        data['date'] = data['test'].str.replace(pat='/', repl='-', regex=False)

        data = data.drop(['test'], axis=1)
        data = data.drop(['yyyy'], axis=1)
        data = data.drop(['regday'], axis=1)

        #data = data.fillna(method='ffill', limit=14)

        # CSV 파일 생성
        data.to_csv('./csv/' + str(fruit_name) + '_temp/processed/'+str(fruit_name) + '_'
                    + str(year) + '.csv', index=False, encoding='UTF-8')


def merge_csv(fruit_name):
    input_file = r'./csv/'+str(fruit_name)+'_temp/processed/'  # csv 파일들이 있는 디렉토리 위치
    output_file = r'./csv/'+str(fruit_name)+'.csv'  # 병합하고 저장하려는 파일명
    all_file_list = glob.glob(os.path.join(input_file, '*'))  # glob 함수로 *로 시작하는 파일들을 모은다
    # print('합쳐질 CSV 파일 목록 : ' + str(all_file_list))
    all_data = []  # 읽어 들인 csv 파일 내용을 저장할 빈 리스트를 하나 만든다
    for file in all_file_list:
        df = pd.read_csv(file)  # for 구문으로 csv 파일들을 읽어 들인다
        all_data.append(df)  # 빈 리스트에 읽어 들인 내용을 추가한다

    data_combine = pd.concat(all_data, axis=0, ignore_index=True)  # concat 함수를 이용해서 리스트의 내용을 병합
    # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True 는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.

    #data_combine = data_combine.fillna(method='ffill', limit=14)

    data_combine.to_csv(output_file, index=False, encoding='UTF-8')  # to_csv 함수로 저장한다. 인데스를 빼려면 False 로 설정
