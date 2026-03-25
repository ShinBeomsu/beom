import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ModuleNotFoundError:
    px = None
    go = None

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
        
        # X, Y 축 직접 선택
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X 축 컬럼 선택", ["(index)"] + df.columns.tolist(), key="x_axis")
        with col2:
            y_col = st.selectbox("Y 축 컬럼 선택", numeric_cols, key="y_axis")
        
        chart_type = st.selectbox("차트 종류", ["막대 차트", "선 차트", "면적 차트", "히스토그램", "커스텀 차트 (Plotly)"])

        # 선택된 축 정보 표시
        if x_col == "(index)":
            st.info(f"X축: 인덱스, Y축: {y_col}")
        else:
            st.info(f"X축: {x_col}, Y축: {y_col}")

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

        elif chart_type == "커스텀 차트 (Plotly)":
            st.subheader("커스텀 Plotly 차트")

            if px is None:
                st.error("Plotly가 설치되지 않았습니다. `pip install plotly` 후 다시 실행하세요.")
            else:
                # Plotly 차트 타입 선택
                plotly_chart_type = st.selectbox("Plotly 차트 타입", [
                    "산점도 (Scatter)", "선 그래프 (Line)", "막대 그래프 (Bar)", 
                    "박스 플롯 (Box)", "히스토그램 (Histogram)", "파이 차트 (Pie)"
                ])

                if plotly_chart_type == "산점도 (Scatter)":
                    if x_col != "(index)":
                        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} 산점도")
                    else:
                        fig = px.scatter(df, y=y_col, title=f"{y_col} 산점도")
                    st.plotly_chart(fig)

                elif plotly_chart_type == "선 그래프 (Line)":
                    if x_col != "(index)":
                        fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} 선 그래프")
                    else:
                        fig = px.line(df, y=y_col, title=f"{y_col} 선 그래프")
                    st.plotly_chart(fig)

                elif plotly_chart_type == "막대 그래프 (Bar)":
                    if x_col != "(index)":
                        fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} 막대 그래프")
                    else:
                        fig = px.bar(df, y=y_col, title=f"{y_col} 막대 그래프")
                    st.plotly_chart(fig)

                elif plotly_chart_type == "박스 플롯 (Box)":
                    fig = px.box(df, y=y_col, title=f"{y_col} 박스 플롯")
                    st.plotly_chart(fig)

                elif plotly_chart_type == "히스토그램 (Histogram)":
                    fig = px.histogram(df, x=y_col, title=f"{y_col} 히스토그램")
                    st.plotly_chart(fig)

                elif plotly_chart_type == "파이 차트 (Pie)":
                    if x_col != "(index)":
                        fig = px.pie(df, values=y_col, names=x_col, title=f"{x_col} 기준 {y_col} 파이 차트")
                    else:
                        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
                        if cat_cols:
                            fig = px.pie(df, values=y_col, names=cat_cols[0], title=f"{cat_cols[0]} 기준 {y_col} 파이 차트")
                        else:
                            st.warning("파이 차트를 그리려면 카테고리형 컬럼이 필요합니다.")
                            fig = None
                    if fig:
                        st.plotly_chart(fig)

                    fig = px.pie(df, values=y_col, names=x_col, title=f"{x_col} 기준 {y_col} 파이 차트")
                else:
                    # 파이 차트의 경우 카테고리형 데이터가 필요하므로 첫 번째 문자열 컬럼 사용
                    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
                    if cat_cols:
                        fig = px.pie(df, values=y_col, names=cat_cols[0], title=f"{cat_cols[0]} 기준 {y_col} 파이 차트")
                    else:
                        st.warning("파이 차트를 그리려면 카테고리형 컬럼이 필요합니다.")
                        fig = None
                if fig:
                    st.plotly_chart(fig)

    st.write("### 통계 요약")
    st.write(df.describe())

else:
    st.warning("데이터를 입력하거나 업로드해서 차트를 확인하세요.")
