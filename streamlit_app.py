import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Streamlit 요소 보여주기", layout="wide")

st.title("🎈 Streamlit UI 요소 종합 가이드")
st.markdown("---")

# 1. 텍스트 요소
st.header("📝 텍스트 요소")
col1, col2 = st.columns(2)

with col1:
    st.subheader("기본 텍스트")
    st.text("이것은 일반 텍스트입니다")
    st.markdown("이것은 **마크다운** 텍스트입니다")

with col2:
    st.subheader("코드 표시")
    st.code("print('Hello, Streamlit!')", language="python")

# 2. 입력 요소
st.header("🎛️ 입력 요소")
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("이름을 입력하세요:", "김철수")
    age = st.number_input("나이를 입력하세요:", min_value=0, max_value=120, value=25)

with col2:
    message = st.text_area("메시지를 입력하세요:", "안녕하세요!")
    email = st.text_input("이메일:", "example@email.com")

with col3:
    city = st.selectbox("도시 선택:", ["서울", "부산", "대전", "대구"])
    hobbies = st.multiselect("취미 선택:", ["독서", "영화", "음악", "스포츠", "요리"])

# 3. 상호작용 요소
st.header("🔘 상호작용 요소")
col1, col2 = st.columns(2)

with col1:
    agree = st.checkbox("약관에 동의합니다")
    if agree:
        st.success("동의해주셨습니다!")

    option = st.radio("선택해주세요:", ["옵션1", "옵션2", "옵션3"])
    st.info(f"선택한 옵션: {option}")

with col2:
    rating = st.slider("만족도 평가 (1-5):", 1, 5, 3)
    temperature = st.slider("온도 설정:", -10.0, 50.0, 20.0)
    
if st.button("클릭하세요!", key="main_button"):
    st.balloons()
    st.success("버튼이 클릭되었습니다!")

# 4. 데이터 표시
st.header("📊 데이터 표시")

# 샘플 데이터 생성
df = pd.DataFrame({
    "이름": ["김철수", "이영희", "박민준", "최지은"],
    "나이": [25, 28, 22, 30],
    "직급": ["인턴", "사원", "대리", "과장"],
    "급여": [3000, 3500, 4000, 4500]
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("테이블")
    st.table(df)

with col2:
    st.subheader("데이터프레임 (정렬 및 필터링 가능)")
    st.dataframe(df, use_container_width=True)

# 메트릭
st.subheader("메트릭")
col1, col2, col3, col4 = st.columns(4)
col1.metric("매출액", "1,000만원", "+12%")
col2.metric("사용자 수", 250, "-2")
col3.metric("평균 평점", "4.8/5", "+0.1")
col4.metric("시스템 가동률", "99.9%", "-0.1%")

# 5. 이미지 및 미디어
st.header("🖼️ 이미지 및 미디어")

col1, col2 = st.columns(2)

with col1:
    st.subheader("샘플 이미지 생성")
    # 간단한 numpy 이미지 생성
    image = np.random.rand(200, 200, 3)
    st.image(image, caption="무작위 이미지")

with col2:
    st.subheader("오디오/비디오 플레이어")
    st.info("오디오 또는 비디오 파일 URL을 제공하여 재생할 수 있습니다.")

# 6. 확장형 요소
st.header("📦 확장형 요소")

with st.expander("자세히 보기"):
    st.write("여기에 숨겨진 내용이 있습니다!")
    st.write(df)

# Tabs 요소
tab1, tab2, tab3 = st.tabs(["탭1", "탭2", "탭3"])

with tab1:
    st.write("이것은 탭1의 내용입니다")
    st.success("성공 메시지")

with tab2:
    st.write("이것은 탭2의 내용입니다")
    st.warning("경고 메시지")

with tab3:
    st.write("이것은 탭3의 내용입니다")
    st.error("에러 메시지")

# 7. 상태 메시지
st.header("💬 상태 메시지")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("성공!")
    st.info("정보입니다")

with col2:
    st.warning("경고입니다")
    st.error("오류가 발생했습니다")

with col3:
    st.question("질문이 있습니다")

# 8. 진행 표시
st.header("⏳ 진행 상황")

progress_bar = st.progress(0)
status_text = st.empty()

for i in range(101):
    progress_bar.progress(i)
    status_text.text(f"진행률: {i}%")

# 9. 차트 (간단한 예시)
st.header("📈 차트")

col1, col2 = st.columns(2)

with col1:
    st.subheader("라인 차트")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(chart_data)

with col2:
    st.subheader("바 차트")
    bar_data = pd.DataFrame({
        "카테고리": ["A", "B", "C", "D"],
        "값": [100, 150, 120, 180]
    })
    st.bar_chart(bar_data.set_index("카테고리"))

# 10. 컬럼과 컨테이너
st.header("📐 레이아웃")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("좁은 컬럼")

with col2:
    st.write("넓은 컬럼 (2배)")

with col3:
    st.write("좁은 컬럼")

# 11. 사이드바
st.sidebar.header("⚙️ 설정")
sidebar_option = st.sidebar.radio("메뉴:", ["메인", "설정", "정보"])

if sidebar_option == "메인":
    st.sidebar.write("메인 페이지입니다")
elif sidebar_option == "설정":
    st.sidebar.write("설정 페이지입니다")
else:
    st.sidebar.write("정보 페이지입니다")

# 12. 폼
st.header("📋 폼")

with st.form(key='my_form'):
    st.write("폼 예시")
    form_name = st.text_input("이름:")
    form_email = st.text_input("이메일:")
    form_message = st.text_area("메시지:")
    submit_button = st.form_submit_button(label='제출')
    
    if submit_button:
        st.success(f"폼이 제출되었습니다! - {form_name}")

st.markdown("---")
st.markdown("### 🎉 이것이 Streamlit의 주요 UI 요소들입니다!")
