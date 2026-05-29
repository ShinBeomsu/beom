import streamlit as st

st.set_page_config(
    page_title="조건부확률을 이용한 질병진단",
    page_icon="📘",
    layout="wide"
)

st.title("📘 조건부확률을 이용한 질병진단")
st.write("이 페이지는 탐구활동 전 질병 검사의 핵심개념을 쉽게 이해하기 위한 페이지입니다. 앞으로의 탐구활동은 이 용어들을 바탕으로 구성됩니다.")

st.markdown("---")

st.subheader("🎯 이번 수업에서 배우는 것")
st.write(
    "- 검사 성능을 나타내는 **민감도**, **특이도**의 뜻\n"
    "- 전체 인구에서 질병이 실제로 얼마나 많은지를 나타내는 **유병률**\n"
    "- 검사 결과를 네 가지로 나누는 **진양성, 진음성, 위양성, 위음성**\n"
    "- 이 개념들이 왜 진단 검사에서 중요한지 파악"
)

st.markdown("---")

st.subheader("🧠 핵심 용어를 쉽게 표현하자면?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 민감도 (Sensitivity)")
    st.write("**질병이 실제로 있을 때, 검사를 잘 잡아내는 능력**입니다.")
    st.write("예를 들어, 실제로 병이 있는 사람 중 양성으로 판정되는 비율을 말합니다.")
    st.caption("쉽게 말하면: '실제 환자를 놓치지 않는 능력'")

with col2:
    st.markdown("### 특이도 (Specificity)")
    st.write("**질병이 실제로 없을 때, 정상으로 올바르게 판단하는 능력**입니다.")
    st.write("건강한 사람 중 음성으로 판정되는 비율을 말합니다.")
    st.caption("쉽게 말하면: '건강한 사람을 잘못 양성으로 보지 않는 능력'")

with col3:
    st.markdown("### 유병률 (Prevalence)")
    st.write("**전체 인구 중 실제로 질병을 가진 사람의 비율**입니다.")
    st.write("유병률이 낮으면, 같은 검사 정확도라도 양성 결과가 실제 환자일 가능성이 더 낮아질 수 있습니다.")
    st.caption("쉽게 말하면: '병이 있는 사람이 전체에서 얼마나 흔한가'")

st.markdown("---")

st.subheader("✅ 검사 결과의 네 가지 경우")

st.write("검사 결과는 실제 상태와 판정 결과를 함께 보면서 네 가지로 나눌 수 있습니다.")

case_cols = st.columns(2)

with case_cols[0]:
    st.markdown("#### 1. 진양성 (True Positive)")
    st.write("실제로 병이 있고, 검사도 양성으로 맞힌 경우입니다.")
    st.write("예: 실제 환자이며 검사 결과도 양성")

with case_cols[1]:
    st.markdown("#### 2. 진음성 (True Negative)")
    st.write("실제로 병이 없고, 검사도 음성으로 맞힌 경우입니다.")
    st.write("예: 건강한 사람이며 검사 결과도 음성")

with case_cols[0]:
    st.markdown("#### 3. 위양성 (False Positive)")
    st.write("실제로는 병이 없는데, 검사에서 양성으로 나온 경우입니다.")
    st.write("예: 건강한 사람인데 오진된 경우")

with case_cols[1]:
    st.markdown("#### 4. 위음성 (False Negative)")
    st.write("실제로는 병이 있는데, 검사에서 음성으로 나온 경우입니다.")
    st.write("예: 실제 환자인데 놓친 경우")

st.markdown("---")

st.subheader("💡 왜 이 용어를 알아야 하나요?")
st.write(
    "검사의 정확도가 좋아 보여도, 유병률이 낮으면 양성 결과가 실제 환자일 가능성이 낮아질 수 있습니다.\n"
    "또한 위양성이나 위음성을 이해하면, 검사 결과를 잘못 해석하는 문제를 줄일 수 있습니다."
)

st.info("다음 단계에서는 실제 숫자와 그래프를 보면서 이 개념들이 어떻게 작동하는지 확인해봅다.")
