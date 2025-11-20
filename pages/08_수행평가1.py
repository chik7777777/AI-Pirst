# pages/06_video_app.py
# 완전 새로 작성된 Streamlit + Plotly 기반 분석 앱 코드
# CSV: ../video.csv

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Video Preference Dashboard", layout="wide")

st.title("📊 Video Preference Dashboard — 앱 선호도 분석")
st.write("`../video.csv` 파일을 기반으로 연도·시청자 조건에 따른 앱 선호도를 시각적으로 분석하는 Streamlit 앱입니다.")

# ----------------------------
# 데이터 로드
# ----------------------------
@st.cache_data
def load_data():
    encodings = ["cp949", "utf-8", "euc-kr", "latin1"]
    for enc in encodings:
        try:
            df = pd.read_csv("../video.csv", encoding=enc)
            return df, enc
        except:
            pass
    st.error("CSV 파일을 읽을 수 없습니다. 경로 또는 인코딩을 확인하세요.")
    st.stop()


df, used_enc = load_data()
st.sidebar.success(f"CSV Loaded (encoding={used_enc})")

# ----------------------------
# 자동 컬럼 감지
# ----------------------------
cols = df.columns.tolist()


def detect(cands):
    for c in cands:
        for col in cols:
            if col.lower() == c:
                return col
    for c in cands:
        for col in cols:
            if c in col.lower():
                return col
    return None


year_col = detect(["year", "upload_year", "date"])
app_col = detect(["app", "platform"])
views_col = detect(["views", "view_count", "watch"])
viewer_col = detect(["viewer", "audience", "age", "gender"])

st.sidebar.header("컬럼 설정")

year_col = st.sidebar.selectbox("연도 컬럼", [None] + cols, index=(cols.index(year_col) if year_col in cols else 0))
app_col = st.sidebar.selectbox("앱/플랫폼 컬럼", [None] + cols, index=(cols.index(app_col) if app_col in cols else 0))
views_col = st.sidebar.selectbox("조회수 컬럼", [None] + cols, index=(cols.index(views_col) if views_col in cols else 0))
viewer_col = st.sidebar.selectbox("시청자 기준 컬럼", [None] + cols, index=(cols.index(viewer_col) if viewer_col in cols else 0))

if not app_col:
    st.error("앱/플랫폼 컬럼을 반드시 선택해야 합니다.")
    st.stop()

# ----------------------------
# 연도 처리
# ----------------------------
if year_col:
    try:
        df["_date"] = pd.to_datetime(df[year_col], errors="coerce")
        if df["_date"].notnull().any():
            df["_year"] = df["_date"].dt.year
        else:
            df["_year"] = df[year_col].astype(str).str.extract(r"(20\\d{2}|19\\d{2})")[0]
    except:
        df["_year"] = None
else:
    df["_year"] = None

# ----------------------------
# 사이드바 필터
# ----------------------------
st.sidebar.header("필터")

years = sorted(df["_year"].dropna().unique().tolist()) if df["_year"].notnull().any() else []
selected_year = st.sidebar.selectbox("연도 선택", ["전체"] + [str(int(y)) for y in years])

if viewer_col:
    viewers = sorted(df[viewer_col].dropna().unique().tolist())
    selected_viewer = st.sidebar.selectbox("시청자 기준", ["전체"] + [str(v) for v in viewers])
else:
    selected_viewer = "전체"

# ----------------------------
# 필터 적용
# ----------------------------
filtered = df.copy()

if selected_year != "전체" and "_year" in df.columns:
    filtered = filtered[filtered["_year"] == int(selected_year)]

if viewer_col and selected_viewer != "전체":
    filtered = filtered[filtered[viewer_col] == selected_viewer]

st.write(f"### 🔎 필터된 데이터 수: {len(filtered)} rows")

# ----------------------------
# 앱별 선호도 계산
# ----------------------------
if views_col:
    agg = (
        filtered.groupby(app_col)[views_col]
        .sum()
        .reset_index(name="weight")
        .sort_values("weight", ascending=False)
    )
else:
    agg = filtered[app_col].value_counts().reset_index()
    agg.columns = [app_col, "weight"]
    agg = agg.sort_values("weight", ascending=False)

# ----------------------------
# 색상: 1등 빨간색 + 파란색 그라데이션
# ----------------------------
colors = []
apps = agg[app_col].astype(str).tolist()

if len(apps) > 0:
    colors.append("rgba(255,0,0,1)")  # 1위 빨간색
    base = np.array([31, 119, 180])
    n = len(apps) - 1
    for i in range(n):
        t = i / max(1, n - 1)
        rgb = (base * (1 - 0.7 * t) + 255 * (0.7 * t)).astype(int)
        alpha = 1 - 0.4 * t
        colors.append(f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha:.2f})")

# ----------------------------
# 막대 그래프 생성
# ----------------------------
fig = px.bar(
    agg,
    x=app_col,
    y="weight",
    title=f"앱 선호도 분석 (연도={selected_year}, 시청자={selected_viewer})",
    text="weight"
)

fig.update_traces(marker_color=colors)
fig.update_layout(xaxis_title="앱", yaxis_title="조회수 또는 빈도")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 상위 3 앱 영상 추천
# ----------------------------
st.markdown("---")
st.header("🏆 상위 3개 앱 인기 영상 추천")

for rank, row in enumerate(agg.head(3).itertuples(index=False), start=1):
    app_name = getattr(row, app_col)
    st.subheader(f"{rank}위 — {app_name}")

    app_data = filtered[filtered[app_col] == app_name]
    if views_col in app_data.columns:
        app_data = app_data.sort_values(views_col, ascending=False)

    title_col = None
    for c in ["title", "video_title", "name", "title_text"]:
        if c in app_data.columns:
            title_col = c
            break

    for vid in app_data.head(3).itertuples():
        title = getattr(vid, title_col) if title_col else "제목 정보 없음"
        reason = []
        if views_col:
            reason.append(f"조회수 높음 ({getattr(vid, views_col)})")
        st.write(f"- **{title}** — {' / '.join(reason) if reason else '데이터 부족'}")

# ----------------------------
# 실행 방법
# ----------------------------
st.sidebar.markdown("---")
st.sidebar.header("실행 방법")
st.sidebar.code("streamlit run pages/06_video_app.py")

