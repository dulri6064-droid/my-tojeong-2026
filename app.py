import streamlit as st
import pandas as pd
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime
import time

# --------------------------------------------------------------------------
# [1] 설정 및 데이터 준비
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 신년 운세",
    page_icon="🐎",
    layout="centered"
)

# 화면 디자인 (스타일)
st.markdown("""
    <style>
    .main-title { font-size: 3rem; color: #FF4B4B; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .sub-title { font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 30px; line-height: 1.5; }
    .result-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .month-text { font-size: 0.95rem; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# 토정비결 계산용 상수
VAR_YEAR_NUM = 1 
MONTH_CONSTANTS = [0, 2, 5, 3, 4, 1, 6, 2, 5, 3, 4, 1, 6] 

# [추가됨] 태어난 시에 따른 타고난 기질 데이터
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
# [2] 화면 구성 (입력란)
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🐎 2026 토정비결</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">병오년(丙午年), 당신의 운명을 확인하세요.<br>(음력/양력/시간 선택 가능)</div>', unsafe_allow_html=True)
st.write("---")

col_img, col_input = st.columns([1, 2])

with col_img:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.caption("붉은 말의 해")

with col_input:
    name = st.text_input("성함", placeholder="예: 홍길동")
    
    # 1. 양력/음력 선택 버튼
    calendar_type = st.radio("생년월일 구분", ["양력", "음력"], horizontal=True)
    
    # 2. 날짜 입력 (선택에 따라 다름)
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
        
    else: # 음력 선택 시 숫자 입력창이 나옴
        c1, c2, c3 = st.columns(3)
        with c1:
            input_year = st.number_input("년(Year)", 1930, 2025, 1975)
        with c2:
            input_month = st.number_input("월(Month)", 1, 12, 1)
        with c3:
            input_day = st.number_input("일(Day)", 1, 30, 15)
        
        is_leap_month = st.checkbox("윤달(Leap Month) 입니까?")

    # 3. 태어난 시 선택창
    time_options = [
        "모름",
        "자시 (23:00 ~ 01:00)", "축시 (01:00 ~ 03:00)", "인시 (03:00 ~ 05:00)",
        "묘시 (05:00 ~ 07:00)", "진시 (07:00 ~ 09:00)", "사시 (09:00 ~ 11:00)",
        "오시 (11:00 ~ 13:00)", "미시 (13:00 ~ 15:00)", "신시 (15:00 ~ 17:00)",
        "유시 (17:00 ~ 19:00)", "술시 (19:00 ~ 21:00)", "해시 (21:00 ~ 23:00)"
    ]
    birth_time = st.selectbox("태어난 시 (선택)", time_options)

# --------------------------------------------------------------------------
# [3] 운세 계산 및 결과 출력
# --------------------------------------------------------------------------
if st.button("📜 2026년 운세 풀이 보기", use_container_width=True):
    if df is None:
        st.error("⚠️ 데이터 파일(db.xlsx)이 없습니다.")
    elif not name:
        st.warning("성함을 입력해주세요.")
    else:
        with st.spinner('사주를 분석하고 점괘를 뽑는 중입니다...'):
            time.sleep(1.5)
            
            # (1) 음력/양력 변환 로직
            calendar = KoreanLunarCalendar()
            if calendar_type == "양력":
                calendar.setSolarDate(input_year, input_month, input_day)
                lunar_year = calendar.lunarYear
                lunar_month = calendar.lunarMonth
                lunar_day = calendar.lunarDay
                display_msg = f"양력 {input_year}년 {input_month}월 {input_day}일"
            else:
                lunar_year = input_year
                lunar_month = input_month
                lunar_day = input_day
                leap_msg = "(윤달)" if is_leap_month else ""
                display_msg = f"음력 {input_year}년 {input_month}월 {input_day}일 {leap_msg}"
            
            # (2) 토정비결 공식 계산
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
            
            # (3) 결과 화면 보여주기
            st.success(f"✅ {name}님의 사주 정보: [{display_msg}] / [{birth_time}]")
            
            # [여기가 추가된 부분!] 시간별 운세 보여주기
            if birth_time in TIME_LUCK:
                time_msg = TIME_LUCK[birth_time]
                st.info(f"🕰️ **[태어난 시 풀이]** {time_msg}")
            
            st.markdown("### 🔮 당신의 2026년 운세")
            
            if not result_row.empty:
                title = result_row.iloc[0]['title']
                content = result_row.iloc[0]['content']
                
                # 메인 결과
                st.markdown(f"""
                    <div class="result-box">
                        <h3>{title}</h3>
                        <p style="font-size:1.1rem; line-height:1.6;">{content}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # 월별 운세
                st.write("") 
                with st.expander("📅 2026년 월별 운세 흐름 (클릭)"):
                    st.info("※ 1년의 흐름을 파악하여 길흉화복을 대비하세요.")
                    try:
                        row_data = result_row.iloc[0]
                        m_col1, m_col2 = st.columns(2)
                        for i in range(1, 13):
                            month_text = row_data[f'month_{i}']
                            if i <= 6:
                                with m_col1:
                                    st.markdown(f"<div class='month-text'><b>{i}월:</b> {month_text}</div>", unsafe_allow_html=True)
                            else:
                                with m_col2:
                                    st.markdown(f"<div class='month-text'><b>{i}월:</b> {month_text}</div>", unsafe_allow_html=True)
                    except:
                        st.warning("⚠️ 월별 데이터가 준비되지 않았습니다.")
            else:
                st.error(f"결과를 찾을 수 없습니다. (코드: {final_code})")