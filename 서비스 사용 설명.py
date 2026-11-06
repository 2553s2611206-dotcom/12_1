import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 초기화
if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = 1.0

if "current_step" not in st.session_state:
    st.session_state.current_step = 1


# 3. 음성 안내 함수 (브라우저 자바스크립트 TTS 호출)
def speak_text(text, rate=1.0):
    safe_text = json.dumps(text, ensure_ascii=False)

    html_code = f"""
    <script>
    if ("speechSynthesis" in window) {{
        const synth = window.speechSynthesis;
        synth.cancel();

        const msg = new SpeechSynthesisUtterance({safe_text});
        msg.lang = "ko-KR";
        msg.rate = {rate};

        synth.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=0, width=0)


# 4. 안내 멘트 정의
app_usage_text = (
    "앱 사용법을 안내합니다. "
    "음성이 너무 느리면 파란색 버튼을, 빠르면 빨간색 버튼을 눌러주세요. "
    "이제 두 가지 기능을 소개합니다. 설명에 맞게 아래의 색깔 버튼을 눌러주세요."
)

step_data = {
    1: {
        "title": "1️⃣ 기능 1: 목적지 기반 버스 안내",
        "description": "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다.",
        "script": "기능 1번 안내입니다. 목적지를 입력하면 가장 적합한 버스를 안내해 줍니다. 기능 1 페이지로 이동하려면 노란색 기능 1 버튼을 눌러주세요."
    },
    2: {
        "title": "2️⃣ 기능 2: 카메라를 이용한 버스 번호 인식",
        "description": "카메라로 버스를 비추면 버스 번호를 인식하여 몇 번 버스인지 알려줍니다.",
        "script": "기능 2번 안내입니다. 카메라로 버스를 비추면 버스 번호를 인식하여 몇 번 버스인지 알려줍니다. 기능 2 페이지로 이동하려면 초록색 기능 2 버튼을 눌러주세요."
    }
}


# 5. 전체 CSS 디자인
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    h1, h2, h3, p {
        color: #000000;
    }
    /* 음성 조절 버튼 디자인 */
    div.st-key-slow_btn button,
    div.st-key-fast_btn button {
        width: 100% !important;
        min-height: 140px !important;
        height: 140px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        border-radius: 22px !important;
        color: #FFFFFF !important;
    }
    div.st-key-slow_btn button {
        background: #0055FF !important;
        border: 5px solid #003399 !important;
    }
    div.st-key-fast_btn button {
        background: #FF0000 !important;
        border: 5px solid #990000 !important;
    }
    /* 상단 안내 버튼들 */
    div.st-key-usage_btn button {
        background: #7B2CBF !important;
        color: white !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        min-height: 75px !important;
        border-radius: 20px !important;
        border: 5px solid #4A148C !important;
    }
    div.st-key-feat1_btn button, div.st-key-feat2_btn button {
        font-size: 22px !important;
        font-weight: 800 !important;
        min-height: 60px !important;
        border-radius: 15px !important;
    }
    /* 기능 설명 카드 */
    .feature-card {
        background-color: #F5F8FF;
        border: 4px solid #222222;
        border-radius: 24px;
        padding: 35px;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .feature-title {
        font-size: 36px;
        font-weight: 900;
        margin-bottom: 25px;
    }
    .feature-description {
        font-size: 25px;
        line-height: 1.8;
        font-weight: 700;
    }
    /* 페이지 이동 버튼 */
    div[data-testid="stPageLink"] a {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        min-height: 120px !important;
        padding: 24px !important;
        border: 5px solid #222222 !important;
        border-radius: 22px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        text-decoration: none !important;
    }
    div[data-testid="stPageLink"] a p {
        font-size: 30px !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
    .status-text {
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 6. 페이지 제목 및 상태 표시
st.title("🚌 시각장애인 버스 탑승 보조 시스템")

st.markdown(
    f"""
    <div class="status-text">
        현재 음성 속도: {st.session_state.speech_rate:.2f}배속
       　|　
        현재 안내 단계: {st.session_state.current_step}단계
    </div>
    """,
    unsafe_allow_html=True
)


# 7. 상단 음성 안내 버튼들 (앱 사용법 / 기능 1 / 기능 2)
if st.button("🔊 앱 사용법 듣기", key="usage_btn", use_container_width=True):
    speak_text(app_usage_text, st.session_state.speech_rate)

col_f1, col_f2 = st.columns(2)
with col_f1:
    if st.button("📢 기능 1 안내 듣기", key="feat1_btn", use_container_width=True):
        speak_text(step_data[1]["script"], st.session_state.speech_rate)
with col_f2:
    if st.button("📢 기능 2 안내 듣기", key="feat2_btn", use_container_width=True):
        speak_text(step_data[2]["script"], st.session_state.speech_rate)


# 8. 음성 속도 조절 버튼 (파란색: 느리게, 빨간색: 빠르게)
col_slow, col_fast = st.columns(2)

with col_slow:
    if st.button("🐢 음성 느리게", key="slow_btn", use_container_width=True):
        st.session_state.speech_rate = max(0.5, round(st.session_state.speech_rate - 0.25, 2))
        st.rerun()

with col_fast:
    if st.button("⚡ 음성 빠르게", key="fast_btn", use_container_width=True):
        st.session_state.speech_rate = min(2.0, round(st.session_state.speech_rate + 0.25, 2))
        st.rerun()


st.markdown("---")


# 9. 현재 단계별 카드 및 페이지 링크 출력
step = st.session_state.current_step
current_info = step_data[step]

# 기능 설명 카드
st.markdown(
    f"""
    <div class="feature-card">
        <div class="feature-title">
            {current_info["title"]}
        </div>
        <div class="feature-description">
            {current_info["description"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 기능별 이동 버튼 색상 설정 및 링크
if step == 1:
    st.markdown(
        """
        <style>
        div[data-testid="stPageLink"] a {
            background-color: #FFD600 !important;
            color: #000000 !important;
            border-color: #8A6500 !important;
        }
        div[data-testid="stPageLink"] a p {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.page_link(
        "pages/우선순위.py",
        label="기능 1: 목적지 입력 및 버스 안내 페이지로 이동하기",
        icon="🚌",
        use_container_width=True
    )
else:
    st.markdown(
        """
        <style>
        div[data-testid="stPageLink"] a {
            background-color: #008044 !important;
            color: #FFFFFF !important;
            border-color: #004D2A !important;
        }
        div[data-testid="stPageLink"] a p {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.page_link(
        "pages/카메라 인식 시스템.py",
        label="기능 2: 카메라 버스 번호 인식 페이지로 이동하기",
        icon="📷",
        use_container_width=True
    )


# 10. 하단 제어 버튼 (이전 안내 / 다시 듣기 / 다음 안내)
col_prev, col_replay, col_next = st.columns(3)

with col_prev:
    if st.button("⬅️ 이전 안내", key="prev_btn", use_container_width=True):
        st.session_state.current_step = 2 if st.session_state.current_step == 1 else 1
        speak_text(step_data[st.session_state.current_step]["script"], st.session_state.speech_rate)
        st.rerun()

with col_replay:
    if st.button("🔊 다시 듣기", key="replay_btn", use_container_width=True):
        speak_text(current_info["script"], st.session_state.speech_rate)

with col_next:
    if st.button("다음 안내 ➡️", key="next_btn", use_container_width=True):
        st.session_state.current_step = 2 if st.session_state.current_step == 1 else 1
        speak_text(step_data[st.session_state.current_step]["script"], st.session_state.speech_rate)
        st.rerun()
