# arena2-book
카카오 아레나 2회 대회(브런치 글 추천)에 제출한 최종 코드의 저장소는 아래와 같습니다.  
https://github.com/JungoKim/brunch_nafma

본 저장소에서는 데이터 분석 및 1등 솔루션의 모델별 성능을 확인하기 위한 추가 코드를 공유합니다.

* eda.ipynb 제공되는 데이터를 이해하기 위한 Explatory Data Analysis 노트북입니다.
* inference_cf.py 협업 필터링 만으로 100건의 추천글을 생성하는 프로그램입니다.
* inference_cbf.py 컨텐츠 기반 필터링 만으로 100건의 추천글을 생성하는 프로그램입니다.
* inference_cbf_cf.py 두가지 모델의 예측 순서를 바꾸어서 100건의 추천글을 생성하는 프로그램입니다.

1등 솔루션의 협업 필터링 추천 구현시 실험했던 워드 임베딩의 학습 데이터 생성, 모델 생성 및 예측 코드도 공유합니다.
* prepare_w2v.py 글 아이디를 단어로, 각 세션에서 읽은 글들의 모음을 문장으로 Word2Vec 학습 데이터를 생성합니다.
* train_w2v.py 파이썬 gensim 패키지를 사용하여 Word2Vec 모델을 생성합니다. (model 디렉토리를 생성하고 인자를 train로 주어 실행) 
* recommend_wv.py 생성한 Word2Vec 모델로 추천할 글을 예측합니다. (인자를 dev로 주어 실행)

참고 링크 목록
* 카카오 아레나 2회 대회 https://arena.kakao.com/c/2
* 카카오 아레나 2회 대회 플레이그라운드 https://arena.kakao.com/c/6
* 카카오 아레나 2회 대회 예제 코드 https://github.com/kakao-arena/brunch-article-recommendation
