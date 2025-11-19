# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION & DATA LOAD ---

st.set_page_config(
    page_title="OTT 서비스 선호도 분석 및 콘텐츠 추천",
    layout="wide"
)

# 데이터 로드 및 캐싱 함수
@st.cache_data
def load_data(file_path):
    """CSV 파일을 불러오고 인코딩 오류를 처리합니다."""
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        st.warning("CSV 파일 인코딩 오류! 'euc-kr'로 재시도합니다.")
        return pd.read_csv(file_path, encoding='euc-kr')

# 분석 제외 칼럼
EXCLUDE_COLUMNS = ['연도', '구분1', '구분2', '사례수', 'OTT 비이용', '기타']

try:
    df_raw = load_data('video.csv') 
except FileNotFoundError:
    st.error("🚨 `video.csv` 파일을 프로젝트 최상위 폴더(Root)에서 찾을 수 없습니다. 경로를 확인해주세요.")
    st.stop() 


# --- PREPROCESSING ---

def preprocess_data(df):
    """Wide 포맷을 Long 포맷으로 변환"""
    ott_columns = [col for col in df.columns if col not in EXCLUDE_COLUMNS]
    df_long = pd.melt(
        df,
        id_vars=['연도', '구분1', '구분2'],
        value_vars=ott_columns,
        var_name='OTT',
        value_name='이용률(%)'
    )
    return df_long

df_long = preprocess_data(df_raw.copy())


# --- RECOMMENDATION DATA & FUNCTION ---
RECOMMENDATIONS = {
    '유튜브': {
        '추천': '인기 쇼츠, 브이로그 및 라이브 스트리밍',
        '설명': '1인 크리에이터의 **짧고 재미있는 숏폼 콘텐츠(Shorts)**와 실시간 소통이 가능한 **라이브 방송**이 모든 연령대에서 압도적인 인기를 보입니다.'
    },
    '넷플릭스': {
        '추천': '오리지널 K-드라마, 글로벌 시리즈 및 영화',
        '설명': '세계적인 성공을 거둔 **넷플릭스 오리지널 드라마** 시리즈와 전 세계에서 인기를 끄는 **블록버스터 영화**가 주력 콘텐츠입니다.'
    },
    '티빙': {
        '추천': 'CJ ENM 채널의 최신 예능/드라마 및 독점 오리지널',
        '설명': 'tvN, Mnet 등 **CJ ENM 계열 채널** VOD 시청이 가능하며, **'환승연애', '술꾼도시여자들'** 등 화제성 높은 독점 오리지널 콘텐츠가 인기입니다.'
    },
    '웨이브': {
        '추천': '지상파/종편 드라마 및 예능 다시보기',
        '설명': 'KBS, MBC, SBS 등 **지상파 3사**와 종편 채널의 **최신 드라마, 예능** 프로그램 VOD에 강점을 보입니다.'
    },
    '쿠팡플레이': {
        '추천': '독점 스포츠 생중계 및 SNL 코리아',
        '설명': 'K리그 등 **독점 스포츠 경기 생중계**와 젊은 층에게 인기 있는 **'SNL 코리아'** 등의 코미디 콘텐츠를 제공합니다.'
    },
    '디즈니플러스': {
        '추천': '마블, 스타워즈, 픽사 오리지널 시리즈',
        '설명': '**마블 시네마틱 유니버스(MCU)**, **스타워즈** 등 강력한 글로벌 프랜차이즈의 독점 오리지널 시리즈가 주요 콘텐츠입니다.'
    }
}

def get_recommendation_and_explanation(ott_name):
    """OTT 서비스별 일반적인 인기 콘텐츠 유형과 설명을 반환합니다."""
    return RECOMMENDATIONS.get(ott_name, {'추천': '정보 없음', '설명': '이 OTT 서비스에 대한 추천 정보가 준비되지 않았습니다.'})


# --- CHART GENERATION ---

def create_plotly_bar_chart(df, year, sub_division):
    
    filtered_data = df[
        (df['연도'] == year) &
        (df['구분2'] == sub_division)
    ].sort_values(by='이용률(%)', ascending=False).reset_index(drop=True)

    # 1등은 빨간색, 나머지는 파란색 그라데이션
    blue_shades = ['#0047AB', '#1f77b4', '#4682B4', '#6a9cbf', '#8db5ca', '#b1cde5', '#d3e6f0']
    colors = []
    for i in range(len(filtered_data)):
        if i == 0:
            colors.append('red') # 1등
        else:
            colors.append(blue_shades[(i - 1) % len(blue_shades)])

    fig = go.Figure(data=[
        go.Bar(
            x=filtered_data['이용률(%)'],
            y=filtered_data['OTT'],
            marker_color=colors,
            orientation='h',
            text=filtered_data['이용률(%)'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
        )
    ])

    fig.update_layout(
        title={'text': f"**{sub_division}의 OTT 서비스 선호 순위**", 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20}},
        xaxis_title="이용률 (%)",
        yaxis_title="OTT 서비스",
        yaxis={'categoryorder':'total ascending'},
        height=600,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    fig.update_traces(hovertemplate='<b>%{y}</b><br>이용률: %{x:.1f}%<extra></extra>')

    return fig, filtered_data 


# --- STREAMLIT INTERFACE ---

st.title("📺 OTT 서비스 선호도 인터랙티브 분석")
st.markdown("---")

# 1. 사이드바 구성 (사용자 입력)
with st.sidebar:
    st.header("⚙️ 분석 조건 선택")

    years = sorted(df_raw['연도'].unique())
    selected_year = st.selectbox("🗓️ 년도를 선택하세요:", years, index=len(years)-1)

    divisions = df_raw['구분1'].unique()
    selected_division_type = st.radio("👥 시청자 구분 기준:", divisions)

    filtered_df_by_type = df_raw[df_raw['구분1'] == selected_division_type]
    sub_divisions = sorted(filtered_df_by_type['구분2'].unique())
    selected_sub_division = st.selectbox(
        f"세부 {selected_division_type} 기준 선택:",
        sub_divisions
    )

st.header(f"📊 {selected_year}년, {selected_sub_division}의 OTT 이용률 순위")
st.write(f"**기준**: **{selected_year}년** / **{selected_sub_division}** (단위: %) - **OTT 비이용, 기타 제외**")
st.markdown("---")


# 그래프 생성 및 데이터 추출
if not df_long.empty:
    chart, ranked_data = create_plotly_bar_chart(df_long, selected_year, selected_sub_division)
    st.plotly_chart(chart, use_container_width=True)
    
    # --- Top 3 콘텐츠 추천 섹션 ---
    st.markdown("---")
    st.subheader("🥇 Top 3 OTT 서비스 인기 콘텐츠 추천 및 설명")
    
    top_3_otts = ranked_data['OTT'].head(3).tolist()
    
    cols = st.columns(3)
    
    for i, ott_name in enumerate(top_3_otts):
        recommendation = get_recommendation_and_explanation(ott_name)
        rank = i + 1
        utilization_rate = ranked_data.iloc[i]["이용률(%)"]
        
        # HTML 스타일 문자열을 단순화하여 직접 마크다운에 삽입하지 않고, 
        # f-string을 이용하여 깔끔하게 구성합니다.
        
        # 1. 스타일 클래스 정의 (실제 Streamlit에서는 CSS 파일이 없으므로 인라인 스타일 유지)
        if rank == 1:
            color_style = "background-color: #ffeaea; border-left: 5px solid red; padding: 10px; border-radius: 5px;"
        else:
            color_style = "background-color: #eaf3ff; border-left: 5px solid #0047AB; padding: 10px; border-radius: 5px;"
            
        
        # 2. 카드 콘텐츠 생성 (백틱(``)이나 ''' 트리플 쿼트를 사용하지 않고, 
        # 따옴표 사용을 최소화하여 파이썬 컴파일러의 부담을 줄입니다)
        card_content = (
            f'<div style="{color_style}">'
            f'<h4><b>{rank}위: {ott_name}</b> ({utilization_rate:.1f}%)</h4>'
            f'<p><b>📌 주요 인기 콘텐츠</b>: {recommendation["추천"]}</p>'
            f'<p><b>💬 설명</b>: {recommendation["설명"]}</p>'
            '</div>'
        )
        
        with cols[i]:
            st.markdown(card_content, unsafe_allow_html=True)


else:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다. 필터 조건을 확인해주세요.")

# 하단에 원본 데이터 테이블 표시
st.markdown("---")
with st.expander("원본 데이터 테이블 보기"):
    st.dataframe(df_raw[
        (df_raw['연도'] == selected_year) & 
        (df_raw['구분2'] == selected_sub_division)
    ].reset_index(drop=True), use_container_width=True)
