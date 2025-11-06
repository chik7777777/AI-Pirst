import streamlit as st

# MBTI 책/영화 추천 앱 (Streamlit Cloud에서 작동)
# 추가 라이브러리 불필요. 포스터는 플레이스홀더 URL을 사용했습니다.
# 실제 포스터를 넣으려면 recommendations 딕셔너리의 'poster' 값을 해당 이미지 URL로 바꿔주세요.

st.set_page_config(page_title="MBTI 북·무비 추천", page_icon=":books:", layout="centered")

st.title("MBTI로 고르는 한국 책 + 영화 추천")
st.caption("MBTI를 골라주면 청소년에게 친근한 말투로 책 2권과 영화 2편을 센스있게 추천해줘요. ✨")

MBTIS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

selected = st.selectbox("당신의 MBTI를 골라줘", MBTIS)

# 추천 데이터 (책: 한국 작품 기준, 영화: 한국 영화 중심)
# 필요하면 poster 값을 실제 이미지 URL로 바꿔주세요.
placeholder = "https://via.placeholder.com/300x450?text=Poster"

recommendations = {
    "ISTJ": {
        "books":[
            {"title":"82년생 김지영","author":"조남주","reason":"현실적이고 책임감 강한 ISTJ에게 사회와 개인의 의무를 차분히 바라보게 해주는 작품이에요.", "poster": placeholder},
            {"title":"아몬드","author":"손원평","reason":"논리적이고 규칙을 좋아하는 성향에게 감정과 공감에 대해 생각할 거리를 줘요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"기생충","director":"봉준호","reason":"세밀한 관찰력으로 사회 구조를 파악하는 ISTJ에게 메시지와 구성 모두 흥미로울 거예요.", "poster": placeholder},
            {"title":"택시운전사","director":"장훈","reason":"사실에 기반한 묵직한 이야기로 책임감 있는 성향과 잘 맞아요.", "poster": placeholder}
        ]
    },
    "ISFJ": {
        "books":[
            {"title":"우리들의 일그러진 영웅","author":"이문열","reason":"타인을 돌보는 성향에게 인간관계와 사회의 규칙을 생각하게 해줘요.", "poster": placeholder},
            {"title":"완득이","author":"김려령","reason":"따뜻한 시선과 성장 이야기로 공감 능력이 큰 ISFJ에게 추천해요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"국제시장","director":"윤제균","reason":"가족과 헌신을 중요하게 여기는 분들에게 울림이 큰 영화예요.", "poster": placeholder},
            {"title":"소원","director":"이준익","reason":"치유와 회복을 다루는 이야기로 감정 이입이 잘 되는 ISFJ에게 좋아요.", "poster": placeholder}
        ]
    },
    "INFJ": {
        "books":[
            {"title":"채식주의자","author":"한강","reason":"내면의 깊은 서사를 섬세하게 파고드는 작품이라 통찰력 있는 INFJ에게 어울려요.", "poster": placeholder},
            {"title":"소년이 온다","author":"한강","reason":"강렬한 윤리적 질문과 감정의 여운이 오래가는 책이에요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"버닝","director":"이창동","reason":"미스터리한 분위기와 상징을 해석하는 걸 좋아하는 INFJ에게 추천해요.", "poster": placeholder},
            {"title":"마더","director":"봉준호","reason":"모성과 윤리, 인간 심리를 깊게 다루는 작품입니다.", "poster": placeholder}
        ]
    },
    "INTJ": {
        "books":[
            {"title":"미생","author":"윤태호","reason":"전략적 사고와 계획을 좋아하는 INTJ에게 직장과 인간관계를 분석하게 해줘요.", "poster": placeholder},
            {"title":"우리가 빛의 속도로 갈 수 없다면","author":"김초엽","reason":"과학적 상상력과 사유를 자극하는 단편집이에요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"추격자","director":"나홍진","reason":"복잡한 플롯과 심리 묘사를 좋아하는 분에게 강렬한 몰입감을 줍니다.", "poster": placeholder},
            {"title":"올드보이","director":"박찬욱","reason":"구조적 복선과 반전이 많은 영화라 분석적 성향에 맞아요.", "poster": placeholder}
        ]
    },
    "ISTP": {
        "books":[
            {"title":"칼의 노래","author":"김훈","reason":"간결한 문체와 행동 중심의 서사가 행동파 ISTP에게 잘 맞아요.", "poster": placeholder},
            {"title":"해독의 시간","author":"황정은","reason":"짧지만 날카로운 관찰이 많은 작품으로 실용적 감각을 자극해요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"범죄와의 전쟁: 나쁜놈들 전성시대","director":"윤종빈","reason":"액션과 현실 묘사가 균형 있어 행동 중심 성향에 어울려요.", "poster": placeholder},
            {"title":"악의 연대기","director":"김태균","reason":"긴장감 있고 즉각적인 반응을 즐기는 ISTP에게 추천합니다.", "poster": placeholder}
        ]
    },
    "ISFP": {
        "books":[
            {"title":"그녀의 별이 사라졌다","author":"황정은","reason":"감성적 표현과 소소한 순간을 좋아하는 ISFP에게 어울리는 작품이에요.", "poster": placeholder},
            {"title":"나는 나를 파괴할 권리가 있다","author":"김영하","reason":"개성 있고 감각적인 문장으로 감성적인 독자에게 추천합니다.", "poster": placeholder}
        ],
        "movies":[
            {"title":"클래식","director":"곽재용","reason":"서정적이고 감성적인 멜로를 좋아하는 분에게 따뜻해요.", "poster": placeholder},
            {"title":"건축학개론","director":"윤제균","reason":"첫사랑의 설렘과 감정을 섬세히 다루는 영화예요.", "poster": placeholder}
        ]
    },
    "INFP": {
        "books":[
            {"title":"채식주의자","author":"한강","reason":"상징과 내면의 세계를 탐구하는 INFP에게 깊은 울림을 줘요.", "poster": placeholder},
            {"title":"종의 기원","author":"김영하","reason":"정체성과 개인의 서사를 성찰하게 만드는 작품입니다.", "poster": placeholder}
        ],
        "movies":[
            {"title":"시","director":"이창동","reason":"시적인 서사와 감정선이 풍부해 감성적 성향과 잘 맞아요.", "poster": placeholder},
            {"title":"봄날은 간다","director":"허진호","reason":"잔잔하고 여운 있는 멜로로 마음에 오래 남습니다.", "poster": placeholder}
        ]
    },
    "INTP": {
        "books":[
            {"title":"미생","author":"윤태호","reason":"시스템과 규칙을 분석하는 재미가 있어요.", "poster": placeholder},
            {"title":"멋진 신세계 (번역)","author":"올더스 헉슬리 (번역: 황윤조 등)","reason":"사상적 실험을 즐기는 INTP에게 흥미로운 상상력을 제공합니다.", "poster": placeholder}
        ],
        "movies":[
            {"title":"살인의 추억","director":"봉준호","reason":"미스테리와 논리적 추리가 결합된 작품이라 분석적 성향에 잘 맞아요.", "poster": placeholder},
            {"title":"스파이","director":"윤종빈","reason":"계획과 반전이 있는 긴장감 넘치는 영화예요.", "poster": placeholder}
        ]
    },
    "ESTP": {
        "books":[
            {"title":"죽음에 관하여","author":"공지영","reason":"강렬한 경험과 현실적 이야기를 선호하는 ESTP에게 추천해요.", "poster": placeholder},
            {"title":"아웃랜더 (한국 번역본)","author":"대니얼 스티븐슨","reason":"액션과 속도감 있는 전개가 매력적입니다.", "poster": placeholder}
        ],
        "movies":[
            {"title":"신세계","director":"박훈정","reason":"빠른 전개와 액션, 긴장감이 ESTP에게 딱이에요.", "poster": placeholder},
            {"title":"베테랑","director":"류승완","reason":"에너지 넘치고 속도감 있는 연출이 즐거움을 줍니다.", "poster": placeholder}
        ]
    },
    "ESFP": {
        "books":[
            {"title":"그렇게 아버지가 된다","author":"히가시노 게이고 (한국 번역)","reason":"감정과 드라마를 좋아하는 ESFP에게 공감되는 주제예요.", "poster": placeholder},
            {"title":"연애의 기억","author":"정세랑","reason":"사람 냄새 나는 이야기와 유머가 돋보여요.", "poster": placeholder}
        ],
        "movies":[
            {"title":"극한직업","director":"이병헌","reason":"유머와 활력이 넘치고 함께 보면 즐거운 영화입니다.", "poster": placeholder},
            {"title":"타짜","director":"최동훈","reason":"화려한 연출과 캐릭터가 ESFP의 취향과 잘 맞아요.", "poster": placeholder}
        ]
    },
    "ENFP": {
        "books":[
            {"title":"오직 두 사람","author":"강지영","reason":"상상력과 인간 관계의 섬세한 묘사가 ENFP의 호기심을 자극해요.", "poster": placeholder},
            {"title":"알려지지 않은 밤과 하루","author":"공지영","reason":"다양한 감정과 이야기의 결합이 매력적입니다.", "poster": placeholder}
        ],
        "movies":[
            {"title":"극장에서 만난 사람들","director":"김종관","reason":"감성적이고 자유로운 분위기를 좋아하는 ENFP에게 좋아요.", "poster": placeholder},
            {"title":"비밀은 없다","director":"이창동","reason":"사건과 인간 드라마가 결합되어 생각할 거리를 줍니다.", "poster": placeholder}
        ]
    },
    "ENTP": {
        "books":[
            {"title":"혼자 공부하는 사람들","author":"이외수","reason":"도발적이고 아이디어가 많은 내용을 즐기는 ENTP에게 어울려요.", "poster": placeholder},
            {"title":"총, 균, 쇠 (번역)","author":"재레드 다이아몬드","reason":"넓은 관점과 논쟁적 주제를 좋아하는 분에게 추천합니다.", "poster": placeholder}
        ],
        "movies":[
            {"title"
