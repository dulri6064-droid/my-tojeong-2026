import streamlit as st
import pandas as pd
from korean_lunar_calendar import KoreanLunarCalendar
from datetime import datetime
import time

# --------------------------------------------------------------------------
# [1] 설정 및 디자인 (꾸미기)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 신년 운세",
    page_icon="🐎",
    layout="centered"
)

# 깔끔한 스타일 적용 (CSS)
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    .disclaimer {
        font-size: 0.9rem;
        color: #888;
        font-weight: normal;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# [2] 2026년(병오년) 정통 로직 데이터
# --------------------------------------------------------------------------
VAR_YEAR_NUM = 1  # 2026년 태세수
MONTH_CONSTANTS = [0, 2, 5, 3, 4, 1, 6, 2, 5, 3, 4, 1, 6] 

# --------------------------------------------------------------------------
# [3] 데이터 불러오기
# --------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("db.xlsx", dtype={'code': str})
        return df
    except Exception as e:
        return None

df = load_data()

# --------------------------------------------------------------------------
# [4] 화면 구성 (UI)
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🐎 2026 토정비결</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="sub-title">
        병오년(丙午年), 당신의 운명을 미리 확인하세요.<br>
        <span class="disclaimer">(본 결과는 고전을 현대적 의미로 재해석 했음을 알려드립니다)</span>
    </div>
""", unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=150)
    st.caption("붉은 말의 해 (병오년)")

with col2:
    st.info("💡 생년월일은 **양력**으로 입력해주세요. 프로그램이 자동으로 음력으로 변환하여 분석합니다.")
    name = st.text_input("성함", placeholder="예: 홍길동")
    birth_date = st.date_input(
        "생년월일",
        min_value=datetime(1930, 1, 1),
        max_value=datetime(2025, 12, 31),
        value=datetime(1990, 1, 1)
    )

# --------------------------------------------------------------------------
# [5] 운세 계산 로직 (작괘)
# --------------------------------------------------------------------------
if st.button("📜 나의 2026년 운세 확인하기", use_container_width=True):
    if df is None:
        st.error("⚠️ 'db.xlsx' 파일이 폴더에 없습니다. 엑셀 파일을 확인해주세요.")
    elif not name:
        st.warning("성함을 입력해주세요.")
    else:
        with st.spinner('천기누설! 운세를 분석 중입니다...'):
            time.sleep(1.5)
            
            # 1. 양력 -> 음력 변환
            calendar = KoreanLunarCalendar()
            calendar.setSolarDate(birth_date.year, birth_date.month, birth_date.day)
            lunar_year = calendar.lunarYear
            lunar_month = calendar.lunarMonth
            lunar_day = calendar.lunarDay
            
            # 2. 나이 계산
            age = 2026 - birth_date.year + 1
            
            # 3. 토정비결 계산
            upper = (age + VAR_YEAR_NUM) % 8
            if upper == 0: upper = 8
            
            if lunar_month <= 12: m_const = MONTH_CONSTANTS[lunar_month]
            else: m_const = 1
            middle = (lunar_month + m_const) % 6
            if middle == 0: middle = 6
            
            lower = (lunar_day + 1) % 3
            if lower == 0: lower = 3
            
            final_code = f"{upper}{middle}{lower}"
            
            # 4. 결과 출력
            result_row = df[df['code'] == final_code]
            
            st.success(f"🎉 분석 완료! {name}님은 [음력 {lunar_month}월 {lunar_day}일]생으로 변환되었습니다.")
            st.markdown("### 🔮 당신의 2026년 점괘")
            
            if not result_row.empty:
                title = result_row.iloc[0]['title']
                content = result_row.iloc[0]['content']
                st.markdown(f"""
                    <div class="result-box">
                        <h3>{title}</h3>
                        <p style="font-size:1.1rem; line-height:1.6;">{content}</p>
                    </div>
                """, unsafe_allow_html=True)
                # 점괘 코드 출력 부분은 삭제했습니다.
            else:
                st.error(f"죄송합니다. 결과 코드 [{final_code}]에 해당하는 내용이 엑셀에 없습니다.")