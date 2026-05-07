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

st.title("👨‍⚕️ 당신은 정확한 진단을 내릴 수 있습니까?")
st.subheader("🏥 조건부확률을 이용한 질병진단")
st.write("검사 정확도가 99%이고 유병률이 1%일 때, 양성인 사람이 실제 환자일 확률을 예측해 보세요.")
user_guess_text = st.text_input("예상 확률을 입력해 보세요 (%):", "", placeholder="숫자로만 입력하세요", key="init_guess")

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
        0.0, 1.0, 0.95,
        0.01,
        help="질병이 있을 때 검사가 양성으로 나올 확률"
    )
    st.caption("질병 있음 → 양성 검사")
    
    specificity = st.slider(
        "특이도 (Specificity)",
        0.0, 1.0, 0.90,
        0.01,
        help="질병이 없을 때 검사가 음성으로 나올 확률"
    )
    st.caption("질병 없음 → 음성 검사")
    
    prevalence = st.slider(
        "유병률 (Prevalence)",
        0.0, 1.0, 0.10,
        0.001,
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
    st.header("❓ 결과를 보기 전, 당신의 직관은?")
    st.write("아래 정보를 보고, '검사가 양성으로 나왔을 때 실제로 병에 걸렸을 확률'을 계산해 보세요!")

    # 데이터 테이블 제시
    st.subheader("📊 주어진 데이터")

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

    st.markdown("---")

    st.subheader("❓ 핵심 질문")
    st.write(f"""
    **검사가 양성(+)으로 나온 {test_positive}명 중에서, 실제로 질병이 있는 사람은 {true_positive}명입니다.**

    👉 **따라서 검사 결과가 양성일 때, 실제로 질병이 있을 확률은?**
    """)

    # 정답 선택지
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        option_a = round((true_positive / test_positive) * 100, 1)
        btn_a = st.checkbox(f"🔘 {option_a}%")

    with col2:
        option_b = round((sensitivity * 100), 1)
        btn_b = st.checkbox(f"🔘 {option_b}% (민감도)")

    with col3:
        option_c = round((specificity * 100), 1)
        btn_c = st.checkbox(f"🔘 {option_c}% (특이도)")

    with col4:
        option_d = round((prevalence * 100), 1)
        btn_d = st.checkbox(f"🔘 {option_d}% (유병률)")

    # 정답 확인
    if st.button("답변 제출", key="prediction_check"):
        if btn_a:
            st.success(f"🎯 정답입니다! ({option_a}%)")
            st.write(f"""
            양성 예측도 (PPV) = {true_positive} / {test_positive} = **{ppv:.2%}**
            """)
        elif btn_b or btn_c or btn_d:
            st.error(f"❌ 아쉽습니다! 정답: {ppv:.1%}")

    st.markdown("---")

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

    # 시각화: 2개만 나란히 배치
    st.subheader("📈 시각화")

    col_left, col_right = st.columns([1.2, 1])

    # 왼쪽: Waffle Chart
    with col_left:
        st.write("**Waffle Chart: 1,000명 분포**")
        
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
            height=400,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, autorange='reversed'),
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_waffle, use_container_width=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("🔴 진양성")
        c2.markdown("🟠 위양성")
        c3.markdown("🔵 위음성")
        c4.markdown("🟢 진음성")

    # 오른쪽: Sankey Diagram
    with col_right:
        st.write("**Sankey: 인구 흐름**")
        
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
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(255,255,255,1)',
            plot_bgcolor='rgba(255,255,255,1)'
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

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

    st.markdown("---")
    st.subheader("🎮 미션 임파서블")
    st.write("슬라이더를 자유롭게 움직이기보다, 아래 목표를 달성해 보세요.")

    st.write("**미션 A:** 현재 민감도와 특이도를 고정한 채, 유병률을 높여서 PPV를 80% 이상으로 만들어 보세요.")
    if ppv >= 0.8:
        st.success("🎉 미션 A 성공! 현재 PPV가 80% 이상입니다.")
    else:
        st.info(f"현재 PPV는 {ppv:.2%}입니다. 유병률을 더 높여서 목표를 달성해 보세요.")

    st.write("**미션 B:** 희귀병 상황(유병률 0.1%)에서 위양성 수가 진양성 수보다 적어지도록 만들어 보세요.")
    if prevalence <= 0.001 and false_positive < true_positive:
        st.success("🎉 미션 B 성공! 희귀병 상황에서 위양성 수가 진양성 수보다 적습니다.")
    else:
        st.info(
            f"현재 유병률은 {prevalence:.2%}입니다. 특이도를 높이고 유병률을 낮춰서 위양성을 줄여보세요. "
            f"현재 위양성 {false_positive}명, 진양성 {true_positive}명입니다."
        )

    st.markdown("---")
    st.subheader("🏥 의사 결정 시뮬레이션")
    st.write("환자가 양성 판정을 받았습니다. 이 병은 수술 부작용이 크기 때문에 신중하게 판단해야 합니다.")
    decision = st.radio(
        "어떤 처방을 권하시겠습니까?",
        ["즉시 수술", "정밀 재검사 권유", "단순 경과 관찰"],
        key="decision_radio"
    )

    if st.button("진단 결과 제출", key="decision_submit"):
        if decision == "즉시 수술":
            if ppv < 0.5:
                st.warning("위험한 결정입니다! 양성 예측도가 낮아 오진일 확률이 높습니다.")
                st.write("결과: 불필요한 수술로 환자가 고통을 겪을 수 있습니다.")
            else:
                st.success("데이터에 근거한 합리적인 결정을 내리셨습니다.")
                st.write("결과: 수술이 적절히 진행되어 환자가 보호받았습니다.")
        elif decision == "정밀 재검사 권유":
            st.success("현명한 선택입니다! 추가 검사로 오진 위험을 줄였습니다.")
            st.write("결과: 정확한 진단을 위한 재검사가 진행되었습니다.")
        else:
            if ppv < 0.3:
                st.success("현명한 결정입니다. 당장의 수술보다 경과 관찰이 안전합니다.")
            else:
                st.warning("주의가 필요합니다. PPV가 비교적 높으므로 추가 검사나 전문의 자문이 필요합니다.")

# ============================================================
# TAB 3: 연습 문제
# ============================================================

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
st.subheader("🎁 보너스: 수식으로 직접 계산해보기")
st.write("""
베이즈 정리를 사용하여 양성 예측도를 계산할 수 있습니다:

$$\\text{PPV} = \\frac{\\text{민감도} \\times \\text{유병률}}{\\text{민감도} \\times \\text{유병률} + (1-\\text{특이도}) \\times (1-\\text{유병률})}$$
""")

col1, col2, col3 = st.columns(3)

with col1:
    sens_input = st.slider("민감도 선택", 0.0, 1.0, 0.9, 0.01)

with col2:
    spec_input = st.slider("특이도 선택", 0.0, 1.0, 0.9, 0.01)

with col3:
    prev_input = st.slider("유병률 선택", 0.0, 1.0, 0.1, 0.01)

# 계산
numerator = sens_input * prev_input
denominator = (sens_input * prev_input) + ((1 - spec_input) * (1 - prev_input))

if denominator > 0:
    ppv_bonus = numerator / denominator
else:
    ppv_bonus = 0

st.markdown("---")

st.subheader("📝 베이즈 정리 공식 적용")
st.write("""
다음 공식을 이용하여 양성 예측도를 계산해 보세요:

$$\\text{PPV} = \\frac{\\text{민감도} \\times \\text{유병률}}{\\text{민감도} \\times \\text{유병률} + (1-\\text{특이도}) \\times (1-\\text{유병률})}$$
""")

st.write("**각 값을 직접 계산해서 입력해 보세요:**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("민감도", f"{sens_input:.2f}")
with col2:
    st.metric("특이도", f"{spec_input:.2f}")
with col3:
    st.metric("유병률", f"{prev_input:.2f}")
with col4:
    st.metric("1-유병률", f"{1-prev_input:.2f}")

st.markdown("---")

st.subheader("✏️ 단계별 계산")

# 단계 1: 분자 계산
st.write("**단계 1️⃣: 분자(민감도 × 유병률) 계산**")
col1, col2, col3 = st.columns([1, 1, 1.5])
with col1:
    step1_input = st.number_input(
        "분자 값 입력 (소수점 4자리까지):",
        min_value=0.0,
        max_value=1.0,
        step=0.0001,
        format="%.4f",
        key="step1"
    )
with col2:
    st.write(f"**정답**: {numerator:.4f}")
with col3:
    if abs(step1_input - numerator) < 0.0001:
        st.success("✅ 맞습니다!")
    elif step1_input > 0:
        st.error("❌ 다시 계산해보세요")

st.latex(f"\\text{{분자}} = {sens_input:.2f} \\times {prev_input:.2f} = {numerator:.4f}")

st.markdown("---")

# 단계 2: 분모 계산
st.write("**단계 2️⃣: 분모 계산**")
st.write("분모 = (민감도 × 유병률) + ((1-특이도) × (1-유병률))")

col1, col2 = st.columns(2)
with col1:
    st.write("먼저 (1-특이도) × (1-유병률) 계산:")
    step2a_input = st.number_input(
        "(1-특이도) × (1-유병률) 값 입력:",
        min_value=0.0,
        max_value=1.0,
        step=0.0001,
        format="%.4f",
        key="step2a"
    )
    step2a_correct = (1 - spec_input) * (1 - prev_input)
    if abs(step2a_input - step2a_correct) < 0.0001:
        st.success("✅ 맞습니다!")
    elif step2a_input > 0:
        st.error("❌ 다시 계산해보세요")
    st.latex(f"(1-{spec_input:.2f}) \\times (1-{prev_input:.2f}) = {step2a_correct:.4f}")

with col2:
    st.write("분모 전체 계산:")
    step2b_input = st.number_input(
        "분모 값 입력 (소수점 4자리까지):",
        min_value=0.0,
        max_value=2.0,
        step=0.0001,
        format="%.4f",
        key="step2b"
    )
    if abs(step2b_input - denominator) < 0.0001:
        st.success("✅ 맞습니다!")
    elif step2b_input > 0:
        st.error("❌ 다시 계산해보세요")
    st.latex(f"\\text{{분모}} = {numerator:.4f} + {step2a_correct:.4f} = {denominator:.4f}")

st.markdown("---")

# 단계 3: 최종 계산
st.write("**단계 3️⃣: 최종 계산 (분자 ÷ 분모)**")
col1, col2, col3 = st.columns([1, 1, 1.5])
with col1:
    step3_input = st.number_input(
        "양성 예측도 입력 (소수점 4자리까지):",
        min_value=0.0,
        max_value=1.0,
        step=0.0001,
        format="%.4f",
        key="step3"
    )
with col2:
    st.write(f"**정답**: {ppv_bonus:.4f}")
with col3:
    if abs(step3_input - ppv_bonus) < 0.0001:
        st.success("✅ 정답입니다!")
        st.balloons()
    elif step3_input > 0:
        st.error("❌ 다시 계산해보세요")

st.latex(f"\\text{{PPV}} = \\frac{{{numerator:.4f}}}{{{denominator:.4f}}} = {ppv_bonus:.4f}")

st.markdown("---")

# 최종 결과
st.subheader("📊 최종 결과")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("민감도", f"{sens_input:.0%}")
with col2:
    st.metric("특이도", f"{spec_input:.0%}")
with col3:
    st.metric("유병률", f"{prev_input:.0%}")
with col4:
    st.metric("양성 예측도", f"{ppv_bonus:.2%}", delta="계산 결과")

st.success(f"""
🎯 **최종 양성 예측도 = {ppv_bonus:.4f} = {ppv_bonus:.2%}**

이는 검사가 양성으로 나온 사람 중 실제로 질병이 있을 확률입니다!
""")
