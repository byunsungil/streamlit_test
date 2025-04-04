import streamlit as st
st.set_page_config(page_title="뉴스 워드클라우드", layout="wide")  # ✅ 제일 위에 위치!

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import requests
from bs4 import BeautifulSoup
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from io import BytesIO


cars = pd.read_csv("자동차등록현황보고_자동차등록대수현황 시도별 (201101 ~ 202502).csv",encoding = "cp949",skiprows=5)

cars.columns = ['일시', '시도명', '시군구', '승용_관용', '승용_자가용', '승용_영업용', '승용_계',
              '승합_관용', '승합_자가용', '승합_영업용', '승합_계',
              '화물_관용', '화물_자가용', '화물_영업용', '화물_계',
              '특수_관용', '특수_자가용', '특수_영업용', '특수_계',
              '총계_관용', '총계_자가용', '총계_영업용', '총계']
cars = cars[(cars['시도명'] == '서울') & (cars['시군구'] == '강남구')]

cars_kangnam = cars[['일시','승용_영업용']]

cnt = cars_kangnam[:12]['승용_영업용']

cnt = cnt.str.replace(',', '').astype(int)

cnt3 = cars_kangnam[:24]['승용_영업용']
cnt3 = cnt3.str.replace(',', '').astype(int)

st.title("법인 차량 변동 추세")
st.header("안녕하세요 👋")
st.write("이것은 2023 영업용 승용_차량 변동 추이 입니다.")

fig, ax = plt.subplots(figsize=(8, 4))
plt.xticks(rotation=45)  # 45도 회전
ax.plot(cars_kangnam[:24]['일시'], cnt3)
ax.set_title('2023 cars')
ax.set_xlabel('month')
ax.set_ylabel('count')

# Streamlit에 그래프 출력
st.pyplot(fig)


cnt = cars_kangnam[:12]['승용_영업용']
cnt = cnt.str.replace(',', '').astype(int)
car_2023 = sum(cnt)/12
cnt2 = cnt = cars_kangnam[12:24]['승용_영업용']
cnt2 = cnt2.str.replace(',', '').astype(int)
car_2024 = sum(cnt2)/12

st.write(f"2023 평균 등록수 : 약 {car_2023:.0f}대")
st.write(f"2024 평균 등록수 : 약 {car_2024:.0f}대")





st.title("📰 네이버 뉴스 워드클라우드")
query = st.text_input("검색어를 입력하세요", value="법인자동차 등록 현황")

if st.button("분석 시작") and query:
    with st.spinner("뉴스 기사 크롤링 중..."):
        # 뉴스 크롤링
        articles = []
        for page in range(1, 6):
            start = (page - 1) * 10 + 1
            url = f"https://search.naver.com/search.naver?where=news&query={query}&start={start}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            news_items = soup.select("ul.list_news li.bx")
            for item in news_items:
                title_tag = item.select_one("a.news_tit")
                if title_tag:
                    articles.append(title_tag["title"])

    if len(articles) == 0:
        st.warning("기사를 찾을 수 없습니다.")
    else:
        st.success(f"{len(articles)}개의 뉴스 제목을 수집했습니다.")

        # 텍스트 처리
        text = " ".join(articles)
        text = re.sub("[^가-힣\s]", "", text)
        words = text.split()
        words = [w for w in words if len(w) > 1]
        word_freq = Counter(words)

        # 워드클라우드 생성
        wc = WordCloud(
            font_path="c:/Windows/Fonts/malgun.ttf",  # 한글 폰트 경로
            width=800,
            height=400,
            background_color="white"
        )
        wc.generate_from_frequencies(word_freq)

        # 이미지 표시
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)





