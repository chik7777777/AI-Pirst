import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지도 🌏", layout="wide")

st.title("🌸 외국인들이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 인기 명소를 지도에서 보고, 각 명소에 대한 설명도 아래에서 확인해보세요!")

# 관광지 데이터
locations = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, "desc": "조선 왕조의 중심 궁궐로, 한국 전통 건축의 정수를 느낄 수 있는 곳이에요.", "station": "경복궁역 (3호선)"},
    {"name": "명동", "lat": 37.563757, "lon": 126.982705, "desc": "쇼핑, 길거리 음식, K-뷰티로 외국인 관광객들에게 가장 인기 많은 거리예요.", "station": "명동역 (4호선)"},
    {"name": "남산타워 (N서울타워)", "lat": 37.551169, "lon": 126.988227, "desc": "서울의 랜드마크이자 야경 명소로, 사랑의 자물쇠로도 유명해요.", "station": "명동역 (4호선)"},
    {"name": "홍대거리", "lat": 37.556332, "lon": 126.923611, "desc": "젊음과 예술, 버스킹과 클럽 문화가 어우러진 트렌디한 거리예요.", "station": "홍대입구역 (2호선, 경의중앙선)"},
    {"name": "북촌 한옥마을", "lat": 37.582604, "lon": 126.983998, "desc": "전통 한옥이 아름답게 보존된 서울의 대표적인 전통 마을이에요.", "station": "안국역 (3호선)"},
    {"name": "인사동", "lat": 37.574017, "lon": 126.985759, "desc": "전통 찻집, 갤러리, 기념품 가게가 즐비한 한국 전통 거리예요.", "station": "종로3가역 (1·3·5호선)"},
    {"name": "동대문 디자인 플라자 (DDP)", "lat": 37.566541, "lon": 127.009155, "desc": "푸 futuristic한 건축과 패션쇼로 유명한 서울의 디자인 허브예요.", "station": "동대문역사문화공원역 (2·4·5호선)"},
    {"name": "롯데월드", "lat": 37.511011, "lon": 127.098165, "desc": "실내외 놀이시설과 쇼핑몰이 함께 있는 도심형 테마파크예요.", "station": "잠실역 (2·8호선)"},
    {"name": "잠실 롯데타워", "lat": 37.513068, "lon": 127.102493, "desc": "세계 5위 높이의 초고층 빌딩으로, 전망대에서 서울 전경을 볼 수 있어요.", "station": "잠실역 (2·8호선)"},
    {"name": "청계천", "lat": 37.570207, "lon": 126.978134, "desc": "도심 속 힐링 산책로로, 서울의 역사와 현대가 어우러진 곳이에요.", "station": "광화문역 (5호선)"}
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 색상 순환용 리스트
colors = ["red", "blue", "green", "purple", "orange", "cadetblue", "darkred", "darkgreen", "lightgray", "pink"]

# 관광지 마커 추가
for i, place in enumerate(locations):
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}<br><i>가장 가까운 지하철역: {place['station']}</i>",
        tooltip=place["name"],
        icon=folium.Icon(color=colors[i % len(colors)], icon="star")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=750, height=500)

# 지도 아래 상세 설명
st.subheader("🗺 관광지 상세 정보")

for place in locations:
    st.markdown(f"""
    ### {place['name']}
    - 📝 **소개:** {place['desc']}
    - 🚇 **가까운 지하철역:** {place['station']}
    ---
    """)

st.caption("📍 데이터 출처: VisitSeoul, TripAdvisor, Google Maps 기준")
