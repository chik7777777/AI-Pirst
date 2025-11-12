import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 📂 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    # 쉼표 제거 후 숫자 변환
    for col in df.columns[3:]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
    return df

df = load_data()

# -----------------------------
# 🏙️ 행정구 선택
# -----------------------------
st.title("🏙️ 서울시 행정구별 연령대 인구 시각화")
selected_region = st.selectbox("📍 행정구를 선택하세요", df["행정구역"].tolist())

# 선택한 구 데이터 필터링
region_data = df[df["행정구역"] == selected_region].T.reset_index()
region_data.columns = ["항목", "인구수"]

# 연령 데이터만 추출
age_data = region_data[region_data["항목"].str.contains("거주자_\\d+세")].copy()
age_data["나이"] = age_data["항목"].str.extract("거주자_(\d+)세").astype(int)

# -----------------------------
# 📈 그래프 그리기
# -----------------------------
fig = px.line(
    age_data,
    x="나이",
    y="인구수",
    title=f"{selected_region} 연령별 인구 분포",
)

# 스타일 커스터마이징
fig.update_layout(
    plot_bgcolor="#f0f0f0",  # 회색 바탕
    xaxis=dict(
        title="나이",
        dtick=10,  # 10살 단위 구분선
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="인구수",
        dtick=100,  # 100명 단위 구분선
        gridcolor="lightgray"
    ),
    title_x=0.5,
)

# -----------------------------
# 📊 그래프 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ℹ️ 데이터 요약
# -----------------------------
total_pop = int(df[df["행정구역"] == selected_region]["2025년10월_거주자_총인구수"].iloc[0].replace(",", ""))
st.markdown(f"**{selected_region}의 총인구:** {total_pop:,}명")
st.caption("※ 출처: 2025년 10월 기준 서울특별시 주민등록 인구통계")
