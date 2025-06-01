import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from gensim.models import Word2Vec
from mecab import MeCab
from tqdm import tqdm

file_path = "2024_parisolympic.csv"

df = pd.read_csv(file_path)
tweet_contents = df["Tweet_Content"].dropna() #Tweet_Content 열의 내용만 추출
tweet_contents.to_csv("2024_parisolympic.txt", index=False, header=True, lineterminator='\n', encoding='utf-8') #txt파일로 변환 후 저장

train_data = pd.read_table("2024_parisolympic.txt")
print(train_data[:5])
print(len(train_data))

print(train_data["Tweet_Content"].nunique())
train_data.drop_duplicates(subset=["Tweet_Content"], inplace=True) #중복제거
print(len(train_data))

print(train_data.isnull().values.any()) #False

# print(train_data.isnull().sum())
# train_data.loc[train_data.Tweet_Content.isnull()]
# train_data = train_data.dropna(how = 'any')
# print(train_data.isnull().values.any())
# print(len(train_data)) #24행에서 출력값이 True라면 실행

def preprocessing(text):
    new_text1 = re.sub(r"\(.*?\)", "", text)
    new_text2 = re.sub(r"https?:\/\/t\.co\/\w{10}", "", new_text1) #트위터 url 제거
    new_text3 = re.sub(r"[\r\n]+", "", new_text2)
    new_text4 = re.sub(r"[^ㄱ-ㅎ가-힣0-9a-zA-Z\s]", "", new_text3)

    return new_text4

print(train_data["Tweet_Content"][:5])
train_data["Tweet_Content"] = train_data["Tweet_Content"].apply(preprocessing)
print(train_data["Tweet_Content"][:5])

train_data["Tweet_Content"].replace('', np.nan, inplace=True)
print(train_data.isnull().sum()) #0

# print(train_data.loc[train_data.Tweet_Content.isnull()][:5])
# train_data = train_data.dropna(how = 'any')
# print(len(train_data)) #45행 출력값이 1 이상이라면 실행

train_data.to_csv("2024_parisolympic_cleaned.txt", index=False, sep='\t', encoding='utf-8') #전처리 텍스트 txt파일로 저장