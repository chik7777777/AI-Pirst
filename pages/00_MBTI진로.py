import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="🔮", layout="centered")

st.title("MBTI로 알아보는 맞춤 진로 추천 🔍")
st.write("16가지 MBTI 중 하나를 골라봐 — 각 유형에 어울리는 진로 2개와 적합한 학과/성격을 알려줄게. 청소년도 보기 편하게 쉽게 썼어! 😄")

MBTIS = [
    'ISTJ','ISFJ','INFJ','INTJ',
    'ISTP','ISFP','INFP','INTP',
    'ESTP','ESFP','ENFP','ENTP',
    'ESTJ','ESFJ','ENFJ','ENTJ'
]

# 각 MBTI에 대해 진로 2개를 추천하고, 적합한 학과와 성격을 간단히 설명
CAREER_DB = {
    'ISTJ': [
        {'job':'회계사 / 세무사', 'majors':['회계학', '경영학'], 'personality':'세부사항을 잘 챙기고 규칙을 따르는 성향', 'emoji':'📊'},
        {'job':'토목/건축기사', 'majors':['건축공학', '토목공학'], 'personality':'실무적, 계획적이며 책임감 있는 성향', 'emoji':'🏗️'}
    ],
    'ISFJ': [
        {'job':'간호사', 'majors':['간호학'], 'personality':'섬세하고 남을 돌보는 걸 좋아하는 성향', 'emoji':'💉'},
        {'job':'사회복지사', 'majors':['사회복지학'], 'personality':'공감능력이 높고 안정감을 주는 성향', 'emoji':'🤝'}
    ],
    'INFJ': [
        {'job':'심리상담사/임상심리사', 'majors':['심리학'], 'personality':'사람의 내면을 이해하려는 통찰력 있는 성향', 'emoji':'🧠'},
        {'job':'작가 / 콘텐츠 기획자', 'majors':['국어국문학', '문예창작', '커뮤니케이션'], 'personality':'창의적이고 가치 지향적인 성향', 'emoji':'✍️'}
    ],
    'INTJ': [
        {'job':'데이터 사이언티스트', 'majors':['통계학', '컴퓨터공학', '수학'], 'personality':'전략적이고 분석적인 문제 해결자', 'emoji':'📈'},
        {'job':'건축가 / 전략기획', 'majors':['건축학', '경영학'], 'personality':'장기적 설계와 구조를 좋아하는 성향', 'emoji':'🧭'}
    ],
    'ISTP': [
        {'job':'기계/자동차 정비사', 'majors':['기계공학', '자동차공학'], 'personality':'손으로 만지고 고치는 실용적 성향', 'emoji':'🔧'},
        {'job':'파일럿 / 항공정비', 'majors':['항공운항과', '항공우주공학'], 'personality':'위기 대처가 빠르고 현실적인 성향', 'emoji':'✈️'}
    ],
    'ISFP': [
        {'job':'디자이너(그래픽/패션)', 'majors':['디자인학', '시각디자인'], 'personality':'감수성이 풍부하고 미적 감각이 있는 성향', 'emoji':'🎨'},
        {'job':'예술치료사', 'majors':['미술치료', '교육학', '심리학'], 'personality':'사람과 창작으로 치유하는 걸 좋아함', 'emoji':'🖌️'}
    ],
    'INFP': [
        {'job':'상담사 / 인문학 연구자', 'majors':['심리학', '철학', '문학'], 'personality':'이상과 가치를 중시하고 공감 능력이 높은 성향', 'emoji':'🌱'},
        {'job':'콘텐츠 크리에이터(창작)', 'majors':['미디어학', '문예창작'], 'personality':'자기표현을 즐기는 창의적 성향', 'emoji':'🎬'}
    ],
    'INTP': [
        {'job':'연구원 / 학자', 'majors':['물리학', '수학', '컴퓨터공학'], 'personality':'이론을 탐구하고 논리적으로 사고하는 성향', 'emoji':'🔬'},
        {'job':'소프트웨어 개발자', 'majors':['컴퓨터공학', '소프트웨어'], 'personality':'문제를 분석하고 시스템을 만드는 걸 즐김', 'emoji':'💻'}
    ],
    'ESTP': [
        {'job':'세일즈/영업', 'majors':['경영학', '마케팅'], 'personality':'행동력이 빠르고 결과 지향적인 성향', 'emoji':'💼'},
        {'job':'기업가(스타트업)', 'majors':['경영학', '창업학'], 'personality':'모험심이 있고 실전에서 배우는 걸 좋아함', 'emoji':'🚀'}
    ],
    'ESFP': [
        {'job':'연예/공연(퍼포머)', 'majors':['무용학', '연기', '음악'], 'personality':'사람들과 어울리며 에너지를 얻는 성향', 'emoji':'🎤'},
        {'job':'이벤트 플래너/서비스업', 'majors':['관광학', '호텔경영'], 'personality':'순발력 있고 고객 지향적인 성향', 'emoji':'🎉'}
    ],
    'ENFP': [
        {'job':'마케팅/브랜딩 전문가', 'majors':['광고홍보학', '경영학'], 'personality':'아이디어가 많고 사람을 설득하는 걸 좋아함', 'emoji':'✨'},
        {'job':'저널리스트/방송작가', 'majors':['신문방송', '커뮤니케이션'], 'personality':'호기심 많고 스토리텔링을 즐기는 성향', 'emoji':'📝'}
    ],
    'ENTP': [
        {'job':'변호사 / 정책입안자', 'majors':['법학', '정치외교학'], 'personality':'토론을 즐기고 창의적으로 논리 세우는 성향', 'emoji':'⚖️'},
        {'job':'스타트업 창업자 / 혁신가', 'majors':['경영학', '컴퓨터공학'], 'personality':'새로운 아이디어를 실험하는 걸 좋아함', 'emoji':'💡'}
    ],
    'ESTJ': [
        {'job':'경영 관리자(운영)', 'majors':['경영학', '인사조직'], 'personality':'구조화, 계획 실행에 강한 성향', 'emoji':'📋'},
        {'job':'공무원/행정', 'majors':['행정학', '법학'], 'personality':'책임감 있고 규칙을 중시하는 성향', 'emoji':'🏛️'}
    ],
    'ESFJ': [
        {'job':'교사 / 교육행정', 'majors':['교육학', '아동학'], 'personality':'남을 챙기고 분위기를 잘 만드는 성향', 'emoji':'🏫'},
        {'job':'HR / 인사담당', 'majors':['경영학', '심리학'], 'personality':'사람 관리와 조율을 잘하는 성향', 'emoji':'🤝'}
    ],
    'ENFJ': [
        {'job':'상담교사 / 교육자', 'majors':['교육학', '심리학'], 'personality':'타인을 이끌고 도와주는 리더십', 'emoji':'🌟'},
        {'job':'PR/홍보 전문가', 'majors':['광고홍보', '커뮤니케이션'], 'personality':'사람과의 소통을 즐기며 영향력 발휘', 'emoji':'📣'}
    ],
    'ENTJ': [
        {'job':'경영 컨설턴트 / CEO', 'majors':['경영학', '경제학'], 'personality':'목표지향적이고 전략을 세우는 리더', 'emoji':'🏆'},
        {'job':'프로젝트 매니저', 'majors':['산업공학', '경영학'], 'personality':'빠른 의사결정과 추진력을 가진 성향', 'emoji':'🛠️'}
    ],
}

st.markdown("---")
chosen = st.selectbox("당신의 MBTI를 골라봐요", MBTIS)

if chosen:
    st.header(f"{chosen}에게 어울리는 진로 ✨")
    options = CAREER_DB.get(chosen, [])

    for i, opt in enumerate(options, 1):
        st.subheader(f"{i}. {opt['job']} {opt['emoji']}")
        st.write(f"**추천 학과:** {', '.join(opt['majors'])}")
        st.write(f"**어울리는 성격:** {opt['personality']}")
        st.write("\n")

    st.info("팁: 관심 있는 진로가 있다면 관련 동아리, 체험활동, 온라인 강의 등을 먼저 시도해보는 걸 추천해요. 경험이 답이 될 때가 많거든요! 😄")

st.markdown("---")
st.caption("앱 제작: 간단한 진로 가이드는 참고용이에요. 더 깊은 진로 상담이 필요하면 학교 진로상담실이나 전문 상담사와 상담해보세요.")

