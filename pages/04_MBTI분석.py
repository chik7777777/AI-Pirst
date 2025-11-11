import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 🔹 페이지 설정
# -------------------------------
st.set_page_config(page_title="MBTI World Explorer", page_icon="🌎", layout="wide")

st.title("🌍 MBTI World Explorer")
st.markdown("""
국가를 선택하면 해당 국가의 **MBTI 유형 분포**를 확인하고,  
특정 MBTI 유형을 선택하면 **그 유형이 가장 높은 국가 순위**를 볼 수 있습니다.
""")

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
selected_country = st.selectbox("🌏 국가를 선택하세요", country_list)

# -------------------------------
# 🔹 선택한 국가의 MBTI 분포
# -------------------------------
country_data = df[df["Country"] == selected_country].iloc[0, 1:]
country_df = pd.DataFrame({
    "MBTI Type": country_data.index,
    "Percentage": country_data.values
}).sort_values(by="Percentage", ascending=False)

# 색상: 1등은 빨강, 나머지는 파랑 그라데이션
colors = ["#FF4B4B"] + [f"rgba(0,0,255,{0.9 - i*0.04})" for i in range(len(country_df) - 1)]

# Plotly 그래프
fig1 = px.bar(
    country_df,
    x="MBTI Type",
    y="Percentage",
    text=country_df["Percentage"].map(lambda x: f"{x*100:.1f}%"),
)
fig1.update_traces(marker_color=colors, textposition="outside")
fig1.update_layout(
    title=f"🇰🇷 {selected_country}의 MBTI 유형 분포",
    title_x=0.5,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
    height=550,
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 🔹 MBTI 유형별 국가 순위 비교
# -------------------------------
st.markdown("---")
st.subheader("📊 MBTI 유형별 전 세계 순위 보기")

mbti_types = [col for col in df.columns if col != "Country"]
selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

# 해당 유형으로 정렬
type_df = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).reset_index(drop=True)

# 색상 설정: 1등은 노랑, 한국은 파랑, 나머지는 회색
def get_color(country):
    if country == "South Korea":
        return "#007BFF"  # 파랑
    elif country == type_df.iloc[0]["Country"]:
        return "#FFD700"  # 노랑 (1등)
    else:
        return "#CCCCCC"  # 회색

type_df["Color"] = type_df["Country"].apply(get_color)

# Plotly 그래프
fig2 = px.bar(
    type_df.head(15),  # 상위 15개 국가만 보기
    x="Country",
    y=selected_type,
    text=type_df.head(15)[selected_type].map(lambda x: f"{x*100:.1f}%"),
)
fig2.update_traces(marker_color=type_df.head(15)["Color"], textposition="outside")
fig2.update_layout(
    title=f"🌐 '{selected_type}' 유형 비율이 높은 국가 Top 15",
    title_x=0.5,
    xaxis_title="국가",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
    height=600,
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 🔹 데이터 보기 (선택사항)
# -------------------------------
with st.expander("📋 데이터 원본 보기"):
    st.dataframe(df)
