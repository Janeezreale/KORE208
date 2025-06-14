# KORE208

본 Git은 고려대학교 2025-1 국어국문학과 전공과목 '한국어정보처리'의 기말과제를 위해 생성되었다.


Presentiation 자료: https://www.canva.com/design/DAGpo82fnIg/MVhLl49oct5oqK3fM6VcnQ/view?utm_content=DAGpo82fnIg&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h65c696a728


## 📚 과제 소개

'**코로나19 전후 감성 분석**(긍정/부정 표현 사용의 시계열적 변화를 중심으로
)'을 주제로 코로나19 이전(2018-2019), 코로나19 범유행 기간(2020-2022), 포스트 코로나(2023-2024)로 시기를 나눠 긍정/부정 표현 사용의 시계열 변화를 알아보고자 한다.


주요 쟁점은 다음과 같다:
1. 코로나19 전후 긍정/부정 표현 사용의 추이가 어떻게 되는가
2. 코로나 블루와 긍정/부정 어휘 사용의 상관관계가 존재하는가
3. 상관관계가 존재한다면, 코로나 블루가 온라인상 정서적 반응 및 의사 표현에 어떤 영향을 미쳤는가?


## 🧐 연구 방법

**BERT**를 활용하여 감성 분석을 진행한다.


1. 선행 연구 검토
2. 데이터 구축: **Octoparse**를 이용하여 코로나 이전(2018-2019), 코로나 팬데믹(2020-2022), 포스트 코로나(2023-2024)로 나눠 각 연도 주요 사건 관련 기사의 댓글/SNS 피드 크롤링
3. 데이터 전처리: 정규 표현식과 MeCab-ko 라이브러리를 활용하여 수집한 텍스트 전처리
4. 감성 분석 모델 구축: nsmc 데이터셋을 사용하여 pretrained 및 fine-tuning된 **koELECTRA-base-finetuned-nsmc**를 활용하여 구축한 데이터셋에 맞게 코드를 수정하여 모델 구축 및 성능 평가


성능 평가 코드 및 결과: https://colab.research.google.com/drive/1cL0t-yIWbOtrkD0p39idNA4e2csAdzLY?usp=sharing (* test 데이터셋 크기가 커서 GPU 사용이 불가피하여 Google Colab 통해 진행함)

7. 빈도 기반 시계열 분석: 구축한 모델을 이용해 시기별로 긍정/부정 표현의 빈도를 집계하여 matplotlib으로 시각화
8. 시각화 결과 분석


## 😎 결론 및 의의


1. 요약: ‘코로나 블루가 온라인상 정서 표현에 영향을 미쳤을 것이다’는 가설을 세우고 코로나19 전후 시기별로 데이터를 수집하여 감성 분석을 진행하였다. 감성 분석 결과 코로나19 확산 시기부터 부정적 감정 표현 빈도는 급증하고 긍정적 감정 표현 빈도는 급감하였고, 종식 이후 부정적 감정 표현은 소폭 감소, 긍정적 감정 표현 빈도는 소폭 증가하였다. 그러나 여전히 부정적 감정 표현 빈도와 긍정적 감정 표현 빈도의 차이가 크기에,  온라인상 정서 표현에 코로나 블루가 어느 정도 영향은 끼쳤음은 알 수 있다.
2. 연구 결과 활용: 옥토퍼스에서 피드 작성자를 자신의 아이디로 설정하는 경우, (공개 계정에 한해) 자신이 작성한 피드를 스크래핑할 수 있다. 연구에서 활용한 전처리 코드와 감성분석 모델을 배포하여 sns글에 나타난 시기별 감성 변화의 자가 측정 도구로 활용 가능하다. 또한 연구 결과를 감성 변화 실태 조사에 활용, 정부 정책 수립에 반영 및 정책 효과 파악에 활용할 수 있다.
3. 향후 과제: 코로나19 유행 시기 특성상, 구어텍스트 수집에 제약을 가졌다. 이번 연구 또한 코로나 유행 전, 유행 중, 포스트코로나 세 시기의 데이터를 같은 조건에서 수집하기 위해 유튜브댓글, 트위터피드라는 문어텍스트 내지 온라인상 구어텍스트에 기반하였다. 또한 사회적 거리두기 정책 해제, 감염병 확산세의 완화로 인해 오프라인 기반 문어 텍스트 말뭉치 구축에 대한 제약이 감소하였다. 이를 바탕으로 언어적 표현을 통해 인간의 감정을 심도 있게 파악하기 위해서는 문어텍스트와 구어텍스트를 고루 수집하여 결과 분석에 반영할 필요성이 생긴다.

