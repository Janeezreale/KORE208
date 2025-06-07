import pandas as pd
import numpy as np
import re

#트위터피드 전처리
file_path = "2018_metoo.csv"

df = pd.read_csv(file_path)
tweet_contents = df["Tweet_Content"].dropna() #Tweet_Content 열의 내용만 추출
tweet_contents.to_csv("2018_metoo.txt", index=False, header=True, lineterminator='\n', encoding='utf-8') #txt파일로 변환 후 저장

train_data = pd.read_table("2018_metoo.txt")
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



input_file = "2024_parisolympic_cleaned.txt"
output_file = "2024_parisolympic_cleaned1.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(len(lines))

# 첫 줄은 헤더로 유지
header = lines[0]
content_lines = lines[1:]

# '버닝썬'이 포함된 행만 필터링
filtered_lines = [line for line in content_lines if '올림픽' in line]
print(len(filtered_lines))

# 헤더 + 필터링된 내용 저장
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines([header] + filtered_lines)
#51~69행 올림픽을 포함하지 않는 행은 제거, 필요한 경우 수행




#유튜브 댓글 전처리
file_path = "youtube(2019,worldcup)/comments.csv"

df = pd.read_csv(file_path)
youtube_comments = df["text"].dropna() #text 열의 내용만 추출
youtube_comments.to_csv("youtube(2019,worldcup)/comments.txt", index=False, header=True, lineterminator='\n', encoding='utf-8') #txt파일로 변환 후 저장

train_data = pd.read_table("youtube(2019,worldcup)/comments.txt")
print(train_data[:5])
print(len(train_data))

print(train_data["text"].nunique())
train_data.drop_duplicates(subset=["text"], inplace=True) #중복제거
print(len(train_data))

print(train_data.isnull().values.any()) #False

# print(train_data.isnull().sum())
# train_data.loc[train_data.comment1.isnull()]
# train_data = train_data.dropna(how = 'any')
# print(train_data.isnull().values.any())
# print(len(train_data)) #90행에서 출력값이 True라면 실행

def preprocessing(text):
    new_text1 = re.sub(r"\(.*?\)", "", text)
    new_text2 = re.sub(r"[\r\n]+", "", new_text1)
    new_text3 = re.sub(r"[^ㄱ-ㅎ가-힣0-9a-zA-Z\s]", "", new_text2)

    return new_text3

print(train_data["text"][:5])
train_data["text"] = train_data["text"].apply(preprocessing)
print(train_data["text"][:5])

train_data["text"].replace('', np.nan, inplace=True)
print(train_data.isnull().sum()) #0

print(train_data.loc[train_data.text.isnull()][:5])
train_data = train_data.dropna(how = 'any')
print(len(train_data)) #110행 출력값이 1 이상이라면 실행

train_data.to_csv("youtube(2019,worldcup)/comments_cleaned.txt", index=False, sep='\t', encoding='utf-8') #전처리 텍스트 txt파일로 저장