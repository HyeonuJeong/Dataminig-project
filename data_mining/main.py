# 데이터마이닝 정가람(1526025), 이주승(1625022), 곽지훈(1826002), 정현우(2025407)
# IDE 는 PyCharm 을 사용하였습니다. Python 3.8

import fruit  # fruit.py : 과일 데이터 관련 함수
import holiday  # holiday.py : 휴일 데이터 관련 함수
import temp  # temp.py : 기온 데이터 관련 함수
import wage  # wage.py : 최저 임금 관련 함수
import pptn  # pptn.py : 강수량 데이터 관련 함수
import week  # week.py : 요일 데이터 관련 함수

import func  # func.py : 기타 함수

import after  # after.py : 각 데이터 전처리 이후 다시 전체 전처리 할때 사용

import LSTM  # LSTM.py : Long-Short-Term-Memory (RNN)
import SVM  # SVM.py : SVM 분류
import RF  # RF.py : 랜덤 포레스트

# 필요한 초기 디렉토리 생성

func.create_directory('./csv')
# API 를 사용하지 않고 다운로드 받은 CSV 파일들의 원본 파일 경로
func.create_directory('./csv/original')

func.create_directory('./csv/apple_temp')
func.create_directory('./csv/apple_temp/original')
func.create_directory('./csv/apple_temp/processed')

func.create_directory('./csv/pear_temp')
func.create_directory('./csv/pear_temp/original')
func.create_directory('./csv/pear_temp/processed')

func.create_directory('./csv/holiday_temp')
func.create_directory('./csv/holiday_temp/original')
func.create_directory('./csv/holiday_temp/processed')


# API 사용하여 사과 CSV 다운로드 (2016년 ~ 2018년)
fruit.download_csv('apple', 2016, 2018)
# 사과 데이터 전처리 (2016년 ~ 2018년)
fruit.data_processing('apple', 2016, 2018)
# 사과 CSV 파일 합치기 (./csv/apple_temp/processed/ 안의 모든 파일)
fruit.merge_csv('apple')

# API 사용하여 배 CSV 다운로드 (2016년 ~ 2018년)
fruit.download_csv('pear', 2016, 2018)
# 배 데이터 전처리 (2016년 ~ 2018년)
fruit.data_processing('pear', 2016, 2018)
# 배 CSV 파일 합치기 (./csv/pear_temp/processed/ 안의 모든 파일)
fruit.merge_csv('pear')

# API 사용하여 휴일 데이터 CSV 다운로드 (2016년 ~ 2018년)
holiday.download_csv(2016, 2018)
# 휴일 데이터 전처리 (2016년 ~ 2018년)
holiday.data_processing(2016, 2018)
# 휴일 CSV 파일 합치기 (./csv/pear_temp/processed/ 안의 모든 파일)
holiday.merge_csv()

# 나머지 각 데이터 1차 전처리
temp.data_processing()
pptn.data_processing()
wage.data_processing()
week.data_processing()

# 2차 전처리 (각 데이터 전처리 이후 모든 데이터 한번에 다루기 위해)
after.data_processing()  # 이 함수 실행 시 전처리가 끝난 test_apple.csv , test_pear.csv 생성 완료

# 분석 기법 사용
# LSTM
LSTM.long_short_term_memory('apple')
LSTM.long_short_term_memory('pear')

# SVM
SVM.support_vector_machine('apple')
SVM.support_vector_machine('pear')

# 랜덤 포레스트
RF.random_forest('apple')
RF.random_forest('pear')

