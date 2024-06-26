'''
자전거 대여 서비스 관련 dataset 예측분석

dataset 출처 : UCI 머신러닝 저장소 
https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip


문3) 주어진 데이터셋(data)를 대상으로 단계별로 xgboost 모델을 생성하시오.
   단계1. 불필요한 칼럼 제거 : instant, dteday, casual, cnt
   단계2. X, y변수 선택 : y변수 = registered, X변수 나머지 변수(11개) 
   단계3. train(70) vs test(30) split     
   단계4. xgboost 모델 생성  
   단계5. 중요변수 시각화 & 의미 해석 
   단계6. model 평가 : r2 score  
'''


from xgboost import XGBRegressor # 회귀트리 모델 
from xgboost import plot_importance # 중요변수 시각화 
from sklearn.model_selection import train_test_split # split 
from sklearn.metrics import r2_score # 평가 

import seaborn as sn # 중요변수 시각화 & 해설 

import pandas as pd # dataset

path = r'C:\ITWILL\4_Python_ML\data\Bike-Sharing-Dataset'

data = pd.read_csv(path + '/day.csv')
data.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 731 entries, 0 to 730
Data columns (total 16 columns):
 #   Column      Non-Null Count  Dtype  
---  ------      --------------  -----  
 0   instant     731 non-null    int64  : 일련번호(제외) 
 1   dteday      731 non-null    object : 날짜(제외) 
 2   season      731 non-null    int64  : 계절 
 3   yr          731 non-null    int64  : 연도 
 4   mnth        731 non-null    int64  : 월 
 5   holiday     731 non-null    int64  : 휴일 
 6   weekday     731 non-null    int64  : 요일 
 7   workingday  731 non-null    int64  : 근무일 
 8   weathersit  731 non-null    int64  : 날씨 
 9   temp        731 non-null    float64 : 온도
 10  atemp       731 non-null    float64 : 체감온도
 11  hum         731 non-null    float64 : 습도
 12  windspeed   731 non-null    float64 : 풍속
 13  casual      731 non-null    int64   : 비가입자 이용수(제외) 
 14  registered  731 non-null    int64   : 가입자 이용수(y변수) 
 15  cnt         731 non-null    int64   : 전체사용자 이용수(제외) 
'''
data.head()


# 단계1. 불필요한 칼럼 제거(instant, dteday, casual, cnt) &  new_data 만들기  
new_data = data.drop(['instant', 'dteday', 'casual', 'cnt'], axis=1)
new_data.shape # (731, 12)

# 단계2. X, y변수 선택 : new_data에서 y변수 = registered, X변수 = 나머지변수(11개) 
X = new_data.drop('registered', axis=1)

y = new_data.registered


#  단계3. train(70) vs test(30) split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3)


# 단계4. xgboost 모델 생성 
model = XGBRegressor().fit(X=X_train, y=y_train) 


# 단계5. 중요변수 시각화 & 의미 해석   

# 1) 중요변수 시각화 
plot_importance(model)

# 2) 중요변수 Top6 해설 
# 습도(hum) > 풍속(windspeed) > 온도(temp) > 주말(weekday) > 온도(atemp) > 월(mnth)

#######################################
## 탐색적자료분석(EDA) : 중요변수 기준 
#######################################

# 습도(hum) vs 이용자수(registered)
sn.scatterplot(data = data, x=data.hum, 
               y=data.registered)
#[해설] 습도 0.4 이상 일때 이용자수가 많아진다.

# 풍속(windspeed) vs 이용자수(registered)
sn.scatterplot(data = data, x=data.windspeed, 
               y=data.registered)
#[해설] 풍속 0.35이하 일때 이용자수가 많아진다. 

# 온도(temp) vs 이용자수(registered)
sn.scatterplot(data = data, x=data.temp, 
               y=data.registered)
#[해설] 온도가 높을 수록 이용자수가 많아진다. 


# 주말(weekday) vs 이용자수(registered) 
data.weekday # 이산변수 
sn.barplot(data = data, x=data.weekday, 
               y=data.registered)
#[해설] 주말(0, 6)에 비해서 평일(1~5) 이용자수가 많다. 


# 월(mnth) vs 이용자수(registered) 
data.mnth # 이산변수
sn.barplot(data = data, x=data.mnth, 
               y=data.registered)
#[해설] 5월~10월 사이 이용자수가 상대적으로 많다.


# 단계6. model 평가 
y_pred = model.predict(X_test)

score = r2_score(y_test, y_pred)
print('r2 score =', score)
# r2 score = 0.8948685530861655











 