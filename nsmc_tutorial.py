# 참조 모델
# https://huggingface.co/monologg/koelectra-base-finetuned-nsmc

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

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
        # 긴 문장이 입력되었을 때의 최대 토큰 길이를 현재 사용하는 모델의 최대 토큰 길이인 512로 맞춰줌

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

# 입력한 문장을 읽고 감성 분석까지 하는 코드
def analyze_sentences(sentence_list, sa):
    results = []
    for sentence in sentence_list:
        sentence = sentence.strip() # 앞뒤 공백 제거
        if not sentence: # 빈 문자열이 입력되었을 경우
            continue # 건너뛴다
        score = sa(sentence)
        label = "positive" if score >= 0 else "negative"
        results.append(label)
    return results

# 프로그램 시작
if __name__ == "__main__":
    sa = sentiment_analysis()
    # 문장 직접 입력(카테고리 수정 가능)
    before_exam = [
        "내일이 오지 않으면 좋겠다.",
        "학교가 날아가 버렸으면.",
        "아직 1회독도 끝내지 못했는데 내일이 시험이라니 난 망했다."
    ]
    during_exam = [
        "공부한 내용이 기억이 안 나서 큰일이다.",
        "아, 학점이 낮게 나올 것 같다.",
        "교수님, 죄송합니다."
    ]
    after_exam = [
        "시험이 끝나서 기분이 홀가분해.",
        "드디어 종강이라니, 너무 기쁜걸.",
        "학점이 잘 나오지 않을까 걱정돼."
    ]
    # 카테고리를 수정했을 경우 수정한 것과 일치하도록 변경
    categories = {
        "before_exam": analyze_sentences(before_exam, sa),
        "during_exam": analyze_sentences(during_exam, sa),
        "after_exam": analyze_sentences(after_exam, sa)
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
    print(f"  Positive: {pos_count}") # 시기별로 각각 1/0/2
    print(f"  Negative: {neg_count}") # 시기별로 각각 2/3/1

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