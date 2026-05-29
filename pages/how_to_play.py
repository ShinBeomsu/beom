from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="진단검사 탐구활동 안내",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 조건부확률 탐구활동 활용법")
st.write("이 페이지는 진단검사 수업 활동을 어떻게 진행하는지 안내하는 페이지입니다. 값 조절에 따라 각 차트와 결과가 어떻게 바뀌는지 직접 예시로 살펴볼 수 있습니다.")

project_root = Path(__file__).resolve().parents[1]
font_path = project_root / "assets" / "fonts" / "NotoSansCJKkr-Regular.otf"
if not font_path.exists():
    raise FileNotFoundError(f"한글 폰트 파일을 찾을 수 없습니다: {font_path}")

font_title = ImageFont.truetype(str(font_path), 30)
font_small = ImageFont.truetype(str(font_path), 18)
font_tiny = ImageFont.truetype(str(font_path), 15)


def draw_text_with_outline(draw, position, text, font, fill, outline="white", outline_width=2):
    x, y = position
    for offset_x in range(-outline_width, outline_width + 1):
        for offset_y in range(-outline_width, outline_width + 1):
            if offset_x == 0 and offset_y == 0:
                continue
            draw.text((x + offset_x, y + offset_y), text, fill=outline, font=font)
    draw.text((x, y), text, fill=fill, font=font)

st.markdown("---")

st.subheader("1. 어떤 순서로 진행해야 하나요?")
steps = [
    "① `pages/math_education.py`를 열어 수업 화면으로 이동합니다.",
    "② 왼쪽 슬라이더에서 민감도, 특이도, 유병률 값을 바꿉니다.",
    "③ 오른쪽의 요약, 분류표, 시각화가 즉시 바뀌는 모습을 관찰합니다.",
    "④ 민감도와 특이도의 변화에 따른 그래프 변화를 비교하면서 어떤 값이 늘고 줄어드는지 확인합니다.",
    "⑤ 각 변화가 분류표와 확률 계산에 어떻게 연결되는지 수학적 원리를 이해합니다.",
    "⑥ 마지막으로 연습문제를 풀며 마무리합니다.",
]
for step in steps:
    st.write(step)

st.markdown("---")

st.subheader("2. 값을 조절하면 어떤 것이 바뀌나요?")
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.write("- **민감도**가 높아지면 실제 환자 중 양성으로 잡히는 비율이 늘어납니다. 그래서 진양성이 늘고 위음성이 줄어드는 경향이 있습니다.")
    st.write("- **특이도**가 높아지면 건강한 사람 중 음성으로 잡히는 비율이 늘어납니다. 그래서 진음성이 늘고 위양성이 줄어드는 경향이 있습니다.")
    st.write("- **유병률**이 높아지면 전체 인구에서 실제 환자가 많아집니다. 같은 검사 성능이라도 양성 결과가 실제 환자일 가능성이 상대적으로 커지는 경향을 볼 수 있습니다.")

with col2:
    st.info("예시: 민감도가 95% → 99%로 올라가면, 실제 환자 중 놓치는 사람(위음성)이 줄어듭니다. 특이도가 90% → 99%로 올라가면, 건강한 사람 중 오진되는 사람(위양성)이 줄어듭니다.")

st.markdown("---")

st.subheader("3. 직접 조절하면서 변화를 확인해볼까요?")

st.write("아래 슬라이더를 바꾸면, 같은 10,000명을 기준으로 진단 결과 분류가 어떻게 변하는지 예시 차트를 바로 확인할 수 있습니다.")

sample_total = 10000

sensitivity = st.slider("민감도 (Sensitivity)", 0.50, 0.99, 0.95, 0.01)
specificity = st.slider("특이도 (Specificity)", 0.50, 0.99, 0.90, 0.01)
prevalence = st.slider("유병률 (Prevalence)", 0.01, 0.30, 0.10, 0.01)

# 계산 예시
sample_disease_positive = int(sample_total * prevalence)
sample_disease_negative = sample_total - sample_disease_positive
sample_true_positive = int(round(sample_disease_positive * sensitivity))
sample_false_negative = sample_disease_positive - sample_true_positive
sample_false_positive = int(round(sample_disease_negative * (1 - specificity)))
sample_true_negative = sample_disease_negative - sample_false_positive

summary_df = pd.DataFrame({
    "구분": ["진양성", "위음성", "위양성", "진음성"],
    "인원": [sample_true_positive, sample_false_negative, sample_false_positive, sample_true_negative],
})
summary_df["비율"] = (summary_df["인원"] / sample_total).round(3)

summary_df = summary_df.sort_values("인원", ascending=False)

bar_fig = px.bar(
    summary_df,
    x="구분",
    y="인원",
    color="구분",
    title="예시 분류 결과 (10,000명 기준)",
    labels={"인원": "사람 수", "구분": "결과 종류"}
)
bar_fig.update_layout(showlegend=False)
st.plotly_chart(bar_fig, use_container_width=True)

summary_metrics = pd.DataFrame({
    "지표": ["진양성", "위음성", "위양성", "진음성"],
    "값": [
        f"{sample_true_positive}명 ({sample_true_positive/sample_total:.1%})",
        f"{sample_false_negative}명 ({sample_false_negative/sample_total:.1%})",
        f"{sample_false_positive}명 ({sample_false_positive/sample_total:.1%})",
        f"{sample_true_negative}명 ({sample_true_negative/sample_total:.1%})",
    ]
})
st.dataframe(summary_metrics, use_container_width=True, hide_index=True)

size_chart_image = Image.new("RGB", (900, 260), "white")
size_chart_draw = ImageDraw.Draw(size_chart_image)
size_chart_draw.rounded_rectangle((0, 0, 899, 259), radius=12, fill="white", outline=(180, 180, 180))

draw_text_with_outline(size_chart_draw, (18, 16), "값이 바뀌면 막대 길이도 바뀝니다", font_title, "black")
draw_text_with_outline(size_chart_draw, (18, 52), "표의 인원 수에 따라 막대의 실제 크기가 달라집니다.", font_small, (70, 70, 70))

category_colors = {
    "진양성": "#e74c3c",
    "위음성": "#3498db",
    "위양성": "#f39c12",
    "진음성": "#2ecc71",
}

bar_start_x = 170
bar_top_y = 85
bar_spacing = 40
bar_scale = 700
max_count = max(summary_df["인원"])

for idx, row in enumerate(summary_df.itertuples(index=False)):
    label = row.구분
    count = row.인원
    bar_width = max(12, int((count / max_count) * bar_scale))
    x0 = bar_start_x
    y0 = bar_top_y + idx * bar_spacing
    x1 = x0 + bar_width
    y1 = y0 + 24
    size_chart_draw.rectangle((x0, y0, x1, y1), fill=category_colors[label], outline=(255, 255, 255))
    draw_text_with_outline(size_chart_draw, (18, y0 + 2), label, font_small, "black")
    draw_text_with_outline(size_chart_draw, (x1 + 10, y0 + 2), f"{count}명", font_small, (40, 40, 40))
    draw_text_with_outline(size_chart_draw, (x0 - 50, y0 + 2), f"{count/sample_total:.1%}", font_small, (60, 60, 60))

size_chart_buffer = BytesIO()
size_chart_image.save(size_chart_buffer, format="PNG")
size_chart_bytes = size_chart_buffer.getvalue()

st.image(size_chart_bytes, caption="표의 수치가 바뀌면 막대의 실제 크기가 달라집니다.")

st.markdown("---")

st.subheader("4. 값 변화에 따라 그래프가 어떻게 달라지나요?")

st.write("`math_education.py`에서는 민감도, 특이도, 유병률을 바꾸면 같은 자료가 다른 형태의 그래프로 어떻게 보이는지 확인할 수 있습니다.")

chart_cols = st.columns(2)

with chart_cols[0]:
    trend_df = pd.DataFrame({
        "항목": ["진양성", "위음성", "위양성", "진음성"],
        "값": [sample_true_positive, sample_false_negative, sample_false_positive, sample_true_negative],
    })
    pie_fig = px.pie(
        trend_df,
        values="값",
        names="항목",
        title="검사 결과 비율 예시"
    )
    st.plotly_chart(pie_fig, use_container_width=True)

with chart_cols[1]:
    scale_df = pd.DataFrame({
        "구분": ["질병 있음", "질병 없음"],
        "인원": [sample_disease_positive, sample_disease_negative],
    })
    scale_fig = px.bar(
        scale_df,
        x="구분",
        y="인원",
        color="구분",
        title="유병률에 따른 실제 질병 보유 인원"
    )
    scale_fig.update_layout(showlegend=False)
    st.plotly_chart(scale_fig, use_container_width=True)

st.markdown("---")

st.subheader("5. 수업에서 어떻게 활용할 수 있나요?")

st.write("- 민감도 슬라이더를 높이면 위음성이 줄어드는 모습을 보고, 놓치는 환자가 얼마나 줄어드는지 확인합니다.")
st.write("- 특이도 슬라이더를 높이면 위양성이 줄어드는 모습을 보고, 오진이 얼마나 줄어드는지 확인합니다.")
st.write("- 유병률 슬라이더를 높이면 전체 분포가 바뀌어, 양성 결과가 실제 환자일 가능성이 바뀌는지 관찰합니다.")
st.write("- Waffle, Sankey, Venn 차트는 같은 자료를 다른 방식으로 보여주므로, 수치와 그림이 어떻게 연결되는지 함께 비교합시다.")

st.markdown("---")

st.subheader("6. 기준값을 넣었을 때의 예시 결과")

fixed_sensitivity = 0.95
fixed_specificity = 0.90
fixed_prevalence = 0.10
fixed_total = 10000

fixed_disease_positive = int(fixed_total * fixed_prevalence)
fixed_disease_negative = fixed_total - fixed_disease_positive
fixed_true_positive = int(round(fixed_disease_positive * fixed_sensitivity))
fixed_false_negative = fixed_disease_positive - fixed_true_positive
fixed_false_positive = int(round(fixed_disease_negative * (1 - fixed_specificity)))
fixed_true_negative = fixed_disease_negative - fixed_false_positive

st.write("아래 예시는 하나의 기준값을 넣었을 때 어떤 그림이 만들어지는지 보여줍니다.")

summary_cols = st.columns(3)
with summary_cols[0]:
    st.metric("민감도", f"{fixed_sensitivity:.0%}")
with summary_cols[1]:
    st.metric("특이도", f"{fixed_specificity:.0%}")
with summary_cols[2]:
    st.metric("유병률", f"{fixed_prevalence:.0%}")

# Waffle 예시 이미지
waffle_rows = 20
waffle_cols = 50
waffle_cell = 12
waffle_width = 900
waffle_height = 500
waffle_image = Image.new("RGB", (waffle_width, waffle_height), "white")
waffle_draw = ImageDraw.Draw(waffle_image)
waffle_draw.rounded_rectangle((0, 0, waffle_width - 1, waffle_height - 1), radius=12, fill="white", outline=(180, 180, 180))

waffle_title = f"예시값: 민감도 {fixed_sensitivity:.0%}, 특이도 {fixed_specificity:.0%}, 유병률 {fixed_prevalence:.0%}"
draw_text_with_outline(waffle_draw, (20, 16), waffle_title, font_title, "black")
draw_text_with_outline(waffle_draw, (20, 48), "1000칸 기준의 분포(각 칸 = 10명)", font_small, (80, 80, 80))

waffle_grid_x = 20
waffle_grid_y = 72
waffle_pattern = [
    ("진양성", fixed_true_positive // 10, "#e74c3c"),
    ("위양성", fixed_false_positive // 10, "#f39c12"),
    ("위음성", fixed_false_negative // 10, "#3498db"),
    ("진음성", fixed_true_negative // 10, "#2ecc71"),
]

waffle_cells = []
for label, count, color in waffle_pattern:
    waffle_cells.extend([(label, color)] * count)

# 1000칸을 50x20 그리드에 넣기
for idx, (label, color) in enumerate(waffle_cells):
    row = idx // waffle_cols
    col = idx % waffle_cols
    x0 = waffle_grid_x + col * waffle_cell
    y0 = waffle_grid_y + row * waffle_cell
    x1 = x0 + waffle_cell - 1
    y1 = y0 + waffle_cell - 1
    waffle_draw.rectangle((x0, y0, x1, y1), fill=color, outline=(255, 255, 255))

# 격자선 유지
for row in range(waffle_rows + 1):
    y = waffle_grid_y + row * waffle_cell
    waffle_draw.line((waffle_grid_x, y, waffle_grid_x + waffle_cols * waffle_cell, y), fill=(230, 230, 230))
for col in range(waffle_cols + 1):
    x = waffle_grid_x + col * waffle_cell
    waffle_draw.line((x, waffle_grid_y, x, waffle_grid_y + waffle_rows * waffle_cell), fill=(230, 230, 230))

legend_x = waffle_grid_x + waffle_cols * waffle_cell + 18
legend_y = waffle_grid_y
legend_items = [
    ("진양성", fixed_true_positive, fixed_true_positive / fixed_total, "#e74c3c"),
    ("위양성", fixed_false_positive, fixed_false_positive / fixed_total, "#f39c12"),
    ("위음성", fixed_false_negative, fixed_false_negative / fixed_total, "#3498db"),
    ("진음성", fixed_true_negative, fixed_true_negative / fixed_total, "#2ecc71"),
]
for idx, (label, count, ratio, color) in enumerate(legend_items):
    box_y = legend_y + idx * 30
    waffle_draw.rectangle((legend_x, box_y, legend_x + 18, box_y + 18), fill=color)
    draw_text_with_outline(waffle_draw, (legend_x + 26, box_y - 1), f"{label}: {count}명 ({ratio:.1%})", font_small, "black")

# Venn 예시 이미지
venn_width = 900
venn_height = 500
venn_image = Image.new("RGB", (venn_width, venn_height), "white")
venn_draw = ImageDraw.Draw(venn_image)
venn_draw.rounded_rectangle((0, 0, venn_width - 1, venn_height - 1), radius=12, fill="white", outline=(180, 180, 180))
draw_text_with_outline(venn_draw, (24, 18), "Venn 예시: 겹침 영역의 의미", font_title, "black")
draw_text_with_outline(venn_draw, (24, 52), "검사 양성과 실제 질병의 겹치는 부분을 보여줍니다", font_small, (80, 80, 80))

left_circle = (260, 250, 400, 380)
right_circle = (500, 250, 640, 380)
venn_draw.ellipse(left_circle, fill=(231, 76, 60), outline=(180, 40, 20))
venn_draw.ellipse(right_circle, fill=(52, 152, 219), outline=(20, 90, 180))
venn_draw.ellipse((left_circle[0] + 45, left_circle[1] + 20, right_circle[2] - 45, right_circle[3] - 20), fill=(255, 215, 0), outline=(230, 180, 0))

venn_labels = [
    ("질병 있음\n10%\n1,000명", (150, 220), (0,0,0)),
    ("검사 양성\n18.5%\n1,850명", (700, 220), (0,0,0)),
    ("진양성\n9.5%\n950명", (370, 250), (0,0,0)),
    ("위음성\n0.5%\n50명", (150, 410), (0,0,0)),
    ("위양성\n9.0%\n900명", (700, 410), (0,0,0)),
]
for text, pos, color in venn_labels:
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        draw_text_with_outline(venn_draw, (pos[0], pos[1] + idx * 18), line, font_small, color)

# 이미지 저장
waffle_buffer = BytesIO()
waffle_image.save(waffle_buffer, format="PNG")
waffle_bytes = waffle_buffer.getvalue()

venn_buffer = BytesIO()
venn_image.save(venn_buffer, format="PNG")
venn_bytes = venn_buffer.getvalue()

image_cols = st.columns(2)
with image_cols[0]:
    st.image(waffle_bytes, caption="Waffle 예시: 1000칸 기준")
with image_cols[1]:
    st.image(venn_bytes, caption="Venn 예시: 겹침 영역")
