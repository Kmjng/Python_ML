# -*- coding: utf-8 -*-
"""
문3) df 데이터프레임을 대상으로 다음과 같은 단계로 가변수(dummay variable)를 만드시오.  
"""

import pandas as pd 

## 데이터 생성 
data = {
    'gender' : ['male','female','male','male','female'],
    'height' : [175,165,180,169,188],
    'nation' : ['USA','Korea','China','Korea','Brazil'],
    'married' : [0,1,1,1,0]
}

df = pd.DataFrame(data)
df.info()
'''
Data columns (total 4 columns):
 #   Column   Non-Null Count  Dtype 
---  ------   --------------  ----- 
 0   gender   5 non-null      object
 1   height   5 non-null      int64 
 2   nation   5 non-null      object
 3   married  5 non-null      int64 
'''
 
# 단계1. 'nation' 칼럼 값의 Korea -> Brazil -> USA -> China 순서로 변경 
df['nation'] = df['nation'].astype('category')
df['nation'] = df['nation'].cat.set_categories(['Korea','Brazil','USA','China'])

## 단계2. 'gender','nation' 칼럼으로 k-1개 가변수를 만들어서 new_df 생성하기 
new_df = pd.get_dummies(data=df, columns=['gender','nation'], drop_first = True, dtype='uint8')
new_df2 = pd.get_dummies(data=df, columns=['gender','nation'], drop_first = False, dtype='uint8)
new_df2.columns 
'''['height', 'married', 'gender_female', 'gender_male', 'nation_Korea',
       'nation_Brazil', 'nation_USA', 'nation_China']'''
new_df.columns 
''' ['height', 'gender_male', 'nation_Brazil', 'nation_USA', 'nation_China']'''

## 단계3. new_df에서 'married' 칼럼을 제거하여 현재 객체 적용하기(출력결과 참고)  
'''
   height  gender_male  nation_Brazil  nation_USA  nation_China
0     175            1              0           1             0
1     165            0              0           0             0
2     180            1              0           0             1
3     169            1              0           0             0
4     188            0              1           0             0
'''

new_df.drop('married', axis = 1, inplace=True)
new_df.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   height         5 non-null      int64
 1   gender_male    5 non-null      bool 
 2   nation_Brazil  5 non-null      bool 
 3   nation_USA     5 non-null      bool 
 4   nation_China   5 non-null      bool 
dtypes: bool(4), int64(1)
memory usage: 192.0 bytes
'''
