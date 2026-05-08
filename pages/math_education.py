import random
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="조건부확률과 질병진단",
    page_icon="🏥",
    layout="wide"
)

if "sensitivity" not in st.session_state:
    st.session_state.sensitivity = 0.95
if "specificity" not in st.session_state:
    st.session_state.specificity = 0.90
if "prevalence" not in st.session_state:
    st.session_state.prevalence = 0.10
if "what_if_clicked" not in st.session_state:
    st.session_state.what_if_clicked = False

st.title("👨‍⚕️ 당신은 정확한 진단을 내릴 수 있습니까?")
st.subheader("🏥 조건부확률을 이용한 질병진단")
st.write("5천만 명의 대한민국 인구 중 실제 질병에 걸린 사람이 50만 명(1%)일 때, 검사 정확도가 99%인 상황에서 양성인 사람이 실제 환자일 확률을 예측해 보세요.")

col1, col2 = st.columns([3, 1])
with col1:
    user_guess_text = st.text_input("예상 확률을 입력해 보세요 (%):", "", placeholder="숫자로만 입력하세요", key="init_guess")
with col2:
    if st.button("유병률 0.1%로 낮추기", key="what_if_prev"):
        st.session_state.sensitivity = 0.99
        st.session_state.specificity = 0.99
        st.session_state.prevalence = 0.001
        st.session_state.what_if_clicked = True

if "what_if_clicked" in st.session_state and st.session_state.what_if_clicked:
    ppv_old = 0.99 * 0.01 / (0.99 * 0.01 + 0.01 * 0.99)
    ppv_low = 0.99 * 0.001 / (0.99 * 0.001 + 0.01 * 0.999)
    st.info(f"유병률을 0.1%로 낮추면, 검사 정확도가 99%여도 PPV(양성예측도)는 약 {ppv_low:.1%}로 떨어집니다.")
    chart_df = pd.DataFrame({
        "시나리오": ["유병률 1%", "유병률 0.1%"],
        "PPV": [ppv_old, ppv_low]
    })
    fig_ppv = px.bar(
        chart_df,
        x="시나리오",
        y="PPV",
        text=chart_df["PPV"].apply(lambda x: f"{x:.1%}"),
        color="시나리오",
        color_discrete_sequence=["#636EFA", "#EF553B"]
    )
    fig_ppv.update_layout(
        title="같은 검사 정확도에서 유병률 감소 시 PPV 변화",
        yaxis_tickformat=".0%",
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        height=340
    )
    fig_ppv.update_traces(textposition="outside")
    st.plotly_chart(fig_ppv, use_container_width=True)
    st.write("유병률이 낮아질수록 실제 양성인 사람 비율(PPV)이 급격히 떨어집니다. 이것이 진단 검사 해석에서 기저율 오류가 중요한 이유입니다.")

if st.button("결과 확인하기", key="guess_submit"):
    actual_guess = 50
    if user_guess_text.strip() == "":
        st.warning("먼저 예측 확률을 입력해 주세요.")
    else:
        try:
            user_guess = float(user_guess_text)
            if user_guess < 0 or user_guess > 100:
                st.warning("0에서 100 사이의 숫자를 입력해 주세요.")
            elif user_guess > 70:
                st.error(f"대부분의 사람들이 {user_guess}%라고 생각하지만, 실제로는 약 {actual_guess}%입니다. 왜 내 생각과 다를까요? 아래 미션에서 함께 살펴봅시다.")
            elif user_guess > actual_guess:
                st.warning(f"당신의 예측은 조금 높습니다. 실제 확률은 약 {actual_guess}%입니다. 아래에서 왜 이런 차이가 나는지 확인해보세요.")
            else:
                st.success(f"통계적 직관이 훌륭합니다! 실제 확률은 약 {actual_guess}%입니다. 아래에서 근거를 함께 분석해봅시다.")
        except ValueError:
            st.error("숫자를 올바르게 입력해 주세요.")

st.markdown("---")

# 개념 설명
st.header("📚 조건부확률이란?")
col1, col2 = st.columns(2)

with col1:
    st.subheader("조건부확률의 정의")
    st.write("""
    **조건부확률** P(A|B)는 사건 B가 일어났을 때, 사건 A가 일어날 확률입니다.
    
    수식: P(A|B) = P(A∩B) / P(B)
    """)
    
with col2:
    st.subheader("베이즈 정리")
    st.write("""
    **베이즈 정리**는 조건부확률을 역으로 계산하는 공식입니다.
    
    P(A|B) = P(B|A) × P(A) / P(B)
    """)

st.info("💡 질병진단에서 우리가 알고 싶은 것은 '검사가 양성일 때, 실제로 질병이 있을 확률'입니다. 이것이 바로 조건부확률입니다!")

# 사이드바: 파라미터 설정
with st.sidebar:
    st.header("🔧 파라미터 설정")
    st.write("아래 슬라이더를 조정하면 오른쪽이 즉시 업데이트됩니다!")
    st.markdown("### 🎯 오늘의 미션")
    st.info("위양성(가짜 환자)의 수를 10명 미만으로 줄여보세요!")
    
    sensitivity = st.slider(
        "민감도 (Sensitivity)",
        0.0, 1.0, st.session_state.sensitivity,
        0.01,
        key="sensitivity",
        help="질병이 있을 때 검사가 양성으로 나올 확률"
    )
    st.caption("질병 있음 → 양성 검사")
    
    specificity = st.slider(
        "특이도 (Specificity)",
        0.0, 1.0, st.session_state.specificity,
        0.01,
        key="specificity",
        help="질병이 없을 때 검사가 음성으로 나올 확률"
    )
    st.caption("질병 없음 → 음성 검사")
    
    prevalence = st.slider(
        "유병률 (Prevalence)",
        0.0, 1.0, st.session_state.prevalence,
        0.001,
        key="prevalence",
        help="전체 인구에서 질병을 가진 사람의 비율"
    )
    st.caption("실제 질병 보유율 (0.1% 단위까지 조정 가능)")
    
    st.info("💡 설정값을 바꾸면 오른쪽 화면의 모든 결과가 실시간으로 업데이트됩니다!")

if "journal" not in st.session_state:
    st.session_state.journal = []

if "journal_note" not in st.session_state:
    st.session_state.journal_note = ""

# 계산
total_people = 10000

# 실제 질병 보유자
disease_positive = int(total_people * prevalence)
disease_negative = total_people - disease_positive

# 검사 결과
true_positive = int(disease_positive * sensitivity)
false_negative = disease_positive - true_positive

false_positive = int(disease_negative * (1 - specificity))
true_negative = disease_negative - false_positive

# 양성 예측도 (PPV): 검사가 양성일 때 실제 질병이 있을 확률
test_positive = true_positive + false_positive
if test_positive > 0:
    ppv = true_positive / test_positive
else:
    ppv = 0

# 음성 예측도 (NPV): 검사가 음성일 때 실제로 질병이 없을 확률
test_negative = true_negative + false_negative
if test_negative > 0:
    npv = true_negative / test_negative
else:
    npv = 0

# Waffle Chart 데이터 계산
waffle_total = 1000
w_tp = int(ppv * (test_positive / total_people) * waffle_total)
w_fp = int((test_positive / total_people) * waffle_total) - w_tp
w_fn = int((1 - npv) * (test_negative / total_people) * waffle_total)
w_tn = waffle_total - (w_tp + w_fp + w_fn)

# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3 = st.tabs(["📊 시뮬레이션", "🧮 수학적 원리", "✏️ 연습 문제"])

# ============================================================
# TAB 1: 시뮬레이션
# ============================================================
with tab1:
    st.header("📊 실시간 시뮬레이션")
    st.write("슬라이더를 조정하여 파라미터를 변경하면, 아래 결과가 즉시 업데이트됩니다!")

    # 핵심 지표 강조
    st.subheader("💡 진단 결과 요약")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("양성일 때 실제 환자일 확률 (PPV)", f"{ppv:.2%}")
        st.caption("검사 양성 → 실제 질병 있을 확률")
    with c2:
        st.metric("음성일 때 건강할 확률 (NPV)", f"{npv:.2%}")
        st.caption("검사 음성 → 실제 질병 없을 확률")

    st.markdown("---")

    # 시각화: 하나의 큰 차트 + 선택 버튼
    st.subheader("📈 시각화")
    chart_choice = st.radio(
        "보고 싶은 차트를 선택하세요:",
        ["Waffle Chart", "Sankey Diagram", "Venn Diagram"],
        horizontal=True,
        key="chart_choice"
    )

    data_list = (
        [3] * w_tp +
        [2] * w_fp +
        [1] * w_fn +
        [0] * w_tn
    )

    rows = 20
    cols = 50
    z_matrix = np.array(data_list).reshape(rows, cols)

    colorscale = [
        [0, '#2ecc71'],
        [0.33, '#3498db'],
        [0.66, '#f39c12'],
        [1, '#e74c3c']
    ]

    fig_waffle = go.Figure(data=go.Heatmap(
        z=z_matrix,
        colorscale=colorscale,
        showscale=False,
        xgap=2,
        ygap=2,
        hoverinfo='text',
        text=np.where(z_matrix==3, "진양성 (실제 환자 & 양성 판정)",
             np.where(z_matrix==2, "위양성 (건강함 & 양성 판정)",
             np.where(z_matrix==1, "위음성 (실제 환자 & 음성 판정)", "진음성 (건강함 & 음성 판정)")))
    ))

    fig_waffle.update_layout(
        height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange='reversed'),
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            label=[f"전체\n({total_people}명)", 
                    f"질병\n({disease_positive}명)", 
                    f"건강\n({disease_negative}명)",
                    f"검사양성\n({test_positive}명)",
                    f"검사음성\n({test_negative}명)"],
            color=["#95a5a6", "#e74c3c", "#3498db", "#f39c12", "#2ecc71"],
            pad=10
        ),
        link=dict(
            source=[0, 0, 1, 1, 2, 2],
            target=[1, 2, 3, 4, 3, 4],
            value=[disease_positive, disease_negative, true_positive, false_negative, false_positive, true_negative],
            color=["rgba(231, 76, 60, 0.3)", "rgba(52, 152, 219, 0.3)", 
                   "rgba(243, 156, 18, 0.3)", "rgba(46, 204, 113, 0.3)",
                   "rgba(243, 156, 18, 0.3)", "rgba(46, 204, 113, 0.3)"]
        )
    )])

    fig_sankey.update_layout(
        title="",
        font=dict(size=10),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)'
    )

    def draw_proportional_venn(disease_pos, test_pos, true_pos, total):
        scale = 0.3
        r_disease = np.sqrt(disease_pos / total) * scale
        r_test = np.sqrt(test_pos / total) * scale

        if true_pos > 0 and disease_pos > 0 and test_pos > 0:
            ratio = true_pos / min(disease_pos, test_pos)
            ratio = np.clip(ratio, 0.01, 1.0)
            d_min = abs(r_disease - r_test)
            d_max = r_disease + r_test
            dist = d_min + (d_max - d_min) * (1 - 0.8 * ratio)
        else:
            dist = r_disease + r_test + 0.02

        fig = go.Figure()
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y",
            x0=0.08,
            y0=0.08,
            x1=0.92,
            y1=0.92,
            line=dict(color="black", width=2),
            fillcolor="rgba(200, 200, 200, 0.05)"
        )
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=0.5 - dist - r_disease,
            x1=0.5 - dist + r_disease,
            y0=0.5 - r_disease,
            y1=0.5 + r_disease,
            fillcolor="rgba(231, 76, 60, 0.4)",
            line_color="rgba(231, 76, 60, 0.8)"
        )
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=0.5 + dist - r_test,
            x1=0.5 + dist + r_test,
            y0=0.5 - r_test,
            y1=0.5 + r_test,
            fillcolor="rgba(52, 152, 219, 0.4)",
            line_color="rgba(52, 152, 219, 0.8)"
        )

        overlap_label = f"D ∩ +\n진양성 {true_pos}명"
        false_positive_label = f"위양성\n{test_pos - true_pos}명"

        fig.add_annotation(x=0.5 - dist, y=0.88, text=f"D\n질병 {disease_pos}명", showarrow=False, font=dict(size=14, color="#e74c3c"))
        fig.add_annotation(x=0.5 + dist, y=0.88, text=f"+\n검사 양성 {test_pos}명", showarrow=False, font=dict(size=14, color="#2980b9"))
        fig.add_annotation(x=0.5, y=0.55, text=overlap_label, showarrow=False, font=dict(size=14, color="#2c3e50"))
        fig.add_annotation(x=0.7, y=0.45, text=false_positive_label, showarrow=False, font=dict(size=12, color="#2980b9"))
        fig.add_annotation(x=0.5, y=0.04, text="전체 인구 S = 10,000명\n(전체 집합 안에서 질병과 검사 양성 집단의 크기를 비교하세요)", showarrow=False, font=dict(size=12), align="center")

        fig.update_xaxes(visible=False, range=[0, 1])
        fig.update_yaxes(visible=False, range=[0, 1])
        fig.update_layout(
            height=520,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(255,255,255,1)',
            plot_bgcolor='rgba(255,255,255,1)'
        )
        return fig

    fig_venn = draw_proportional_venn(disease_positive, test_positive, true_positive, total_people)

    if chart_choice == "Waffle Chart":
        st.write("**Waffle Chart: 1,000명 분포**")
        st.plotly_chart(fig_waffle, use_container_width=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("🔴 진양성")
        c2.markdown("🟠 위양성")
        c3.markdown("🔵 위음성")
        c4.markdown("🟢 진음성")
        st.write("**설명:**")
        st.write("- 🔴 진양성: 실제로 병이 있는 사람이 검사에서 양성으로 나온 경우")
        st.write("- 🟠 위양성: 실제로는 건강한데 검사에서 양성으로 나온 경우")
        st.write("- 🔵 위음성: 실제로 병이 있는데 검사에서 음성으로 나온 경우")
        st.write("- 🟢 진음성: 실제로 건강한 사람이 검사에서 음성으로 나온 경우")
    elif chart_choice == "Sankey Diagram":
        st.write("**Sankey Diagram: 인구 흐름**")
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.write("**Venn Diagram: 질병 집단 D와 양성 집단 +의 겹침(D ∩ +)**")
        st.write("왼쪽 원은 실제로 병이 있는 사람, 오른쪽 원은 검사에서 양성 판정을 받은 사람입니다.")
        st.write("겹치는 부분 D ∩ +는 검사에서 양성이면서 실제로도 병이 있는 사람, 즉 진양성입니다.")
        st.write("이 부분이 전체 양성 집단에서 얼마나 큰지 보면, 검사 결과의 신뢰도를 이해하기 쉽습니다.")
        st.plotly_chart(fig_venn, use_container_width=True)

    st.markdown("---")

    # 데이터 테이블
    st.subheader("📊 상세 데이터")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**1) 전체 인구 현황 (10,000명)**")
        prevalence_data = {
            "구분": ["질병 있음", "질병 없음", "합계"],
            "인원 수": [disease_positive, disease_negative, total_people]
        }
        st.dataframe(pd.DataFrame(prevalence_data), use_container_width=True, hide_index=True)

    with col2:
        st.write("**2) 검사의 성능**")
        performance_data = {
            "지표": ["민감도", "특이도"],
            "정의": ["질병 있을 때 양성으로 나올 확률", "질병 없을 때 음성으로 나올 확률"],
            "값": [f"{sensitivity:.0%}", f"{specificity:.0%}"]
        }
        st.dataframe(pd.DataFrame(performance_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("📋 검사 결과 분류표")
    
    classification_data = {
        "": ["질병 있음", "질병 없음", "합계"],
        "검사 양성(+)": [true_positive, false_positive, test_positive],
        "검사 음성(-)": [false_negative, true_negative, test_negative],
        "합계": [disease_positive, disease_negative, total_people]
    }
    classification_df = pd.DataFrame(classification_data).set_index("")
    st.dataframe(classification_df, use_container_width=True)

# ============================================================
# TAB 2: 수학적 원리
# ============================================================
with tab2:
    st.header("📝 베이즈 정리와 양성 예측도")
    
    st.subheader("🧮 공식")
    st.latex(r"P(D|+) = \frac{P(+|D) \times P(D)}{P(+|D) \times P(D) + P(+|D^c) \times P(D^c)}")
    
    st.write("""
    여기서:
    - P(D|+) = 양성 예측도 (PPV): 검사 양성 시 실제 질병 있을 확률
    - P(+|D) = 민감도: 질병 있을 때 양성으로 나올 확률
    - P(D) = 유병률: 실제 질병 보유율
    - P(+|D^c) = 위양성률 (1-특이도): 질병 없을 때 양성으로 나올 확률
    - P(D^c) = 1-유병률: 실제 건강한 비율
    """)

    st.markdown("---")

    st.subheader("🎯 현재 파라미터로 계산")

    # 계산 과정
    with st.expander("📋 단계별 계산 과정 보기", expanded=False):
        st.write("**단계 1: 분자 계산**")
        numerator_val = sensitivity * prevalence
        st.latex(f"P(+|D) \\times P(D) = {sensitivity:.2f} \\times {prevalence:.2f} = {numerator_val:.4f}")

        st.write("**단계 2: 분모의 두 번째 항**")
        false_pos_rate = (1 - specificity) * (1 - prevalence)
        st.latex(f"P(+|D^c) \\times P(D^c) = {1-specificity:.2f} \\times {1-prevalence:.2f} = {false_pos_rate:.4f}")

        st.write("**단계 3: 분모 전체**")
        denominator_val = numerator_val + false_pos_rate
        st.latex(f"\\text{{분모}} = {numerator_val:.4f} + {false_pos_rate:.4f} = {denominator_val:.4f}")

        st.write("**단계 4: 최종 계산 (분자 ÷ 분모)**")
        st.latex(f"PPV = \\frac{{{numerator_val:.4f}}}{{{denominator_val:.4f}}} = {ppv:.4f} = {ppv:.2%}")

    # 최종 결과
    st.success(f"""
    🎯 **현재 설정에서:**
    
    **양성 예측도 (PPV) = {ppv:.2%}**
    
    즉, 검사가 양성으로 나온 사람 중 {ppv:.1%}가 실제 환자입니다.
    """)

    st.markdown("---")

    st.subheader("💡 핵심 통찰")
    st.write(f"""
    - **민감도({sensitivity:.0%})**가 높아도, 유병률({prevalence:.0%})이 낮으면 양성 예측도는 **{ppv:.0%}**일 수 있습니다.
    - 이는 **기저율 오류(Base Rate Fallacy)**의 좋은 예입니다.
    - 동일한 검사 성능이어도 **유병률에 따라 신뢰도가 크게 달라집니다.**
    """)

# ============================================================
# TAB 3: 연습 문제
# ============================================================

with tab3:
    # 학생 연습 문제
    st.header("✏️ 학생 연습 문제")
    st.write("아래의 문제를 직접 풀어보고 답을 입력하여 확인해 보세요!")

    st.markdown("---")

    # 문제 1
    st.subheader("📌 문제 1: 기본 개념 이해")
    st.write("""
    어떤 질병 검사의 특성은 다음과 같습니다:
    - **민감도**: 85% (질병이 있을 때 양성으로 나올 확률)
    - **특이도**: 95% (질병이 없을 때 음성으로 나올 확률)
    - **유병률**: 5% (전체 인구 중 질병 보유자 비율)

    **질문**: 검사가 양성(+)으로 나왔을 때, 실제로 질병이 있을 확률(양성 예측도)은?
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        sensitivity_1 = 0.85
        specificity_1 = 0.95
        prevalence_1 = 0.05
        
        tp_1 = 1000 * prevalence_1 * sensitivity_1
        fp_1 = 1000 * (1 - prevalence_1) * (1 - specificity_1)
        ppv_1 = tp_1 / (tp_1 + fp_1)
        
        user_answer_1 = st.number_input(
            "답 입력 (소수점 셋째 자리까지, 예: 0.461):",
            min_value=0.0,
            max_value=1.0,
            step=0.001,
            key="problem1"
        )
        
        if st.button("정답 확인", key="check1"):
            if abs(user_answer_1 - ppv_1) < 0.005:
                st.success(f"✅ 정답입니다! 양성 예측도 = {ppv_1:.3f} ({ppv_1:.1%})")
                st.write(f"""
                **계산 과정:**
                - 실제 질병 있는 경우: 1000명 중 {int(prevalence_1*1000)}명
                - 양성 검사: {int(tp_1)}명 (질병 있음 × 민감도)
                - 위양성: {int(fp_1)}명 (질병 없음 × (1-특이도))
                - PPV = {int(tp_1)} / ({int(tp_1)} + {int(fp_1)}) = **{ppv_1:.1%}**
                """)
            else:
                st.error(f"❌ 틀렸습니다. 정답: {ppv_1:.3f} ({ppv_1:.1%})")
                st.write(f"당신의 답: {user_answer_1:.3f}")

    st.markdown("---")

    # 문제 2
    st.subheader("📌 문제 2: 유병률 변화의 영향")
    st.write("""
    문제 1과 동일한 검사이지만, 유병률이 다른 지역에서 사용됩니다.
    - **민감도**: 85%
    - **특이도**: 95%
    - **유병률**: 20% (문제 1은 5%였음)

    **질문**: 유병률이 20%일 때, 양성 예측도는 몇 %일까요?
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        sensitivity_2 = 0.85
        specificity_2 = 0.95
        prevalence_2 = 0.20
        
        tp_2 = 1000 * prevalence_2 * sensitivity_2
        fp_2 = 1000 * (1 - prevalence_2) * (1 - specificity_2)
        ppv_2 = tp_2 / (tp_2 + fp_2)
        
        user_answer_2 = st.number_input(
            "답 입력 (소수점 셋째 자리까지, 예: 0.789):",
            min_value=0.0,
            max_value=1.0,
            step=0.001,
            key="problem2"
        )
        
        if st.button("정답 확인", key="check2"):
            if abs(user_answer_2 - ppv_2) < 0.005:
                st.success(f"✅ 정답입니다! 양성 예측도 = {ppv_2:.3f} ({ppv_2:.1%})")
                st.write(f"""
                **계산 과정:**
                - 실제 질병 있는 경우: 1000명 중 {int(prevalence_2*1000)}명
                - 양성 검사: {int(tp_2)}명 (질병 있음 × 민감도)
                - 위양성: {int(fp_2)}명 (질병 없음 × (1-특이도))
                - PPV = {int(tp_2)} / ({int(tp_2)} + {int(fp_2)}) = **{ppv_2:.1%}**
                
                **비교**: 문제 1에서는 {ppv_1:.1%}였는데, 유병률이 5배 증가하면서 {ppv_2:.1%}로 증가했습니다!
                """)
            else:
                st.error(f"❌ 틀렸습니다. 정답: {ppv_2:.3f} ({ppv_2:.1%})")
                st.write(f"당신의 답: {user_answer_2:.3f}")

    st.markdown("---")

    # 문제 3
    st.subheader("📌 문제 3: 다양한 파라미터")
    st.write("""
    새로운 질병 검사:
    - **민감도**: 92%
    - **특이도**: 88%
    - **유병률**: 3%

    **질문**: 검사가 양성으로 나왔을 때, 실제로 질병이 있을 확률은?
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        sensitivity_3 = 0.92
        specificity_3 = 0.88
        prevalence_3 = 0.03
        
        tp_3 = 1000 * prevalence_3 * sensitivity_3
        fp_3 = 1000 * (1 - prevalence_3) * (1 - specificity_3)
        ppv_3 = tp_3 / (tp_3 + fp_3)
        
        user_answer_3 = st.number_input(
            "답 입력 (소수점 셋째 자리까지, 예: 0.150):",
            min_value=0.0,
            max_value=1.0,
            step=0.001,
            key="problem3"
        )
        
        if st.button("정답 확인", key="check3"):
            if abs(user_answer_3 - ppv_3) < 0.005:
                st.success(f"✅ 정답입니다! 양성 예측도 = {ppv_3:.3f} ({ppv_3:.1%})")
                st.write(f"""
                **계산 과정:**
                - 실제 질병 있는 경우: 1000명 중 {int(prevalence_3*1000)}명
                - 양성 검사: {int(tp_3)}명
                - 위양성: {int(fp_3)}명
                - PPV = {int(tp_3)} / ({int(tp_3)} + {int(fp_3)}) = **{ppv_3:.1%}**
                
                **통찰**: 민감도가 높아도(92%) 유병률이 매우 낮으면(3%), 양성 예측도가 낮습니다!
                """)
            else:
                st.error(f"❌ 틀렸습니다. 정답: {ppv_3:.3f} ({ppv_3:.1%})")
                st.write(f"당신의 답: {user_answer_3:.3f}")

    st.markdown("---")

    st.subheader("🔖 디지털 탐구 일지")
    st.write("현재 실험한 조건과 결과를 저장해 두고, 유병률과 PPV 관계를 스스로 정리해 보세요.")

    if st.button("내 일지에 저장", key="save_journal"):
        st.session_state.journal.append({
            "저장 시간": pd.Timestamp.now().strftime("%H:%M:%S"),
            "민감도": f"{sensitivity:.1%}",
            "특이도": f"{specificity:.1%}",
            "유병률": f"{prevalence:.2%}",
            "PPV": f"{ppv:.2%}",
            "NPV": f"{npv:.2%}"
        })
        st.success("✅ 일지가 저장되었습니다.")

    journal_df = pd.DataFrame(st.session_state.journal)
    if not journal_df.empty:
        st.dataframe(journal_df, use_container_width=True)
    else:
        st.info("일지를 저장하면 여기에 실험 결과가 기록됩니다.")

    st.text_area(
        "데이터 3개를 모아 유병률과 양성 예측도의 관계를 한 문장으로 정리해보세요.",
        value=st.session_state.journal_note,
        key="journal_note",
        height=120
    )

    st.markdown("---")

    # 보너스: 직접 계산해보기
    st.subheader("🎁 보너스: 무작위 문제로 베이즈 정리 연습")
    st.write("""
    아래에 제시된 무작위 검사 정보를 보고, 베이즈 정리를 직접 적용해 보세요.
    값은 파라미터 설정과 무관하게 새로 생성되며, 직접 수식을 작성할 수 있습니다.
    """)

    if "bonus_problem" not in st.session_state:
        st.session_state.bonus_problem = {
            "sens": round(random.choice([0.72, 0.78, 0.82, 0.85, 0.88, 0.91, 0.93, 0.96]), 2),
            "spec": round(random.choice([0.76, 0.80, 0.85, 0.88, 0.92, 0.95, 0.97]), 2),
            "prev": round(random.choice([0.01, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20]), 2)
        }

    if st.button("새 문제 생성", key="bonus_new_problem"):
        st.session_state.bonus_problem = {
            "sens": round(random.choice([0.72, 0.78, 0.82, 0.85, 0.88, 0.91, 0.93, 0.96]), 2),
            "spec": round(random.choice([0.76, 0.80, 0.85, 0.88, 0.92, 0.95, 0.97]), 2),
            "prev": round(random.choice([0.01, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20]), 2)
        }

    sens_input = st.session_state.bonus_problem["sens"]
    spec_input = st.session_state.bonus_problem["spec"]
    prev_input = st.session_state.bonus_problem["prev"]

    st.markdown("---")

    st.subheader("📝 문제 정보")
    st.write(f"- **민감도**: {sens_input:.0%}")
    st.write(f"- **특이도**: {spec_input:.0%}")
    st.write(f"- **유병률**: {prev_input:.0%}")

    st.write("""
    다음 공식을 이용하여 계산식을 직접 작성해 보세요:

    $$\\text{PPV} = \\frac{\\text{민감도} \\times \\text{유병률}}{\\text{민감도} \\times \\text{유병률} + (1-\\text{특이도}) \\times (1-\\text{유병률})}$$
    """)

    st.markdown("---")

    st.subheader("✏️ 직접 수식 작성")
    formula_1 = st.text_area(
        "1) 분자 계산식 입력",
        value="예: 0.85 × 0.05",
        height=80,
        key="bonus_formula_1"
    )
    formula_2 = st.text_area(
        "2) 분모 계산식 입력",
        value="예: (0.85 × 0.05) + ((1-0.95) × (1-0.05))",
        height=80,
        key="bonus_formula_2"
    )
    formula_3 = st.text_area(
        "3) PPV 최종 계산식 입력",
        value="예: 0.0425 / 0.0475",
        height=80,
        key="bonus_formula_3"
    )

    st.markdown("---")

    # 실제 계산
    numerator = sens_input * prev_input
    def false_positive_rate(specificity, prevalence):
        return (1 - specificity) * (1 - prevalence)
    false_pos_rate = false_positive_rate(spec_input, prev_input)
    denominator = numerator + false_pos_rate
    ppv_bonus = numerator / denominator if denominator > 0 else 0

    st.subheader("🔢 계산 결과 확인")
    num_answer = st.number_input(
        "분자 결과 입력 (소수점 4자리까지)",
        min_value=0.0,
        max_value=1.0,
        step=0.0001,
        format="%.4f",
        key="bonus_num_answer"
    )
    den_answer = st.number_input(
        "분모 결과 입력 (소수점 4자리까지)",
        min_value=0.0,
        max_value=2.0,
        step=0.0001,
        format="%.4f",
        key="bonus_den_answer"
    )
    ppv_answer = st.number_input(
        "PPV 결과 입력 (소수점 4자리까지)",
        min_value=0.0,
        max_value=1.0,
        step=0.0001,
        format="%.4f",
        key="bonus_ppv_answer"
    )

    if st.button("정답 확인", key="bonus_check"):
        correct = True
        if abs(num_answer - numerator) > 0.0001:
            st.error(f"분자 값이 다릅니다. 정답은 {numerator:.4f} 입니다.")
            correct = False
        if abs(den_answer - denominator) > 0.0001:
            st.error(f"분모 값이 다릅니다. 정답은 {denominator:.4f} 입니다.")
            correct = False
        if abs(ppv_answer - ppv_bonus) > 0.0001:
            st.error(f"PPV 값이 다릅니다. 정답은 {ppv_bonus:.4f} 입니다.")
            correct = False
        if correct:
            st.success("🎉 모두 정답입니다! 수식을 잘 적용했습니다.")

    st.markdown("---")

    st.subheader("📊 정답 예시")
    st.write(f"- 분자 = {sens_input:.2f} × {prev_input:.2f} = {numerator:.4f}")
    st.write(f"- (1-특이도) × (1-유병률) = {1-spec_input:.2f} × {1-prev_input:.2f} = {false_pos_rate:.4f}")
    st.write(f"- 분모 = {numerator:.4f} + {false_pos_rate:.4f} = {denominator:.4f}")
    st.write(f"- PPV = {numerator:.4f} / {denominator:.4f} = {ppv_bonus:.4f} ({ppv_bonus:.2%})")

