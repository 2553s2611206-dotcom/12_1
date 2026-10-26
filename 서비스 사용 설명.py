
import streamlit as st
import streamlit.components.v1 as components
import time
import json

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 초기화
if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 1.0

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True

# 3. 브라우저 음성 안내 함수
def speak_text(text, rate):
    safe_text = json.dumps(text, ensure_ascii=False)

    html_content = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();

            var msg = new SpeechSynthesisUtterance({safe_text});
            msg.lang = 'ko-KR';
            msg.rate = {rate};

            window.speechSynthesis.speak(msg);
        }}
    </script>
    """

    components.html(html_content, height=0, width=0)

# 4. 화면 스타일
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 음성 느리게 버튼 - 파란색 */
    div[data-testid="stHorizontalBlock"]:has(
        button[key="slow_btn"]
    ) {
        width: 100%;
    }

    /* 상단 속도 조절 버튼 공통 스타일 */
    div[data-testid="stHorizontalBlock"]:has(
        button[key="slow_btn"]
    ) div[data-testid="column"] div.stButton > button {
        font-size: 38px !important;
        font-weight: 900 !important;
        height: 180px !important;
        width: 100% !important;
        border-radius: 25px !important;
    }

    /* 파란색 느리게 버튼 */
    div[data-testid="stHorizontalBlock"]:has(
        button[key="slow_btn"]
    ) div[data-testid="column"]:first-child div.stButton > button {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        border: 6px solid #002288 !important;
        box-shadow: 0px 10px 20px rgba(0, 85, 255, 0.4) !important;
    }

    /* 빨간색 빠르게 버튼 */
    div[data-testid="stHorizontalBlock"]:has(
        button[key="fast_btn"]
    ) div[data-testid="column"]:nth-child(2) div.stButton > button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border: 6px solid #880000 !important;
        box-shadow: 0px 10px 20px rgba(255, 0, 0, 0.4) !important;
    }

    .single-main-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 45px 20px;
        margin: 20px 0;
        font-size: 36px;
        font-weight: 900;
        text-align: center;
        text-decoration: none;
        border-radius: 30px;
        border: 5px solid #000000;
        box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease-in-out;
    }

    .bg-step-1 {
        background-color: #FFD700 !important;
        color: #000000 !important;
    }

    .bg-step-2 {
        background-color: #00CC55 !important;
        color: #FFFFFF !important;
    }

    .bg-step-3 {
        background-color: #AA00FF !important;
        color: #FFFFFF !important;
    }

    .single-main-btn:hover {
        transform: scale(1.02);
    }

    .feature-card {
        background-color: #F0F4F8;
        border: 4px solid #111111;
        border-radius: 25px;
        padding: 30px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 앱 타이틀 및 정보
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")

st.markdown(
    f"### 🔊 현재 속도: **{st.session_state.speech_rate}x** "
    f"| 안내 단계: **기능 {st.session_state.current_step} / 3**"
)

# ----------------------------------------------------
# 상단 음성 속도 조절 버튼
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🐢 음성 느리게", key="slow_btn"):
        st.session_state.speech_rate = max(
            0.5,
            round(st.session_state.speech_rate - 0.25, 2)
        )
        st.rerun()

with col_right:
    if st.button("⚡ 음성 빠르게", key="fast_btn"):
        st.session_state.speech_rate = min(
            2.0,
            round(st.session_state.speech_rate + 0.25, 2)
        )
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# 단계별 안내 정보
# ----------------------------------------------------
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 목적지 기반 버스 안내",
        "desc": "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다.",
        "script": (
            "기능 1번 안내입니다. "
            "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다. "
            "아래의 큰 버튼을 누르면 기능 1번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 1] 목적지 입력 및 버스 안내 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84",
        "bg_class": "bg-step-1"
    },

    2: {
        "title": "2️⃣ 기능 2: 카메라를 이용한 버스 번호 인식",
        "desc": "카메라로 버스를 비추면 버스 번호를 인식하여 몇 번 버스인지 알려줍니다.",
        "script": (
            "기능 2번 안내입니다. "
            "카메라로 버스를 비추면 버스 번호를 인식하여 "
            "몇 번 버스인지 알려줍니다. "
            "아래의 큰 버튼을 누르면 기능 2번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 2] 카메라 버스 번호 인식 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%B9%B4%EB%A9%94%EB%9D%BC_%EC%9D%B8%EC%8B%9D_%EC%8B%9C%EC%8A%A4%ED%85%9C",
        "bg_class": "bg-step-2"
    },

    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "desc": "정류장 주변의 보도블록, 벤치, 위험 장애물을 감지하여 안전하게 대기하도록 돕습니다.",
        "script": (
            "마지막 기능 3번 안내입니다. "
            "정류장 주변 위험 요소를 안내합니다. "
            "아래의 큰 버튼을 누르면 기능 3번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3"
    }
}

step = st.session_state.current_step
current_info = step_data[step]

# ----------------------------------------------------
# 음성 안내 실행
# ----------------------------------------------------
speak_text(
    current_info["script"],
    st.session_state.speech_rate
)

# ----------------------------------------------------
# 중앙 기능 설명 및 이동 버튼
# ----------------------------------------------------
st.markdown("## 📋 현재 음성 설명 중인 기능")

card_html = (
    '<div class="feature-card">'
    f'<h2 style="margin-top:0; font-size:32px;">'
    f'{current_info["title"]}</h2>'
    f'<p style="font-size:22px; color:#222222; font-weight:bold;">'
    f'{current_info["desc"]}</p>'
    f'<a href="{current_info["link_url"]}" '
    f'target="_blank" rel="noopener noreferrer" '
    f'class="single-main-btn {current_info["bg_class"]}">'
    f'{current_info["link_text"]}'
    '</a>'
    '</div>'
)

st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# 하단 컨트롤러
# ----------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    if st.button(
        "⬅️ 이전 안내",
        key="prev_btn",
        use_container_width=True
    ):
        st.session_state.current_step = 3 if step == 1 else step - 1
        st.rerun()

with col_ctrl2:
    if st.button(
        "🔊 음성 다시 듣기",
        key="replay_btn",
        use_container_width=True
    ):
        speak_text(
            current_info["script"],
            st.session_state.speech_rate
        )

with col_ctrl3:
    if st.button(
        "다음 안내 ➡️",
        key="next_btn",
        use_container_width=True
    ):
        st.session_state.current_step = 1 if step == 3 else step + 1
        st.rerun()

# ----------------------------------------------------
# 자동 다음 단계 전환
# ----------------------------------------------------
if st.session_state.auto_play:
    WAIT_TIME = 12
    time.sleep(WAIT_TIME)

    st.session_state.current_step = 1 if step == 3 else step + 1
    st.rerun()
