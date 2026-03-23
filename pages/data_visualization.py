import pandas as pd
import streamlit as st

st.title("📊 간단한 데이터 시각화 예제")
st.write("사용자가 직접 데이터를 입력하거나 CSV 파일을 업로드하여 다양한 차트를 그릴 수 있습니다.")

st.sidebar.header("데이터 입력 옵션")
input_mode = st.sidebar.selectbox("입력 방식 선택", ["샘플 데이터", "수동 입력", "CSV 업로드"])

df = None

if input_mode == "샘플 데이터":
    df = pd.DataFrame({
        "카테고리": ["A", "B", "C", "D", "E"],
        "값": [10, 23, 17, 9, 30],
        "변경율": [2.1, -1.4, 3.3, 0.5, -0.7],
    })
    st.info("샘플 데이터를 선택했습니다.")

elif input_mode == "수동 입력":
    st.subheader("콤마로 구분된 숫자 목록 입력")
    raw = st.text_area(
        "값 입력 (예: 5, 10, 9, 20)",
        value="10, 15, 12, 18, 22"
    )
    if raw.strip():
        try:
            numbers = [float(x.strip()) for x in raw.split(",") if x.strip()]
            categories = [f"항목 {i+1}" for i in range(len(numbers))]
            df = pd.DataFrame({"카테고리": categories, "값": numbers})
        except ValueError:
            st.error("숫자 형식으로 올바르게 입력해주세요.")

elif input_mode == "CSV 업로드":
    st.subheader("CSV 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("CSV 로딩 성공")
        except Exception as e:
            st.error(f"CSV를 읽는 중 오류가 발생했습니다: {e}")

if df is not None:
    st.write("### 입력된 데이터 미리보기")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(numeric_cols) == 0:
        st.warning("숫자형 컬럼이 없습니다. 차트를 그리려면 숫자형 컬럼이 필요합니다.")
    else:
        st.write("### 차트 옵션")
        chart_type = st.selectbox("차트 종류", ["막대 차트", "선 차트", "면적 차트", "히스토그램"])
        y_col = st.selectbox("Y 축 컬럼", numeric_cols)

        x_col_candidates = [c for c in df.columns if c != y_col]
        x_col = st.selectbox("X 축 컬럼 (선택, 없으면 index)", ["(index)"] + x_col_candidates)

        if chart_type == "막대 차트":
            if x_col == "(index)":
                st.bar_chart(df[y_col])
            else:
                st.bar_chart(df.set_index(x_col)[y_col])

        elif chart_type == "선 차트":
            if x_col == "(index)":
                st.line_chart(df[y_col])
            else:
                st.line_chart(df.set_index(x_col)[y_col])

        elif chart_type == "면적 차트":
            if x_col == "(index)":
                st.area_chart(df[y_col])
            else:
                st.area_chart(df.set_index(x_col)[y_col])

        elif chart_type == "히스토그램":
            st.write(df[y_col].plot(kind="hist", bins=20, alpha=0.7).figure)

    st.write("### 통계 요약")
    st.write(df.describe())

else:
    st.warning("데이터를 입력하거나 업로드해서 차트를 확인하세요.")
