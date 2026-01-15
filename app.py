import streamlit as st
import pandas as pd
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime
import time

# --------------------------------------------------------------------------
# [1] 기본 설정 및 디자인 (강력한 투명망토 💣)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 신년 운세",
    page_icon="🐎",
    layout="centered"
)

# 🎨 Streamlit 마크, 풋터, 헤더, 모바일 뱃지까지 강제 삭제
hide_streamlit_style = """
            <style>
            /* 헤더와 풋터 숨기기 */
            header {visibility: hidden !important;}
            [data-testid="stHeader"] {display: none !important;}
            footer {visibility: hidden !important; display: none !important;}
            [data-testid="stFooter"] {display: none !important;}
            
            /* 모바일에서 뜨는 뱃지 숨기기 */
            .viewerBadge_container__1QSob {display: none !important;}
            
            /* 화면 여백 조정 */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 5rem !important;
            }
            #MainMenu {visibility: hidden !important; display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 글씨 디자인
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; color: #FF4B4B; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .sub-title { font-size: 1.0rem; color: #555; text-align: center; margin-bottom: 25px; line-height: 1.4; }
    .result-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .month-text { font-size: 0.95rem; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [2] 데이터 준비
# --------------------------------------------------------------------------
VAR_YEAR_NUM = 1 
MONTH_CONSTANTS = [0, 2, 5, 3, 4, 1, 6, 2, 5, 3, 4, 1, 6] 

TIME_LUCK = {
    "자시 (23:00 ~ 01:00)": "남들보다 밤에 정신이 맑아지며, 창의적인 생각이 뛰어난 지략가입니다.",
    "축시 (01:00 ~ 03:00)": "묵묵히 한 우물을 파서 성공하는 끈기의 아이콘입니다. 말년 운이 좋습니다.",
    "인시 (03:00 ~ 05:00)": "활동적이고 추진력이 강하여 리더가 될 자질을 타고났습니다.",
    "묘시 (05:00 ~ 07:00)": "재치와 유머가 넘치며 주변 사람들에게 인기가 많은 매력적인 사람입니다.",
    "진시 (07:00 ~ 09:00)": "이상과 포부가 크고, 한 번 마음먹은 일은 끝까지 해내는 대장부 스타일입니다.",
    "사시 (09:00 ~ 11:00)": "두뇌 회전이 빠르고 처세술이 좋아 어디서든 능력을 인정받습니다.",
    "오시 (11:00 ~ 13:00)": "화끈하고 솔직한 성격으로, 예술적 감각이나 화려한 직업이 잘 어울립니다.",
    "미시 (13:00 ~ 15:00)": "온화하고 부드러운 성품을 가졌으나, 내면은 강단이 있는 외유내강형입니다.",
    "신시 (15:00 ~ 17:00)": "손재주가 좋고 다재다능하여, 기술이나 전문직에서 성공할 운입니다.",
    "유시 (17:00 ~ 19:00)": "깔끔하고 완벽주의 성향이 있어 재물을 잘 모으고 관리하는 능력이 탁월합니다.",
    "술시 (19:00 ~ 21:00)": "책임감이 강하고 신의가 있어 주변 사람들의 깊은 신뢰를 받습니다.",
    "해시 (21:00 ~ 23:00)": "지혜롭고 포용력이 넓어, 남을 가르치거나 상담하는 일에 소질이 있습니다.",
    "모름": "태어난 시가 불분명하지만, 당신은 스스로 운명을 개척할 강한 힘을 가지고 있습니다."
}

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("db.xlsx", dtype={'code': str})
        return df
    except:
        return None

df = load_data()

# --------------------------------------------------------------------------
# [3] 화면 구성 (입력란)
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🐎 2026 토정비결</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">병오년(丙午年), 당신의 운명을 확인하세요.<br>(음력/양력/시간 정밀 분석)</div>', unsafe_allow_html=True)
st.write("---")

col_img, col_input = st.columns([1, 2])

with col_img:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=110)
    st.caption("2026 붉은 말의 해")

with col_input:
    name = st.text_input("성함", placeholder="예: 홍길동")
    
    # 1. 양력/음력 선택
    calendar_type = st.radio("생년월일 구분", ["양력", "음력"], horizontal=True)
    
    # 2. 날짜 입력
    if calendar_type == "양력":
        birth_date = st.date_input(
            "양력 생년월일",
            min_value=datetime(1930, 1, 1),
            max_value=datetime(2025, 12, 31),
            value=datetime(1975, 6, 15)
        )
        is_leap_month = False
        input_year = birth_date.year
        input_month = birth_date.month
        input_day = birth_date.day
        
    else: # 음력 (여기가 문제였던 부분입니다! 완벽하게 고쳤습니다)
        c1, c2, c3 = st.columns(3) # <-- 이 줄이 꼭 있어야 합니다!
        with c1:
            input_year = st.number_input("년(Year)", 1930, 2025, 1975)
        with c2:
            input_month = st.number_input("월(Month)", 1, 12, 1)
        with c3:
            input_day = st.number_input("일(Day)", 1, 30, 15)
        
        is_leap_month = st.checkbox("윤달(Leap Month) 입니까?")

    # 3. 태어난 시
    time_options = [
        "모름",
        "자시 (23:00 ~ 01:00)", "축시 (01:00 ~ 03:00)", "인시 (03:00 ~ 05:00)",
        "묘시 (05:00 ~ 07:00)", "진시 (07:00 ~ 09:00)", "사시 (09:00 ~ 11:00)",
        "오시 (11:00 ~ 13:00)", "미시 (13:00 ~ 15:00)", "신시 (15:00 ~ 17:00)",
        "유시 (17:00 ~ 19:00)", "술시 (19:00 ~ 21:00)", "해시 (21:00 ~ 23:00)"
    ]
    birth_time = st.selectbox("태어난 시 (선택)", time_options)

# --------------------------------------------------------------------------
# [4] 결과 출력
# --------------------------------------------------------------------------
if st.button("📜 2026년 무료 운세 보기", use_container_width=True):
    if df is None:
        st.error("⚠️ 데이터 파일(db.xlsx)이 없습니다.")
    elif not name:
        st.warning("성함을 입력해주세요.")
    else:
        with st.spinner('사주를 분석하고 점괘를 뽑는 중입니다...'):
            time.sleep(1.0)
            
            calendar = KoreanLunarCalendar()
            if calendar_type == "양력":
                calendar.setSolarDate(input_year, input_month, input_day)
                lunar_year = calendar.lunarYear
                lunar_month = calendar.lunarMonth
                lunar_day = calendar.lunarDay
                display_msg = f"양력 {input_year}.{input_month}.{input_day}"
            else:
                lunar_year = input_year
                lunar_month = input_month
                lunar_day = input_day
                leap_msg = "(윤달)" if is_leap_month else ""
                display_msg = f"음력 {input_year}.{input_month}.{input_day} {leap_msg}"
            
            age = 2026 - input_year + 1
            upper = (age + VAR_YEAR_NUM) % 8
            if upper == 0: upper = 8
            
            calc_month = lunar_month 
            if calc_month <= 12: m_const = MONTH_CONSTANTS[calc_month]
            else: m_const = 1
            
            middle = (calc_month + m_const) % 6
            if middle == 0: middle = 6
            
            lower = (lunar_day + 1) % 3
            if lower == 0: lower = 3
            
            final_code = f"{upper}{middle}{lower}"
            result_row = df[df['code'] == final_code]
            
            st.success(f"✅ {name}님 사주: [{display_msg}] / [{birth_time}]")
            
            if birth_time in TIME_LUCK: