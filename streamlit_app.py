import streamlit as st

# 페이지 설정
st.set_page_config(page_title="자기소개", layout="centered")

# 프로필 영역
st.title("👋 신범수 (Shin Beomsu)")
st.markdown("---")

# 소개
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📌 기본 정보")
    st.write("**직책**: 개발자")
    st.write("**관심사**: 웹 개발, 데이터 분석")
    st.write("**위치**: 한국")

with col2:
    st.markdown("### 🎯 소개")
    st.write(
        """
        안녕하세요! 저는 신범수입니다.
        Streamlit을 이용한 웹 애플리케이션 개발을 하고 있습니다.
        새로운 기술을 배우고 창의적인 솔루션을 만드는 것을 좋아합니다.
        """
    )

st.markdown("---")

# 경험 및 기술
st.header("💼 경험 및 기술")

with st.expander("사용 기술", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**프로그래밍 언어**")
        st.write("- Python")
        st.write("- JavaScript")
        st.write("- HTML/CSS")
    
    with col2:
        st.markdown("**프레임워크 & 라이브러리**")
        st.write("- Streamlit")
        st.write("- Pandas")
        st.write("- NumPy")

st.markdown("---")

# 연락처
st.header("📞 연락처")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📧 이메일"):
        st.info("example@example.com")

with col2:
    if st.button("🐙 GitHub"):
        st.info("https://github.com/ShinBeomsu")

with col3:
    if st.button("💼 LinkedIn"):
        st.info("https://linkedin.com")

st.markdown("---")

# 사이드바
st.sidebar.markdown("## 📋 메뉴")
page = st.sidebar.radio("이동하기:", ["홈", "프로젝트", "블로그"])

if page == "홈":
    st.sidebar.write("현재 홈페이지를 보고 있습니다.")
elif page == "프로젝트":
    st.sidebar.write("프로젝트 페이지로 이동하려면 업데이트가 필요합니다.")
else:
    st.sidebar.write("블로그 페이지로 이동하려면 업데이트가 필요합니다.")

st.markdown("---")
st.markdown("<div style='text-align: center'><small>© 2026 신범수. All rights reserved.</small></div>", unsafe_allow_html=True)
