# 예시

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
# Load model directl


class sentiment_analysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-finetuned-nsmc")
        self.model = AutoModelForSequenceClassification.from_pretrained("monologg/koelectra-base-finetuned-nsmc")

    def __call__(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)  # 소프트맥스 적용

    # 부정(0), 긍정(1) 순서라면
    # 긍정 점수만 뽑기 (1번째 인덱스)
            positive_score = probs[0, 1].item()
        return 2 * positive_score - 1


if __name__ == "__main__":

    sentence = ""
    sa = sentiment_analysis()
    print(sa(sentence))
# 데이터 모두 수합되면 문자열 넣는 코드 대신 파일 읽는 코드로 수정할 예정