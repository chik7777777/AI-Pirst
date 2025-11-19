import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 설정 및 데이터 로드 ---

# 1. 페이지 설정
st.set_page_config(
    page_title="OTT 서비스 선호도 분석",
    layout="wide"
)

# 2. 데이터 로드 및 캐싱
# 경로를 'video.csv'로 수정하여 Streamlit Root 폴더에서 파일을 찾도록 합니다.
@st.cache_data
def load_data(file_path):
    """CSV 파일을 불러오고 인코딩 오류를 처리합니다."""
    try:
        # 파일 경로 수정: '../video.csv' -> 'video.csv'
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        # utf-8이 아닐 경우 euc-kr로 재시도
        st.error("CSV 파일 인코딩 오류! 'euc-kr'로 재시도합니다.")
        return pd.read_csv(file_path, encoding='euc-kr')

# 분석에서 제외할 칼럼 리스트
EXCLUDE_COLUMNS = ['연도', '구분1', '구분2', '사례수', 'OTT 비이용', '기타']

try:
    # 파일 로드 시 'video.csv'를 인수로 전달
    df_raw = load_data('video.csv') 
except FileNotFoundError:
    st.error("🚨 `video.csv` 파일을 프로젝트 최상위 폴더(Root)에서 찾을 수 없습니다. 경로를 확인해주세요.")
    st.stop() # 파일을 찾지 못하면 앱 실행 중지


# --- 데이터 전처리 함수 ---
def preprocess_data(df):
    """분석에 필요한 데이터프레임으로 Long 포맷으로 변환합니다."""
    # 분석 대상 OTT 칼럼 추출
    ott_columns = [col for col in df.columns if col not in EXCLUDE_COLUMNS]

    # Wide 포맷을 Long 포맷으로 변환
    df_long = pd.melt(
        df,
        id_vars=['연도', '구분1', '구분2'],
        value_vars=ott_columns,
        var_name='OTT',
        value_name='이용률(%)'
    )
    return df_long

df_long = preprocess_data(df_raw.copy())


# --- Streamlit 인터페이스 구성 ---

st.title("📺 OTT 서비스 선호도 인터랙티브 분석")
st.markdown("---")

# 1. 사이드바 구성 (사용자 입력)
with st.sidebar:
    st.header("⚙️ 분석 조건 선택")

    # 년도 선택
    years = sorted(df_raw['연도'].unique())
    selected_year = st.selectbox("🗓️ 년도를 선택하세요:", years, index=len(years)-1)

    # 구분 기준 ('구분1' - 성별/연령별) 선택
    divisions = df_raw['구분1'].unique()
    selected_division_type = st.radio("👥 시청자 구분 기준:", divisions)

    # 선택된 '구분1'에 해당하는 '구분2' (세부 기준) 선택
    filtered_df_by_type = df_raw[df_raw['구분1'] == selected_division_type]
    sub_divisions = sorted(filtered_df_by_type['구분2'].unique())
    selected_sub_division = st.selectbox(
        f"세부 {selected_division_type} 기준 선택:",
        sub_divisions
    )

st.header(f"📊 {selected_year}년, {selected_sub_division}의 OTT 이용률 순위")
st.write(f"**기준**: **{selected_year}년** / **{selected_sub_division}** (단위: %) - **OTT 비이용, 기타 제외**")
st.markdown("---")


# --- 데이터 필터링 및 그래프 생성 ---

def create_plotly_bar_chart(df, year, sub_division):
    # 1. 필터링 및 순위 정렬
    filtered_data = df[
        (df['연도'] == year) &
        (df['구분2'] == sub_division)
    ].sort_values(by='이용률(%)', ascending=False).reset_index(drop=True)

    # 2. 순위 및 컬러 맵핑
    # 1등은 빨간색, 나머지는 파란색 그라데이션으로 흐려지게 설정
    
    # 2등부터 사용할 파란색 톤 리스트 (진한 파랑에서 옅은 파랑 순)
    blue_shades = [
        '#0047AB', # 2등 (진한 파랑)
        '#1f77b4', 
        '#4682B4', 
        '#6a9cbf', 
        '#8db5ca',
        '#b1cde5',
        '#d3e6f0', # 옅은 파랑
    ]
    
    colors = []
    for i in range(len(filtered_data)):
        if i == 0:
            colors.append('red') # 1등은 빨간색
        else:
            # 2등부터 blue_shades를 순환하며 색상 할당
            colors.append(blue_shades[(i - 1) % len(blue_shades)])

    # 3. Plotly 그래프 생성
    fig = go.Figure(data=[
        go.Bar(
            x=filtered_data['이용률(%)'],
            y=filtered_data['OTT'],
            marker_color=colors,
            orientation='h',
            text=filtered_data['이용률(%)'].apply(lambda x: f'{x:.1f}%'), # 막대 위에 텍스트 표시
            textposition='outside',
        )
    ])

    # 4. 레이아웃 설정
    fig.update_layout(
        title={
            'text': f"**{sub_division}의 OTT 서비스 선호 순위**",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20}
        },
        xaxis_title="이용률 (%)",
        yaxis_title="OTT 서비스",
        yaxis={'categoryorder':'total ascending'}, # 이용률이 높은 순서로 정렬된 채로 보여주기
        height=600,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # 5. 인터랙티브 기능 추가 (호버 텍스트)
    fig.update_traces(hovertemplate='<b>%{y}</b><br>이용률: %{x:.1f}%<extra></extra>')

    return fig

# 그래프 그리기 및 Streamlit에 표시
if not df_long.empty:
    chart = create_plotly_bar_chart(df_long, selected_year, selected_sub_division)
    st.plotly_chart(chart, use_container_width=True)
else:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다. 필터 조건을 확인해주세요.")

# 하단에 원본 데이터 테이블 표시
with st.expander("데이터 테이블 보기"):
    st.dataframe(df_raw[
        (df_raw['연도'] == selected_year) & 
        (df_raw['구분2'] == selected_sub_division)
    ].reset_index(drop=True), use_container_width=True)
