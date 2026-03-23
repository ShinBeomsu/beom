import streamlit as st

st.set_page_config(
    page_title="고등학교 수학교육과정 소개",
    page_icon="📚",
    layout="wide"
)

st.title("📚 고등학교 수학교육과정 소개서")
st.markdown("---")

# 서론
st.header("📖 서론")
st.write("고등학교 수학교육과정은 학생들의 논리적 사고력, 문제 해결 능력, 그리고 수학적 개념 이해를 기르는 데 중추적인 역할을 합니다.")
st.write("수학은 단순한 계산 기술을 넘어 과학, 공학, 경제 등 다양한 분야의 기초가 되는 학문으로, 고등학교 시기 동안 체계적인 교육을 통해")
st.write("학생들이 수학의 본질을 이해하고 실생활에 적용할 수 있는 능력을 키우는 것이 중요합니다.")
st.write("")
st.write("본 소개서는 2015 개정 교육과정을 기준으로 한국 고등학교 수학교육과정의 구성, 특징, 그리고 교육 목표에 대해 설명하고자 합니다.")

# 교육과정 구성
st.header("🏗️ 고등학교 수학교육과정의 구성")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 교육과정의 기본 구조")
    st.write("고등학교 수학교육과정은 공통과정과 선택과정으로 크게 나뉩니다.")
    st.write("이는 학생들의 진로 선택과 학습 능력에 따라 유연하게 수학 교육을 받을 수 있도록 설계되었습니다.")

    st.markdown("**공통과정 (필수 이수)**")
    st.markdown("- **수학Ⅰ**: 함수, 방정식, 부등식, 도형의 방정식 등 기초 개념 학습")
    st.markdown("- **수학Ⅱ**: 삼각함수, 지수함수, 로그함수, 수열 등 고급 함수 개념")

    st.info("공통과정은 모든 고등학생이 이수해야 하며, 수학의 기초를 다지는 역할을 합니다.")

with col2:
    st.subheader("🎯 선택과정 (선택 이수)")
    st.write("학생들은 자신의 진로와 관심사에 따라 다음 과목 중에서 선택하여 이수합니다:")

    subjects = [
        "미적분: 극한, 미분, 적분 등 대학 수준의 수학 기초",
        "확률과 통계: 확률 분포, 통계적 추론, 데이터 분석",
        "기하: 평면 좌표, 공간 도형, 벡터 등 기하학적 개념",
        "수학적 사고력: 논리적 추론, 증명, 조합론 등 고급 사고력 개발"
    ]

    for subject in subjects:
        st.markdown(f"• **{subject}**")

# 교육과정의 특징
st.header("✨ 교육과정의 특징")

features = [
    {
        "title": "학생 중심의 선택 교육",
        "content": "2015 개정 교육과정의 가장 큰 특징은 학생들의 진로 선택권을 강화한 것입니다."
    },
    {
        "title": "개념 중심 교육",
        "content": "단순 암기 위주의 교육에서 벗어나 개념의 이해와 적용을 강조합니다."
    },
    {
        "title": "정보통신기술(ICT) 활용",
        "content": "컴퓨터, 스마트 기기, 소프트웨어를 활용한 수학 교육이 강화되었습니다."
    },
    {
        "title": "평가 방식의 다양화",
        "content": "다양한 평가 방법을 통해 학생들의 수학적 사고력을 종합적으로 평가합니다."
    }
]

for i, feature in enumerate(features):
    if i % 2 == 0:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(feature["title"])
            st.write(feature["content"])
    else:
        with col2:
            st.subheader(feature["title"])
            st.write(feature["content"])

# 교육 목표
st.header("🎯 교육 목표")
goals = [
    "논리적 사고력 개발: 수학적 개념을 이해하고 논리적으로 추론하는 능력",
    "문제 해결 능력 배양: 실생활 문제를 수학적으로 모델링하고 해결하는 능력",
    "수학적 소양 함양: 수학의 아름다움과 유용성을 이해하고 수학을 즐기는 태도",
    "진로 선택 지원: 다양한 선택 과목을 통해 학생들의 진로 선택을 지원"
]

for goal in goals:
    st.markdown(f"• **{goal}**")

st.write("수학교육과정에 대한 추가 질문이 있으시면 언제든지 문의해 주세요.")