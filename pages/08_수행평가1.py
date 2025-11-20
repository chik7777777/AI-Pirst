import streamlit as st
import pandas as pd
import chardet

# -----------------------
# 1) CSV 자동 인코딩 감지
# -----------------------
def load_data(path):
    # 파일 인코딩 자동 탐지
    with open(path, "rb") as f:
        enc = chardet.detect(f.read())["encoding"]

    # CSV 읽기
    df = pd.read_csv(path, encoding=enc)

    # 컬럼명 공백 제거
    df.columns = [c.strip() for c in df.columns]

    return df


# -----------------------
# 2) 연도 컬럼 자동 탐색
# -----------------------
def find_year_column(df):
    candidates = ["year", "Year", "YEAR", "yr", "년도", "연도"]
    for col in df.columns:
        if col.strip() in candidates:
            return col
    return None


# -----------------------
# 3) 메인 코드
# -----------------------
st.title("데이터 분석 대시보드")

# 업로드 혹은 고정 파일 사용
csv_path = "your_file.csv"   # 📌 CSV 파일명을 여기에 입력 또는 업로드 기능으로 변경 가능

df = load_data(csv_path)

# 컬럼 보기
st.subheader("📌 CSV 컬럼명")
st.write(df.columns.tolist())

# 연도 컬럼 자동 탐색
year_col = find_year_column(df)

if year_col is None:
    st.error("❗ CSV 파일 안에서 '연도(year)'로 판단되는 컬럼을 찾을 수 없습니다.")
    st.stop()

# -----------------------
# 4) 연도 선택 UI
# -----------------------
year_selected = st.sidebar.selectbox("연도 선택", sorted(df[year_col].unique()))

# 해당 연도 데이터 필터
filtered = df[df[year_col] == year_selected]

st.subheader(f"📊 {year_selected}년 데이터")
st.dataframe(filtered)

# -----------------------
# 5) 기본 통계
# -----------------------
st.subheader("📈 기본 통계 정보")
st.write(filtered.describe())

