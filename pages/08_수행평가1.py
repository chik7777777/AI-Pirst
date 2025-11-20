# pages/video_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# CSV는 루트 폴더에 있으므로 ../video.csv 로 로드
def load_data():
    return pd.read_csv('../video.csv')

def get_top_apps(df, year, viewer_col):
    filtered = df[df['year'] == year]
    app_group = filtered.groupby('app')[viewer_col].sum().reset_index()
    app_group = app_group.sort_values(by=viewer_col, ascending=False)
    return app_group

def make_color_scale(n):
    colors = []
    for i in range(n):
        if i == 0:
            colors.append('red')
        else:
            # 점점 연해지는 파란색 그라데이션 (예: rgba)
            alpha = max(0.2, 1 - (i * 0.15))
            colors.append(f'rgba(0, 0, 255, {alpha})')
    return colors

def show_recommendations(df, top_apps, viewer_col):
    st.subheader("📌 상위 3개 앱 인기 영상 추천")
    for i, row in top_apps.head(3).iterrows():
        app_name = row['app']
        st.markdown(f"### 🥇 앱: **{app_name}**")
        app_videos = df[df['app'] == app_name]

        # 조회수가 있으면 조회수 기준, 아니면 viewer_col 기준 추천
        metric = 'views' if 'views' in df.columns else viewer_col
        top_videos = app_videos.sort_values(by=metric, ascending=False).head(3)

        for _, vid in top_videos.iterrows():
            title = vid.get('title', '제목 없음')
            desc = vid.get('description', '설명 없음')
            st.write(f"**영상 제목:** {title}")
            st.write(f"👉 {desc}")
            st.write("---")

# Streamlit UI
st.title("📊 연도·시청자 기준 앱 선호 분석 대시보드")

with st.spinner("데이터 불러오는 중..."):
    df = load_data()

st.sidebar.header("🔧 필터 선택")
years = sorted(df['year'].unique())
year_selected = st.sidebar.selectbox("연도 선택", years)

viewer_options = [col for col in df.columns if col not in ['year', 'app', 'title', 'description']]
viewer_selected = st.sidebar.selectbox("시청자 기준 선택", viewer_options)

top_apps = get_top_apps(df, year_selected, viewer_selected)

st.subheader(f"📈 {year_selected}년 {viewer_selected} 기준 앱 선호도")

# 색상 설정
top_apps_sorted = top_apps.sort_values(by=viewer_selected, ascending=False)
colors = make_color_scale(len(top_apps_sorted))

fig = px.bar(
    top_apps_sorted,
    x='app',
    y=viewer_selected,
    title=f"{year_selected}년 앱 선호도",
    text=viewer_selected
)

# 색 적용
fig.update_traces(marker_color=colors)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# 상위 앱 추천
show_recommendations(df, top_apps_sorted, viewer_selected)

