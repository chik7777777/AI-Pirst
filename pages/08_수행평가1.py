# pages/video_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =============================
# 🔍 1. CSV 자동 경로 탐색 로직
# =============================
def load_data():
    candidate_paths = [
        '../video.csv',            # 일반적인 pages 폴더 기준
        '../../video.csv',         # pages 깊이가 다를 경우
        'video.csv',               # 같은 폴더
        '/mount/src/ai-pirst/video.csv',
        '/app/video.csv',
    ]

    for p in candidate_paths:
        if os.path.exists(p):
            return pd.read_csv(p)

    st.error(f"❌ CSV 파일을 찾을 수 없습니다. 확인한 경로: {candidate_paths}")
    st.stop()

# =============================
# 🔍 2. 앱별 합계 계산
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
# 🎨 3. 색상 그라데이션
# =============================
def make_color_scale(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append('red')  # 1등 빨간색
        else:
            alpha = max(0.15, 1 - i * 0.15)  # 점점 연해지는 파란색
            colors.append(f'rgba(0, 0, 255, {alpha})')
    return colors

# =============================
# ⭐ 4. 인기 영상 추천
# =============================
def show_recommendations(df, top_apps, viewer_col):
    st.subheader("📌 상위 3개 앱 인기 영상 추천")

    for _, row in top_apps.head(3).iterrows():
        app_name = row['app']
        st.markdown(f"### 🔵 앱: **{app_name}**")

        app_df = df[df['app'] == app_name]

        metric = 'views' if 'views' in df.columns else viewer_col
        top_videos = app_df.sort_values(by=metric, ascending=False).head(3)

        for _, vid in top_videos.iterrows():
            title = vid.get('title', '제목 없음')
            desc = vid.get('description', '설명 없음')

            st.write(f"**🎬 영상 제목:** {title}")
            st.write(f"👉 {desc}")
            st.write("---")

# =============================
# 🖥️ Streamlit UI
# =============================
st.title("📊 연도별 · 시청자 기준 앱 선호도 분석")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("⚙️ 필터 선택")
year_selected = st.sidebar.selectbox("연도 선택", sorted(df['year'].unique()))

viewer_cols = [col for col in df.columns if col not in ['year', 'app', 'title', 'description']]
viewer_selected = st.sidebar.selectbox("시청자 기준 선택", viewer_cols)

# Top apps
top_apps = get_top_apps(df, year_selected, viewer_selected)
top_apps_sorted = top_apps.sort_values(by=viewer_selected, ascending=False)
colors = make_color_scale(len(top_apps_sorted))

# Plotly chart
st.subheader(f"📈 {year_selected}년 기준 앱 선호도 ({viewer_selected})")

fig = px.bar(
    top_apps_sorted,
    x='app',
    y=viewer_selected,
    text=viewer_selected,
    title=f"{year_selected}년 앱 선호도"
)
fig.update_traces(marker_color=colors)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# Recommendations
show_recommendations(df, top_apps_sorted, viewer_selected)


