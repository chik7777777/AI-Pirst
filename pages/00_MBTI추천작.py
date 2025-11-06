# streamlit_app.py
import streamlit as st

def get_recommendations():
    PLACEHOLDER = "https://via.placeholder.com/300x450?text=Poster"

    # 추천 데이터 (간단화된 예시; 필요하면 poster 값을 실제 URL로 교체)
    return {
        "ISTJ": {
            "books": [
                {"title": "82년생 김지영", "author": "조남주",
                 "reason": "현실적이고 책임감 강한 ISTJ에게 차분히 사회와 개인을 돌아보게 해줘요.",
                 "poster": PLACEHOLDER},
                {"title": "아몬드", "author": "손원평",
                 "reason": "감정과 공감에 대해 생각할 거리를 주는 작품이에요.",
                 "poster": PLACEHOLDER}
            ],
            "movies": [
                {"title": "기생충", "director": "봉준호",
                 "reason": "세밀한 관찰과 구조적 메시지가 인상적인 영화예요.",
                 "poster": PLACEHOLDER},
                {"title": "택시운전사", "director": "장훈",
                 "reason": "사실 기반의 묵직한 이야기로 공감이 가요.",
                 "poster": PLACEHOLDER}
            ]
        },
        "ISFJ": {
            "books": [
                {"title": "우리들의 일그러진 영웅", "author": "이문열",
                 "reason": "타인을 돌보는 마음과 사회 규칙을 생각하게 해줘요.",
                 "poster": PLACEHOLDER},
                {"title": "완득이", "author": "김려령",
                 "reason": "따뜻한 시선의 성장 이야기로 공감 능력이 큰 분께 좋아요.",
                 "poster": PLACEHOLDER}
            ],
            "movies": [
                {"title": "국제시장", "director": "윤제균",
                 "reason": "가족과 헌신을 중요하게 여기는 분께 울림을 줍니다.",
                 "poster": PLACEHOLDER},
                {"title": "소원", "director": "이준익",
                 "reason": "치유와 회복을 다루는 감성적인 영화예요.",
                 "poster": PLACEHOLDER}
            ]
        },
        # 나머지 MBTI 유형도 같은 형식으로 추가 — 예시로 일부만 넣었습니다.
        "ENFP": {
            "books": [
                {"title": "오직 두 사람", "author": "강지영",
                 "reason": "상상력과 관계 묘사를 좋아하는 ENFP에게 잘 맞아요.",
                 "poster": PLACEHOLDER},
                {"title": "알려지지 않은 밤과 하루", "author": "공지영",
                 "reason": "다채로운 감정선과 이야기의 결합이 매력적이에요.",
                 "poster": PLACEHOLDER}
            ],
            "movies": [
                {"title": "극장에서 만난 사람들", "director": "김종관",
                 "reason": "감성적이고 자유로운 분위기를 즐기는 분께 추천해요.",
                 "poster": PLACEHOLDER},
                {"title": "비밀은 없다", "director": "이창동",
                 "reason": "사건과 인간 드라마가 어우러져 생각할 거리를 줘요.",
                 "poster": PLACEHOLDER}
            ]
        }
    }

def show_item(item, kind="book", placeholder="https://via.placeholder.com/300x450?text=Poster"):
    left, right = st.columns([1, 2])
    img_url = item.get("poster") or placeholder
    with left:
        try:
            st.image(img_url, use_column_width=True)
        except Exception:
            # 이미지 로딩 실패 시 플레이스홀더로 대체
            st.image(placeholder, use_column_width=True)
    with right:
        title = item.get("title", "제목 없음")
        if kind == "book":
            author = item.get("author", "작가 정보 없음")
            st.markdown(f"**{title}** — {author}")
        else:
            director = item.get("director", "감독 정보 없음")
            st.markdown(f"**{title}** — 감독: {director}")
        reason = item.get("reason", "")
        if reason:
            st.write(reason)

def main():
    st.set_page_config(page_title="MBTI 북·무비 추천", page_icon="📚", layout="centered")

    st.title("MBTI로 고르는 한국 책 + 영화 추천")
    st.write("MBTI를 골라주면 딱 맞는 한국 책 2권과 영화 2편을 추천해줄게요. ✨")
    st.write("포스터가 없으면 플레이스홀더가 보일 수 있어요. (포스터 URL을 바꾸면 실제 이미지가 나옵니다.)")

    MBTIS = [
        "ISTJ","ISFJ","INFJ","INTJ",
        "ISTP","ISFP","INFP","INTP",
        "ESTP","ESFP","ENFP","ENTP",
        "ESTJ","ESFJ","ENFJ","ENTJ"
    ]

    selected = st.selectbox("당신의 MBTI를 골라줘", MBTIS)

    recommendations = get_recommendations()

    if selected not in recommendations:
        st.warning("해당 MBTI에 대한 데이터가 아직 준비되지 않았어요. 다른 유형을 골라볼래요? 😊")
        return

    data = recommendations[selected]
    st.markdown(f"### {selected} 추천 리스트 💡")
    st.write("아래는 책 2권과 영화 2편이에요 — 추천 이유와 포스터를 함께 보여줘요.")

    st.write("**📚 책 추천**")
    for book in data.get("books", []):
        show_item(book, kind="book")
        st.write("")

    st.write("---")
    st.write("**🎬 영화 추천**")
    for mv in data.get("movies", []):
        show_item(mv, kind="movie")
        st.write("")

    st.caption("포스터가 표시되지 않으면 'poster' 값을 실제 이미지 URL로 바꿔보세요. 예: https://example.com/poster.jpg")
    st.markdown("---")
    st.write("앱 제작: ChatGPT — 더 채워넣거나 문구 바꿀 부분 있으면 말해줘요!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 파싱(문법) 오류는 여기서 잡히지는 않지만
        # 런타임 에러가 나면 사용자에게 보여주도록 처리합니다.
        st.error("앱 실행 중 오류가 발생했어요. 아래 에러 메시지를 확인해 주세요.")
        st.exception(e)
