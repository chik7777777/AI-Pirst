import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 🔹 페이지 설정
# -------------------------------
st.set_page_config(page_title="MBTI World Explorer", page_icon="🌎", layout="wide")

st.title("🌍 MBTI World Explorer")
st.markdown("국가를 선택하면 해당 국가의 **MBTI 유형 분포**를 확인할 수 있습니다.")

# -------------------------------
# 🔹 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -------------------------------
# 🔹 국가 선택
# -------------------------------
country_list = df["Country"].sort_values().unique()
selected_country = st.selectbox("국가를 선택하세요", country_list)

# -------------------------------
# 🔹 선택한 국가의 데이터 추출
# -------------------------------
country_data = df[df["Country"] == selected_country].iloc[0, 1:]
country_df = pd.DataFrame({
    "MBTI Type": country_data.index,
    "Percentage": country_data.values
}).sort_values(by="Percentage", ascending=False)

# -------------------------------
# 🔹 색상 설정 (1등은 빨간색, 나머지는 파란색 그라데이션)
# -------------------------------
colors = ["#FF4B4B"] + [f"rgba(0,0,255,{0.9 - i*0.04})" for i in range(len(country_df) - 1)]

# -------------------------------
# 🔹 Plotly 그래프 생성
# -------------------------------
fig = px.bar(
    country_df,
    x="MBTI Type",
    y="Percentage",
    text=country_df["Percentage"].map(lambda x: f"{x*100:.1f}%"),
)

# 색상 적용
fig.update_traces(marker_color=colors, textposition="outside")

# 디자인 세부 조정
fig.update_layout(
    title=f"🇨🇴 {selected_country}의 MBTI 유형 분포",
    title_x=0.5,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
    height=600,
)

# -------------------------------
# 🔹 그래프 출력
# -------------------------------
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 🔹 데이터 테이블 (선택사항)
# -------------------------------
with st.expander("📋 데이터 보기"):
    st.dataframe(country_df.style.format({"Percentage": "{:.3f}"}))
