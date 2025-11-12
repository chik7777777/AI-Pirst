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

st.title("🏙️ 서울시 인구 시각화 대시보드")

# -----------------------------
# 🧭 탭 구성
# -----------------------------
tab1, tab2 = st.tabs(["📈 행정구별 연령별 꺾은선그래프", "📊 연령대별 인구순 막대그래프"])

# =============================
# 📈 [탭1] 행정구별 연령별 꺾은선그래프
# =============================
with tab1:
    selected_region = st.selectbox("📍 행정구를 선택하세요", df["행정구역"].tolist())

    region_data = df[df["행정구역"] == selected_region].T.reset_index()
    region_data.columns = ["항목", "인구수"]

    age_data = region_data[region_data["항목"].str.contains("거주자_\\d+세")].copy()
    age_data["나이"] = age_data["항목"].str.extract("거주자_(\d+)세").astype(int)

    fig1 = px.line(
        age_data,
        x="나이",
        y="인구수",
        title=f"{selected_region} 연령별 인구 분포",
    )

    fig1.update_layout(
        plot_bgcolor="#f0f0f0",
        xaxis=dict(title="나이", dtick=10, gridcolor="lightgray"),
        yaxis=dict(title="인구수", dtick=100, gridcolor="lightgray"),
        title_x=0.5,
    )

    st.plotly_chart(fig1, use_container_width=True)

    total_pop = int(df[df["행정구역"] == selected_region]["2025년10월_거주자_총인구수"].iloc[0].replace(",", ""))
    st.markdown(f"**{selected_region}의 총인구:** {total_pop:,}명")
    st.caption("※ 출처: 2025년 10월 기준 서울특별시 주민등록 인구통계")

# =============================
# 📊 [탭2] 연령대별 인구순 막대그래프
# =============================
with tab2:
    st.subheader("📊 연령대별 서울시 구별 인구 비교")

    # 선택할 연령대 리스트
    age_groups = [f"{i}대" for i in range(0, 100, 10)]
    selected_age_group = st.selectbox("👶 연령대를 선택하세요", age_groups)

    # 선택한 연령대의 나이 범위 계산
    start_age = int(selected_age_group.replace("대", ""))
    end_age = start_age + 9

    # 각 구별로 해당 연령대 인구 합계 계산
    df_age_sum = df.copy()
    age_cols = [col for col in df.columns if any(f"거주자_{age}세" in col for age in range(start_age, end_age + 1))]

    df_age_sum["해당연령대_인구수"] = df_age_sum[age_cols].apply(lambda x: x.sum(), axis=1)
    df_age_sum_sorted = df_age_sum.sort_values("해당연령대_인구수", ascending=False)

    # 막대그래프 생성
    fig2 = px.bar(
        df_age_sum_sorted,
        x="행정구역",
        y="해당연령대_인구수",
        title=f"서울시 {selected_age_group} 인구순 (상위→하위)",
    )

    fig2.update_layout(
        plot_bgcolor="#f0f0f0",
        xaxis=dict(title="행정구", tickangle=45, gridcolor="lightgray"),
        yaxis=dict(title="인구수", dtick=100, gridcolor="lightgray"),
        title_x=0.5,
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.caption("※ 선택한 연령대(예: 20대 → 20~29세)의 인구수를 구별로 비교")
