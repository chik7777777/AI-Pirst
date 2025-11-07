# streamlit_app.py
import streamlit as st

st.set_page_config(page_title="MBTI별 추천 도서·영화 🎧📚", layout="centered")

MBTI_DATA = {
    "INTJ": {
        "books": [
            {"title": "채식주의자", "author": "한강", "reason": "심리와 상징으로 이야기를 풀어가는 작품이라 깊게 생각하는 INTJ에게 자극적이에요."},
            {"title": "아몬드", "author": "손원평", "reason": "감정의 구조를 차분히 관찰하는 이야기 — 논리적으로 감정을 이해하고 싶은 분께 좋아요."}
        ],
        "movies": [
            {"title": "기생충", "reason": "사회구조를 꿰뚫어보는 날카로운 서사가 있어요. 분석적인 재미가 쏠쏠합니다."},
            {"title": "버닝", "reason": "여백과 암시가 많은 영화라 해석하는 재미가 있어요 — 혼자 여러 번 곱씹기 좋아요."}
        ]
    },
    "INTP": {
        "books": [
            {"title": "소년이 온다", "author": "한강", "reason": "사건과 인간을 깊게 들여다보는 문체가 호기심 많은 INTP에게 맞아요."},
            {"title": "살인자의 기억법", "author": "김영하", "reason": "논리와 퍼즐 같은 전개가 마음을 자극해요."}
        ],
        "movies": [
            {"title": "올드보이", "reason": "복잡한 플롯과 충격적 반전이 많아 추리/해석을 즐기는 분께 추천합니다."},
            {"title": "암살", "reason": "역사 배경 속에서 퍼즐처럼 이어지는 이야기가 매력적이에요."}
        ]
    },
    "INFJ": {
        "books": [
            {"title": "82년생 김지영", "author": "조남주", "reason": "사회와 개인의 연결을 섬세하게 보여줘서 공감 능력 큰 INFJ에게 와닿아요."},
            {"title": "완득이", "author": "김려령", "reason": "사람에 대한 따뜻한 시선과 성장 이야기가 마음을 울립니다."}
        ],
        "movies": [
            {"title": "그렇게 아버지가 된다", "reason": "가족과 정체성에 관한 섬세한 드라마로 감정 이입하기 좋아요."},
            {"title": "7번방의 선물", "reason": "진한 감동과 따뜻함이 있어 마음을 챙기기 좋은 작품이에요."}
        ]
    },
    "INFP": {
        "books": [
            {"title": "죽고 싶지만 떡볶이는 먹고 싶어", "author": "백세희", "reason": "솔직한 내면 고백이 많은 에세이로 위로가 되는 책이에요."},
            {"title": "아몬드", "author": "손원평", "reason": "감정의 미묘함을 따라가는 이야기가 감성적인 INFP에게 잘 맞아요."}
        ],
        "movies": [
            {"title": "우리들", "reason": "청소년의 미묘한 감정과 관계를 진솔하게 그려 공감이 잘 가요."},
            {"title": "건축학개론", "reason": "첫사랑의 감성을 잔잔하게 불러오는 영화라 마음에 남습니다."}
        ]
    },
    "ENTJ": {
        "books": [
            {"title": "미생", "author": "윤태호 (웹툰)", "reason": "조직과 전략, 성장 이야기가 있어 목표 지향적인 ENTJ에게 자극적이에요."},
            {"title": "태백산맥", "author": "조정래", "reason": "거대한 서사와 역사적 맥락에서 리더십과 선택을 생각하게 합니다."}
        ],
        "movies": [
            {"title": "명량", "reason": "리더십, 결단력, 팀워크 같은 요소가 돋보여서 통찰을 줍니다."},
            {"title": "국가대표", "reason": "목표에 집착하고 성취를 쟁취해나가는 이야기라 동기부여에 좋아요."}
        ]
    },
    "ENTP": {
        "books": [
            {"title": "김영하의 여행의 이유", "author": "김영하", "reason": "다양한 생각과 반짝이는 문장이 많아 상상력 자극에 좋습니다."},
            {"title": "살인자의 기억법", "author": "김영하", "reason": "기발한 설정과 전개가 ENTP의 호기심을 자극해요."}
        ],
        "movies": [
            {"title": "곡성", "reason": "해석이 분분한 미스터리로 토론하고 싶은 마음이 샘솟아요."},
            {"title": "암살", "reason": "다양한 사건과 트릭, 빠른 흐름이 흥미진진합니다."}
        ]
    },
    "ENFJ": {
        "books": [
            {"title": "그리스인 조르바", "author": "니코스 카잔차키스 (번역서)", "reason": "사람과 삶을 북돋는 이야기로 타인을 이끄는 ENFJ에게 영감이 돼요."},
            {"title": "완두콩", "author": "정세랑", "reason": "사람 사이의 따뜻한 연결을 유머 있게 보여줘요."}
        ],
        "movies": [
            {"title": "국제시장", "reason": "가족과 희생에 관한 드라마로 공동체 의식을 자극합니다."},
            {"title": "우아한 세계", "reason": "타인을 이해하려는 마음을 건드리는 작품이에요."}
        ]
    },
    "ENFP": {
        "books": [
            {"title": "그해의 여름", "author": "정세랑", "reason": "기발하고 따뜻한 상상력이 ENFP의 감성을 채워줘요."},
            {"title": "고래", "author": "정세랑", "reason": "유머와 진심이 공존하는 문장이 자유로운 에너지를 줍니다."}
        ],
        "movies": [
            {"title": "라라랜드", "reason": "꿈과 열정, 로맨스가 어우러져 감성적 에너지 충전해줘요."},
            {"title": "건축학개론", "reason": "추억과 감성에 집중하는 ENFP에게 힐링됩니다."}
        ]
    },
    "ISTJ": {
        "books": [
            {"title": "완득이", "author": "김려령", "reason": "꾸준한 성장과 책임감 있는 인물이 나와 안정감 있게 읽을 수 있어요."},
            {"title": "칼의 노래", "author": "김훈", "reason": "정직하고 묵직한 문체가 ISTJ의 성향에 잘 맞습니다."}
        ],
        "movies": [
            {"title": "국제시장", "reason": "성실함과 가족애를 중심으로 한 서사가 마음에 들어요."},
            {"title": "변호인", "reason": "원칙을 지키는 인물의 드라마로 공감이 갑니다."}
        ]
    },
    "ISFJ": {
        "books": [
            {"title": "아홉 살 인생", "author": "류시화", "reason": "따뜻하고 작은 삶의 이야기들이 위로가 돼요."},
            {"title": "완득이", "author": "김려령", "reason": "사람을 돌보는 마음이 잘 드러나는 이야기라 친근해요."}
        ],
        "movies": [
            {"title": "7번방의 선물", "reason": "착한 마음과 가족애가 잔잔히 다가와요."},
            {"title": "스윙키즈", "reason": "동료애와 헌신을 느낄 수 있어요."}
        ]
    },
    "ISTP": {
        "books": [
            {"title": "살인자의 기억법", "author": "김영하", "reason": "수수께끼 같은 전개와 현실적인 묘사가 ISTP의 분석력을 자극해요."},
            {"title": "82년생 김지영", "author": "조남주", "reason": "사회 현상을 직시하는 시선이 실용적으로 다가올 수 있어요."}
        ],
        "movies": [
            {"title": "범죄도시", "reason": "직관적이고 액션 중심의 전개가 통쾌해요."},
            {"title": "아저씨", "reason": "직설적이고 손에 땀을 쥐는 액션이 매력적입니다."}
        ]
    },
    "ISFP": {
        "books": [
            {"title": "채식주의자", "author": "한강", "reason": "이미지와 감정에 집중하는 문장이 감성적인 ISFP에게 잘 맞아요."},
            {"title": "너의 췌장을 먹고 싶어", "author": "스미노 요루 (번역서)", "reason": "짧지만 깊은 감정선이 마음에 남아요."}
        ],
        "movies": [
            {"title": "봄날은 간다", "reason": "감정의 여백과 분위기를 즐기는 영화로 좋습니다."},
            {"title": "건축학개론", "reason": "잔잔한 감성으로 오래 기억에 남아요."}
        ]
    },
    "ESTJ": {
        "books": [
            {"title": "태백산맥", "author": "조정래", "reason": "구조와 역사를 따라가는 서사가 체계적이라 ESTJ에게 흥미롭습니다."},
            {"title": "완득이", "author": "김려령", "reason": "현실적이고 성취 중심의 이야기가 힘이 돼요."}
        ],
        "movies": [
            {"title": "강철비", "reason": "리더십과 위기 대응이 큰 비중을 차지해 몰입됩니다."},
            {"title": "택시운전사", "reason": "책임감 있고 행동하는 주인공의 모습이 인상적이에요."}
        ]
    },
    "ESTP": {
        "books": [
            {"title": "광장", "author": "최인훈", "reason": "강렬한 상황과 선택이 많은 이야기라 흥미롭게 읽을 수 있어요."},
            {"title": "살인자의 기억법", "author": "김영하", "reason": "빠른 전개와 긴장감으로 몰입도가 높습니다."}
        ],
        "movies": [
            {"title": "범죄도시", "reason": "속도감 있는 액션과 직설적 재미가 짜릿해요."},
            {"title": "암살", "reason": "스릴과 모험이 결합된 구성으로 흥분을 줍니다."}
        ]
    },
    "ESFP": {
        "books": [
            {"title": "우리들의 일그러진 영웅", "author": "이문열", "reason": "인간 관계와 드라마가 뚜렷해 몰입감 있게 읽어요."},
            {"title": "완득이", "author": "김려령", "reason": "유머와 온기가 있어 즐겁게 빠져들 수 있어요."}
        ],
        "movies": [
            {"title": "극한직업", "reason": "유머와 액션이 잘 섞여 즐겁게 웃을 수 있어요."},
            {"title": "7번방의 선물", "reason": "웃음과 눈물이 적절히 섞인 작품이라 감정 기복이 즐거워요."}
        ]
    },
    "ENFP_alt": {},  # placeholder if needed
    "ESFJ": {
        "books": [
            {"title": "아홉 살 인생", "author": "류시화", "reason": "따뜻하고 사람을 돌보는 메시지가 많아 친화적이에요."},
            {"title": "완득이", "author": "김려령", "reason": "연대감과 배려에 대한 이야기가 마음에 와 닿습니다."}
        ],
        "movies": [
            {"title": "국제시장", "reason": "가족과 전통, 서로 돕는 이야기를 좋아하신다면 추천해요."},
            {"title": "7번방의 선물", "reason": "따뜻한 감정선이 가득해 함께 보기 좋아요."}
        ]
    }
}

# Note: ENSURE all 16 MBTIs are present - some keys above may be different names.
# To keep a clean order and include all 16, make a definitive list and fallback.
ALL_MBTI = [
    "INTJ","INTP","INFJ","INFP","ENTJ","ENTP","ENFJ","ENFP",
    "ISTJ","ISFJ","ISTP","ISFP","ESTJ","ESTP","ESFP","ESFJ"
]

# For MBTIs missing from MBTI_DATA (like "ENFP"), provide reasonable defaults:
DEFAULT_REC = {
    "books": [
        {"title": "아몬드", "author": "손원평", "reason": "감정과 정체성을 섬세히 다루는 이야기로 누구에게나 공감돼요."},
        {"title": "완득이", "author": "김려령", "reason": "따뜻하고 에너지 넘치는 성장담이라 가볍게 읽기 좋아요."}
    ],
    "movies": [
        {"title": "기생충", "reason": "사회적 맥락과 인간관계를 날카롭게 보여줘 생각할 거리가 많아요."},
        {"title": "건축학개론", "reason": "감성적이고 추억을 건드리는 영화라 편하게 추천합니다."}
    ]
}

# Fill missing entries with defaults
for mbti in ALL_MBTI:
    if mbti not in MBTI_DATA:
        MBTI_DATA[mbti] = DEFAULT_REC

st.title("MBTI로 골라보는 한국 책 · 영화 추천 🎒📖🎬")
st.write("원하는 MBTI를 골라봐 — 너랑 잘 맞을 만한 한국 책 2권과 영화 2편을 센스 있게 알려줄게요. 🙂\n\n")

with st.sidebar:
    st.header("설정")
    chosen = st.selectbox("MBTI를 선택하세요", ALL_MBTI, index=0)
    st.write("Tip: 친구 MBTI로도 골라보면 재밌어요! 🤝")

rec = MBTI_DATA.get(chosen, DEFAULT_REC)

st.subheader(f"추천 — {chosen}님을 위한 찐 리스트 ✨")
st.markdown("**도서 (한국 작가 위주)**")
for b in rec["books"]:
    st.markdown(f"- **{b['title']}** _({b.get('author','저자 미상')})_ — {b['reason']}")

st.markdown("**영화**")
for m in rec["movies"]:
    st.markdown(f"- **{m['title']}** — {m['reason']}")

st.divider()
st.caption("추천은 기분 따라 달라질 수 있어요! 필요하면 성향(예: ‘감성형’, ‘분석형’)을 알려주면 더 맞춤 추천도 해줄게 😀")

# Optional: small footer with usage note
st.write("")
st.write("— 만든이: MBTI 추천봇 (간단 버전) | 추가 요청은 언제든지 말해줘! ✍️")
