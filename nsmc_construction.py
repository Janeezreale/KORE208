# 참조 모델
# https://huggingface.co/monologg/koelectra-base-finetuned-nsmc

import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

os.chdir("./") # 경로 설정

# 긍정/부정 감성 분석을 위한 클래스 정의
class sentiment_analysis:
    def __init__(self):
        # KoELECTRA Tokenizer 불러오기 (따로 데이터에 토큰화 과정을 거칠 필요 X)
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-finetuned-nsmc")
        # KoELECTRA model (긍정/부정 판별용) 불러오기
        self.model = AutoModelForSequenceClassification.from_pretrained("monologg/koelectra-base-finetuned-nsmc")

    def __call__(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt", max_length=512, truncation=True)
        # 모델 입력 텐서 크기와 모델 내부 임베딩 레이어의 크기가 다를 때 나타나는 오류를 방지 
        # 긴 문장이 입력되었을 때의 최대 토큰 길이를 모델의 최대 토큰 길이인 512로 맞춰줌

        # 메모리 절약을 위해 학습이 아니라 inference(추론)만 우선 진행 후 softmax 함수로 확률화
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits # 예측 결과 (긍정/부정 점수)
            probs = F.softmax(logits, dim=1)  # softmax 함수 적용하여 각 클래스(긍정/부정)가 선택될 확률로 변환

            positive_score = probs[0, 1].item()
            # 부정(0), 긍정(1) 순서로 softmax 결과가 나오므로 긍정 확률(1번째 인덱스)만 추출
            # why? softmax 결과는 긍정/부정의 값의 합이 항상 1이므로 긍정/부정 중 하나만 알면 전체 판단이 가능함
        return 2 * positive_score - 1 
        # 부정은 -1에 가까운 음수, 긍정은 1에 가까운 양수, 0은 중립

# 데이터 파일을 읽고 감성 분석까지 하는 코드
def analyze_files(file_list, sa):
    results = []
    for file in file_list:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for sentence in lines:
            sentence = sentence.strip() # 앞뒤 공백 제거
            if not sentence: # 빈 줄이 있다면
                continue # 건너뛴다
            score = sa(sentence)
            label = "positive" if score >= 0 else "negative" # 긍정/부정 라벨링
            results.append(label)
    return results

# 프로그램 시작
if __name__ == "__main__":
    sa = sentiment_analysis()
    # 감성 분석기 인스턴스 생성

    before_covid_files = ["2018.txt", "2019.txt"] # 코로나 이전
    covid_pandemic_files = ["2020.txt", "2021.txt", "2022_cleaned.txt"] # 팬데믹 시기
    post_covid_files = ["2023_cleaned.txt", "2024.txt"] # 포스트 코로나

    categories = {
        "before covid": analyze_files(before_covid_files, sa),
        "covid pandemic": analyze_files(covid_pandemic_files, sa),
        "post covid": analyze_files(post_covid_files, sa)
    }

# 시각화 데이터 준비
category_names = []
positive_counts = []
negative_counts = []

# 각 시기별로 긍정/부정 문장 개수 세기(모델이 잘 실행되었나 확인용)
for category, labels in categories.items():
    pos_count = labels.count("positive")
    neg_count = labels.count("negative")
    category_names.append(category)
    positive_counts.append(pos_count)
    negative_counts.append(neg_count)

    print(f"\n{category}:")
    print(f"  Positive: {pos_count}") # 시기별로 각각 3285/4740/3231
    print(f"  Negative: {neg_count}") # 시기별로 각각 3343/6049/3870

import matplotlib.pyplot as plt

# 그래프를 그리기 위한 비율 계산
positive_ratios = []
negative_ratios = []

for pos_count, neg_count in zip(positive_counts, negative_counts):
    total = pos_count + neg_count
    positive_ratios.append(pos_count / total * 100)
    negative_ratios.append(neg_count / total * 100)

# 꺾은선그래프 그리가
plt.figure(figsize=(8, 6))
x = range(len(category_names))

plt.plot(x, positive_ratios, marker='o', color='green', label='Positive %')
plt.plot(x, negative_ratios, marker='o', color='red', label='Negative %')

plt.xticks(x, category_names)
plt.ylabel('Percentage (%)')
plt.title('Sentiment Ratio by Period')
plt.ylim(0, 100)  # y축 0~100% 로 고정
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
