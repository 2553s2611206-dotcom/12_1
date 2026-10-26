
import streamlit as st
import streamlit.components.v1 as components
import time
import json

st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = 1.0

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "auto_play" not in st.session_state:
    st.session_state.auto_play = True


# 음성 안내 함수
def speak_text(text, rate=1.0):
    safe_text = json.dumps(text, ensure_ascii=False)

    html_code = f"""
    <script>
    if ("speechSynthesis" in window) {{
        window.speechSynthesis.cancel();

        const msg = new SpeechSynthesisUtterance({safe_text});
        msg.lang = "ko-KR";
        msg.rate = {rate};

        window.speechSynthesis.speak(msg);
    }}
    </script>
    """

    components.html(html_code, height=0, width=0)


# CSS
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

    /* 음성 조절 버튼 공통 디자인 */
    div.st-key-slow_btn button,
    div.st-key-fast_btn button {
        width: 100% !important;
        min-height: 150px !important;
        height: 150px !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        border-radius: 22px !important;
        color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* 음성 느리게 버튼 - 파란색 */
    div.st-key-slow_btn button,
    div.st-key-slow_btn button[kind] {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        border: 5px solid #003399 !important;
    }

    /* 음성 빠르게 버튼 - 빨간색 */
    div.st-key-fast_btn button,
    div.st-key-fast_btn button[kind] {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border: 5px solid #990000 !important;
    }

    /* 기능 안내 카드 - 기존 디자인 유지 */
    .feature-card {
        background-color: #F5F8FF;
        border: 4px solid #222222;
        border-radius: 24px;
        padding: 35px;
        margin-top: 20px;
        margin-bottom: 25px;
        text-align: center;
    }

    .feature-title {
        color: #000000;
        font-size: 36px;
        font-weight: 900;
        margin-bottom: 25px;
    }

    .feature-description {
        color: #111111;
        font-size: 25px;
        line-height: 1.8;
        font-weight: 700;
        margin-bottom: 30px;
    }

    /* 기능 페이지 이동 버튼 - 기존 클래스 유지 */
    .single-main-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 25px 18px;
        border-radius: 18px;
        border: 4px solid #111111;
        text-align: center;
        font-size: 24px;
        font-weight: 900;
        text-decoration: none !important;
        color: #FFFFFF !important;
        line-height: 1.5;
    }

    .single-main-btn:hover {
        filter: brightness(0.9);
        color: #FFFFFF !important;
    }

    .bg-step-1 {
        background-color: #0055CC;
    }

    .bg-step-2 {
        background-color: #008044;
    }

    .bg-step-3 {
        background-color: #B00020;
    }

    /* 하단 이전/다시 듣기/다음 버튼 */
    div.st-key-prev_btn button,
    div.st-key-replay_btn button,
    div.st-key-next_btn button {
        min-height: 80px !important;
        font-size: 23px !important;
        font-weight: 800 !important;
        border: 3px solid #222222 !important;
        border-radius: 15px !important;
    }

    .status-text {
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        color: #111111;
        padding: 12px;
    }

    @media (max-width: 768px) {
        div.st-key-slow_btn button,
        div.st-key-fast_btn button {
            font-size: 24px !important;
            min-height: 120px !important;
            height: 120px !important;
        }

        .feature-title {
            font-size: 28px;
        }

        .feature-description {
            font-size: 21px;
        }

        .single-main-btn {
            font-size: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 페이지 제목
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


# 음성 속도 조절 버튼
col_left, col_right = st.columns(2)

with col_left:
    if st.button(
        "🐢 음성 느리게",
        key="slow_btn",
        use_container_width=True
    ):
        st.session_state.speech_rate = max(
            0.5,
            round(st.session_state.speech_rate - 0.25, 2)
        )
        st.rerun()

with col_right:
    if st.button(
        "⚡ 음성 빠르게",
        key="fast_btn",
        use_container_width=True
    ):
        st.session_state.speech_rate = min(
            2.0,
            round(st.session_state.speech_rate + 0.25, 2)
        )
        st.rerun()


st.markdown("---")


# 기능 안내 데이터
# 기능 페이지로 연결되는 링크와 버튼 문구를 유지
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 목적지 기반 버스 안내",
        "description": "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다.",
        "script": (
            "기능 1번 안내입니다. 목적지를 입력하면 "
            "가장 적합한 버스를 안내해 줍니다. "
            "아래 버튼을 누르면 기능 1번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 1] 목적지 입력 및 버스 안내 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84",
        "bg_class": "bg-step-1"
    },
    2: {
        "title": "2️⃣ 기능 2: 카메라를 이용한 버스 번호 인식",
        "description": "카메라로 버스를 비추면 버스 번호를 인식하여 몇 번 버스인지 알려줍니다.",
        "script": (
            "기능 2번 안내입니다. 카메라로 버스를 비추면 "
            "버스 번호를 인식하여 몇 번 버스인지 알려줍니다. "
            "아래 버튼을 누르면 기능 2번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 2] 카메라 버스 번호 인식 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%B9%B4%EB%A9%94%EB%9D%BC_%EC%9D%B8%EC%8B%9D_%EC%8B%9C%EC%8A%A4%ED%85%9C",
        "bg_class": "bg-step-2"
    },
    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "description": "정류장 주변의 보도블록, 벤치, 위험 장애물을 감지하여 안전하게 대기하도록 돕습니다.",
        "script": (
            "기능 3번 안내입니다. 정류장 주변 위험 요소를 안내합니다. "
            "아래 버튼을 누르면 기능 3번 페이지로 이동합니다."
        ),
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3"
    }
}


# 현재 기능 표시 및 음성 안내
step = st.session_state.current_step
current_info = step_data[step]

speak_text(
    current_info["script"],
    st.session_state.speech_rate
)

# 기능 페이지 버튼은 기존 HTML 링크 형식으로 유지
st.markdown(
    f"""
    <div class="feature-card">
        <div class="feature-title">
            {current_info["title"]}
        </div>

        <div class="feature-description">
            {current_info["description"]}
        </div>

        <a
            href="{current_info["link_url"]}"
            target="_blank"
            rel="noopener noreferrer"
            class="single-main-btn {current_info["bg_class"]}"
        >
            {current_info["link_text"]}
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# 이전 안내 / 다시 듣기 / 다음 안내
col_prev, col_replay, col_next = st.columns(3)

with col_prev:
    if st.button(
        "⬅️ 이전 안내",
        key="prev_btn",
        use_container_width=True
    ):
        st.session_state.current_step = (
            3 if st.session_state.current_step == 1
            else st.session_state.current_step - 1
        )
        st.rerun()

with col_replay:
    if st.button(
        "🔊 다시 듣기",
        key="replay_btn",
        use_container_width=True
    ):
        speak_text(
            current_info["script"],
            st.session_state.speech_rate
        )

with col_next:
    if st.button(
        "다음 안내 ➡️",
        key="next_btn",
        use_container_width=True
    ):
        st.session_state.current_step = (
            1 if st.session_state.current_step == 3
            else st.session_state.current_step + 1
        )
        st.rerun()


# 자동 단계 전환
if st.session_state.auto_play:
    WAIT_TIME = 12
    time.sleep(WAIT_TIME)

    if st.session_state.current_step == step:
        st.session_state.current_step = (
            1 if step == 3 else step + 1
        )
        st.rerun()
