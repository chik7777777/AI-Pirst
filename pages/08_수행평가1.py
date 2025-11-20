# pages/06_video_app.py
# Streamlit page (single-file) that loads ../video.csv and shows interactive Plotly charts.
# Requirements section removed.

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Video App Preference Explorer", layout="wide")

st.title("📊 어떤 어플을 선호했을까? — Video App Preference Explorer")
st.write("CSV 파일: `../video.csv` 를 불러와 분석합니다. (pages 폴더 내부에서 실행하세요)")

@st.cache_data
def load_data(path: str = "../video.csv"):
    for e in ["cp949", "euc-kr", "utf-8", "latin1"]:
        try:
            df = pd.read_csv(path, encoding=e)
            return df, e
        except Exception:
            pass
    raise RuntimeError(f"파일을 불러오지 못했습니다. 경로와 인코딩을 확인하세요: {path}")

try:
    df, used_encoding = load_data()
    st.sidebar.success(f"Loaded ../video.csv (encoding={used_encoding})")
except Exception as e:
    st.sidebar.error(str(e))
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("컬럼 자동 감지 (수정 가능)")

cols = df.columns.tolist()

def detect_column(candidates):
    for c in candidates:
        for col in cols:
            if col.lower() == c:
                return col
    for c in candidates:
        for col in cols:
            if c in col.lower():
                return col
    return None

year_col = detect_column(["year", "upload_year", "date"])
app_col = detect_column(["app", "platform"])
views_col = detect_column(["views", "view_count", "watch"])
likes_col = detect_column(["likes", "like_count"])
comments_col = detect_column(["comments", "comment_count"])
viewer_col = detect_column(["viewer", "audience", "age", "gender", "viewer_type"])

st.sidebar.markdown("자동 감지 결과를 확인하고 수정하세요:")
selected_year_col = st.sidebar.selectbox("연도 컬럼", options=[None] + cols, index=(cols.index(year_col) if year_col in cols else 0))
selected_app_col = st.sidebar.selectbox("어플/플랫폼 컬럼", options=[None] + cols, index=(cols.index(app_col) if app_col in cols else 0))
selected_views_col = st.sidebar.selectbox("조회수 컬럼", options=[None] + cols, index=(cols.index(views_col) if views_col in cols else 0))
selected_likes_col = st.sidebar.selectbox("좋아요 컬럼", options=[None] + cols, index=(cols.index(likes_col) if likes_col in cols else 0))
selected_viewer_col = st.sidebar.selectbox("시청자 기준 컬럼", options=[None] + cols, index=(cols.index(viewer_col) if viewer_col in cols else 0))

if not selected_app_col:
    st.error("어플/플랫폼 컬럼을 선택해주세요.")
    st.stop()

use_year_filter = False
if selected_year_col in df.columns:
    try:
        df['_parsed_date'] = pd.to_datetime(df[selected_year_col], errors='coerce')
        if df['_parsed_date'].notnull().any():
            df['_year'] = df['_parsed_date'].dt.year
        else:
            if pd.api.types.is_numeric_dtype(df[selected_year_col]):
                df['_year'] = df[selected_year_col]
        use_year_filter = True
    except:
        use_year_filter = False

st.sidebar.markdown("---")
st.sidebar.header("필터")

if use_year_filter:
    years = sorted(df['_year'].dropna().unique().tolist())
    selected_year = st.sidebar.selectbox("연도", options=["전체"] + [str(int(y)) for y in years])
else:
    selected_year = "전체"

viewer_values = None
if selected_viewer_col in df.columns:
    viewer_values = sorted(df[selected_viewer_col].dropna().unique().tolist())
    selected_viewer = st.sidebar.selectbox("시청자 기준 값", options=["전체"] + [str(v) for v in viewer_values])
else:
    selected_viewer = "전체"

filtered = df.copy()
if use_year_filter and selected_year != "전체":
    filtered = filtered[filtered['_year'] == int(selected_year)]
if selected_viewer_col and selected_viewer != "전체":
    filtered = filtered[filtered[selected_viewer_col] == selected_viewer]

st.write(f"**필터된 데이터 수:** {len(filtered)}")

weight_col = selected_views_col if selected_views_col in filtered.columns else None
if weight_col:
    agg = filtered.groupby(selected_app_col)[weight_col].sum().reset_index(name='weight')
else:
    agg = filtered[selected_app_col].value_counts().reset_index()
    agg.columns = [selected_app_col, 'weight']

agg = agg.sort_values('weight', ascending=False)
apps = agg[selected_app_col].astype(str).tolist()
colors = []
if apps:
    colors.append('rgba(255,0,0,1)')
    n_other = max(1, len(apps)-1)
    base = np.array([31,119,180])
    for i in range(n_other):
        t = i / max(1, n_other-1)
        rgb = (base * (1 - 0.6*t) + 255 * (0.6*t)).astype(int)
        alpha = 1 - (0.3 * t)
        colors.append(f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha:.2f})')
colors = colors[:len(apps)]

if len(agg) == 0:
    st.warning("표시할 데이터가 없습니다.")
else:
    fig = px.bar(agg, x=selected_app_col, y='weight', title="앱 선호도", text='weight')
    fig.update_traces(marker_color=colors)
    fig.update_layout(xaxis_title='앱', yaxis_title='값')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.header("🏆 상위 3개 앱 인기 영상 추천")

    top_n = agg.head(3)
    for rank, row in enumerate(top_n.itertuples(index=False), start=1):
        app_name = getattr(row, selected_app_col)
        st.subheader(f"{rank}위 — {app_name}")
        app_videos = filtered[filtered[selected_app_col] == app_name]

        sort_by = selected_views_col if selected_views_col in app_videos.columns else None
        if sort_by:
            app_videos = app_videos.sort_values(sort_by, ascending=False)
        top_videos = app_videos.head(3)

        title_col = None
        for c in ['title','video_title','name','title_text']:
            if c in app_videos.columns:
                title_col = c
                break

        for vid_idx, vid in top_videos.iterrows():
            title = vid[title_col] if title_col else f"Row {vid_idx}"
            reason = []
            if sort_by:
                reason.append(f"{sort_by} 높음")
            st.write(f"- **{title}** — {' / '.join(reason) if reason else '정보 부족'}")

st.sidebar.markdown("---")
st.sidebar.header("실행 방법")
st.sidebar.code("streamlit run pages/06_video_app.py")
