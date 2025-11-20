# pages/video_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =============================
# 1) CSV 자동 경로 + 자동 인코딩 탐색 (오류 방지 최종본)
# =============================
def load_data():
    candidate_paths = [
        '../video.csv',
        '../../video.csv',
        'video.csv',
        '/mount/src/ai-pirst/video.csv',
        '/app/video.csv',
    ]

    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin1']

    for path in candidate_paths:
        if os.path.exists(path):
            for enc in encodings:
                try:
                    return pd.read_csv(path, encoding=enc)
                except Exception:
                    pass
            st.error(f"❌ CSV 파일은 찾았지만 인코딩 오류가 발생했습니다.\n시도한 인코딩: {encodings}")
            st.stop()

    st.error(f"❌ CSV 파일을 찾지 못했습니다. 확인한 경로: {candidate_paths}")
    st.stop()

# =============================
# 2) 앱별 시청자수 집계
# =============================
def get_top_apps(df, year, viewer_col):
    filtered = df[df['year'] == year]
    grouped = (
        filtered.groupby('app')[viewer_col]
        .sum()
        .reset_index()
        .sort_values(by=viewer_col, ascending=False)
    )
    return grouped

# =============================
# 3) 막대 색상: 1등 빨간색 + 파란 계열 그라데이션
# =============================
def make_color_scale(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append("red")
        else:
            alpha = max(0.15, 1 - i * 0.15)
            colors.append(f"rgba(0, 0, 255, {alpha})")
    return colors

# =============================
# 4) 인기 영상 추천
# =============================
def show_recommendations(df, top_apps, viewer_col):
    st.subheader("📌 상위 3개 앱 인기 영상 추천")
    metric = 'views' if 'views' in df.columns else viewer_col

    for _, row in top_apps.head(3).iterrows():
        app = row['app']
        st.markdown(f"### 🔵 앱: **{app}**")

        sub = df[df['app'] == app]
        recomm = sub.sort_values(by=metric, ascending=False).head(3)

        for _, v in recomm.iterrows():
            title = v.get('title', '제목 없음')
            desc = v.get('description', '설명 없음')

            st.write(f"**🎬 영상 제목:** {title}")
            st.write(f"👉 {desc}")
            st.write("---")

# =============================
# Streamlit UI
# =============================
st.title("📊 연도별 · 시청자 기준 앱 선호도 분석 대시보드")

df = load_data()

st.sidebar.header("⚙️ 필터 선택")
year_selected = st.sidebar.selectbox("연도 선택", sorted(df['year'].unique()))

viewer_cols = [c for c in df.columns if c not in ['year', 'app', 'title', 'description']]
viewer_selected = st.sidebar.selectbox("시청자 기준", viewer_cols)

# 집계
result = get_top_apps(df, year_selected, viewer_selected)
colors = make_color_scale(len(result))

st.subheader(f"📈 {year_selected}년 기준 앱 선호도 ({viewer_selected})")
fig = px.bar(result, x='app', y=viewer_selected, text=viewer_selected)
fig.update_traces(marker_color=colors)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# 추천
show_recommendations(df, result, viewer_selected)



# plotly
