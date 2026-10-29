
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
if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = 1.0

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "auto_play" not in st.session_state:
    st.session_state.auto_play = True

# 앱 소개 음성 재생 여부
if "intro_played" not in st.session_state:
    st.session_state.intro_played = False

if "intro_just_started" not in st.session_state:
    st.session_state.intro_just_started = False


# 3. 음성 안내 함수
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


# 4. 앱 전체 소개 음성 내용
app_intro = (
    "안녕하세요. 시각장애인 버스 탑승 보조 시스템입니다. "
    "이 앱은 시각장애인이 버스를 더욱 편리하고 안전하게 이용할 수 있도록 "
    "도움을 주기 위해 만들어졌습니다. "
    "이 앱에는 크게 두 가지 기능이 있습니다. "
    "첫 번째 기능은 목적지 기반 버스 안내 기능입니다. "
    "가고 싶은 목적지를 입력하면 목적지에 맞는 버스 정보를 안내해 줍니다. "
    "두 번째 기능은 카메라를 이용한 버스 번호 인식 기능입니다. "
    "카메라로 버스를 비추면 버스 번호를 인식하여 어떤 버스인지 알려줍니다. "
    "화면 위쪽에는 음성 속도를 조절할 수 있는 버튼이 있습니다. "
    "음성 느리게 버튼을 누르면 안내 음성이 느려지고, "
    "음성 빠르게 버튼을 누르면 안내 음성이 빨라집니다. "
    "기능 1과 기능 2 버튼을 누르면 각각의 기능 페이지로 이동할 수 있습니다. "
    "화면 아래쪽의 이전 안내와 다음 안내 버튼을 누르면 "
    "기능 설명을 바꿔서 들을 수 있습니다. "
    "다시 듣기 버튼을 누르면 현재 기능에 대한 설명을 다시 들을 수 있습니다. "
    "이 앱을 이용하여 더욱 편리하게 버스를 이용하시기 바랍니다. "
    "감사합니다."
)


# 5. 전체 CSS 디자인
st.markdown(
    """
    <style>
    /* 전체 화면 */
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

    /* 음성 느리게: 파란색 */
    div.st-key-slow_btn button {
        background: #0055FF !important;
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        border: 5px solid #003399 !important;
    }

    /* 음성 빠르게: 빨간색 */
    div.st-key-fast_btn button {
        background: #FF0000 !important;
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border: 5px solid #990000 !important;
    }

    /* 앱 소개 카드 */
    .intro-card {
        background-color: #FFF8DC;
        border: 4px solid #8A6500;
        border-radius: 24px;
        padding: 25px;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }

    .intro-title {
        color: #000000;
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .intro-description {
        color: #111111;
        font-size: 22px;
        font-weight: 700;
        line-height: 1.8;
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
        color: #000000;
        font-size: 36px;
        font-weight: 900;
        line-height: 1.5;
        margin-bottom: 25px;
    }

    .feature-description {
        color: #111111;
        font-size: 25px;
        line-height: 1.8;
        font-weight: 700;
    }

    /* 기능 페이지 이동 버튼 공통 디자인 */
    div[data-testid="stPageLink"] a {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        min-height: 120px !important;
        box-sizing: border-box !important;
        padding: 24px !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        border: 5px solid #222222 !important;
        border-radius: 22px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        line-height: 1.5 !important;
        text-align: center !important;
        text-decoration: none !important;
        box-shadow: 0 6px 0 rgba(0, 0, 0, 0.35) !important;
    }

    /* 기능 페이지 버튼 내부 글자 */
    div[data-testid="stPageLink"] a p {
        font-size: 30px !important;
        font-weight: 900 !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }

    /* 하단 안내 버튼 */
    div.st-key-prev_btn button,
    div.st-key-replay_btn button,
    div.st-key-next_btn button {
        min-height: 80px !important;
        font-size: 23px !important;
        font-weight: 800 !important;
        border: 3px solid #222222 !important;
        border-radius: 15px !important;
    }

    /* 현재 안내 상태 */
    .status-text {
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        color: #111111;
        padding: 12px;
    }

    /* 모바일 화면 */
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

        .intro-title {
            font-size: 26px;
        }

        .intro-description {
            font-size: 19px;
        }

        div[data-testid="stPageLink"] a {
            min-height: 100px !important;
            padding: 18px !important;
            font-size: 23px !important;
        }

        div[data-testid="stPageLink"] a p {
            font-size: 23px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 6. 페이지 제목
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


# 7. 음성 속도 조절 버튼
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


# 8. 앱 소개 영역
st.markdown(
    """
    <div class="intro-card">
        <div class="intro-title">
            📢 앱 소개
        </div>
        <div class="intro-description">
            이 앱은 시각장애인의 편리하고 안전한 버스 탑승을
            돕기 위한 시스템입니다.<br>
            목적지 기반 버스 안내와 카메라를 이용한
            버스 번호 인식 기능을 제공합니다.<br>
            앱에 접속하면 전체적인 사용 방법을
            음성으로 자동 안내합니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("---")


# 9. 기능 1, 2 안내 데이터
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 목적지 기반 버스 안내",
        "description": (
            "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다."
        ),
        "script": (
            "기능 1번 안내입니다. "
            "목적지를 입력하면 가장 적합한 버스를 안내해 줍니다. "
            "기능 1 페이지로 이동하려면 기능 1 버튼을 눌러주세요."
        )
    },
    2: {
        "title": "2️⃣ 기능 2: 카메라를 이용한 버스 번호 인식",
        "description": (
            "카메라로 버스를 비추면 버스 번호를 인식하여 "
            "몇 번 버스인지 알려줍니다."
        ),
        "script": (
            "기능 2번 안내입니다. "
            "카메라로 버스를 비추면 버스 번호를 인식하여 "
            "몇 번 버스인지 알려줍니다. "
            "기능 2 페이지로 이동하려면 기능 2 버튼을 눌러주세요."
        )
    }
}


# 10. 현재 기능 표시
step = st.session_state.current_step

if step not in step_data:
    st.session_state.current_step = 1
    step = 1

current_info = step_data[step]


# 앱 첫 접속 시 앱 소개 + 기능 1 음성 자동 안내
if not st.session_state.intro_played:

    st.session_state.intro_played = True
    st.session_state.intro_just_started = True

    speak_text(
        app_intro + " " + current_info["script"],
        st.session_state.speech_rate
    )

else:
    # 앱 소개가 끝난 이후에는 기존 기능 안내 실행
    speak_text(
        current_info["script"],
        st.session_state.speech_rate
    )


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


# 11. 기능별 이동 버튼 색상
if step == 1:
    # 기능 1: 노란색 배경 + 검은색 글씨
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

        div[data-testid="stPageLink"] a:hover {
            background-color: #FFC400 !important;
            color: #000000 !important;
            border-color: #5C4300 !important;
        }

        div[data-testid="stPageLink"] a:hover p {
            color: #000000 !important;
        }

        div[data-testid="stPageLink"] a:focus-visible {
            outline: 5px solid #0057D9 !important;
            outline-offset: 5px !important;
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
    # 기능 2: 초록색 배경 + 흰색 글씨
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

        div[data-testid="stPageLink"] a:hover {
            background-color: #005C31 !important;
            color: #FFFFFF !important;
            border-color: #00351C !important;
        }

        div[data-testid="stPageLink"] a:hover p {
            color: #FFFFFF !important;
        }

        div[data-testid="stPageLink"] a:focus-visible {
            outline: 5px solid #FFB000 !important;
            outline-offset: 5px !important;
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


# 12. 이전 안내 / 다시 듣기 / 다음 안내
col_prev, col_replay, col_next = st.columns(3)

with col_prev:
    if st.button(
        "⬅️ 이전 안내",
        key="prev_btn",
        use_container_width=True
    ):
        st.session_state.current_step = (
            2 if st.session_state.current_step == 1 else 1
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
            2 if st.session_state.current_step == 1 else 1
        )
        st.rerun()


# 13. 자동 단계 전환: 기능 1 ↔ 기능 2
if st.session_state.auto_play:

    # 앱 소개 음성이 재생되는 첫 번째 구간은
    # 기존 12초 대신 60초 동안 기다림
    if st.session_state.intro_just_started:
        WAIT_TIME = 60
        st.session_state.intro_just_started = False
    else:
        WAIT_TIME = 12

    time.sleep(WAIT_TIME)

    if st.session_state.current_step == step:
        st.session_state.current_step = (
            2 if step == 1 else 1
        )
        st.rerun()
