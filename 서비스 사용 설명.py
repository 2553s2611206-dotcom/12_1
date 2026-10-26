
import json
import re
import streamlit as st
import streamlit.components.v1 as components

# ----------------------------------------------------
# 1. 페이지 기본 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------
# 2. 세션 상태 초기화
# ----------------------------------------------------
if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = 1.0

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

# ----------------------------------------------------
# 3. 안전한 브라우저 음성 안내
# ----------------------------------------------------
def speak_text(text, rate=1.0):
    """브라우저의 한국어 음성 합성 기능으로 안내한다."""
    safe_text = json.dumps(str(text), ensure_ascii=False)
    safe_rate = max(0.5, min(2.0, float(rate)))

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <script>
    (function() {{
        const message = {safe_text};
        const rate = {safe_rate};

        if (!("speechSynthesis" in window)) {{
            return;
        }}

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = "ko-KR";
        utterance.rate = rate;

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    </body>
    </html>
    """

    try:
        # 중요: components.html()에는 key 인자를 전달하지 않는다.
        components.html(
            html_content,
            height=1,
            scrolling=False,
        )
    except Exception:
        st.warning(
            "음성 안내를 실행하지 못했습니다. "
            "브라우저 설정을 확인해 주세요."
        )


# ----------------------------------------------------
# 4. 화면 디자인
# ----------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHorizontalBlock"] div.stButton > button {
        min-height: 72px;
        font-size: 22px !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        border: 3px solid #111111 !important;
    }

    .feature-card {
        background-color: #F0F4F8;
        border: 4px solid #111111;
        border-radius: 25px;
        padding: 30px;
        margin-top: 10px;
    }

    .single-main-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 30px 18px;
        margin: 20px 0;
        font-size: 25px;
        font-weight: 900;
        text-align: center;
        text-decoration: none;
        border-radius: 20px;
        border: 4px solid #000000;
    }

    .bg-step-1 {
        background-color: #FFD700;
        color: #000000 !important;
    }

    .bg-step-2 {
        background-color: #008A3E;
        color: #FFFFFF !important;
    }

    .bg-step-3 {
        background-color: #7000B8;
        color: #FFFFFF !important;
    }

    .status-box {
        background: #FFFFFF;
        border: 3px solid #123B64;
        border-radius: 15px;
        padding: 18px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 5. 제목
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")

st.markdown(
    f"""
    ### 🔊 현재 속도: {st.session_state.speech_rate:.2f}배
    ### 안내 단계: 기능 {st.session_state.current_step} / 3
    """
)

# ----------------------------------------------------
# 6. 음성 속도 조절
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button(
        "🐢 음성 느리게",
        key="slow_btn",
        use_container_width=True,
    ):
        st.session_state.speech_rate = max(
            0.5,
            round(st.session_state.speech_rate - 0.25, 2),
        )
        st.rerun()

with col_right:
    if st.button(
        "⚡ 음성 빠르게",
        key="fast_btn",
        use_container_width=True,
    ):
        st.session_state.speech_rate = min(
            2.0,
            round(st.session_state.speech_rate + 0.25, 2),
        )
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# 7. 기능별 안내 데이터
# ----------------------------------------------------
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 버스 번호 카메라 인식 및 음성 안내",
        "desc": (
            "버스 사진을 촬영하면 번호를 인식하고 "
            "음성으로 알려주는 기능입니다."
        ),
        "script": (
            "기능 1번 안내입니다. 버스 번호 카메라 인식 기능입니다. "
            "아래 버튼을 눌러 버스 번호 인식 페이지로 이동하세요."
        ),
        "link_text": "👉 기능 1: 버스 번호 인식 페이지",
        "link_url": "1번링크를 넣으시오",
        "bg_class": "bg-step-1",
    },
    2: {
        "title": "2️⃣ 기능 2: 버스 승하차 예약 알림",
        "desc": (
            "타려는 버스의 승차 의사를 전달하고 "
            "도착 안내를 제공하도록 설계한 기능입니다."
        ),
        "script": (
            "기능 2번 안내입니다. 버스 승하차 예약 알림 기능입니다. "
            "아래 버튼을 눌러 해당 페이지로 이동하세요."
        ),
        "link_text": "👉 기능 2: 승하차 예약 페이지",
        "link_url": "2번링크를 넣으시오",
        "bg_class": "bg-step-2",
    },
    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "desc": (
            "정류장 주변의 장애물이나 위험 요소를 "
            "알려주는 기능입니다."
        ),
        "script": (
            "기능 3번 안내입니다. 정류장 주변 위험 안내 기능입니다. "
            "아래 버튼을 눌러 해당 페이지로 이동하세요."
        ),
        "link_text": "👉 기능 3: 주변 위험 안내 페이지",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3",
    },
}

# 현재 단계의 유효성 확인
if st.session_state.current_step not in step_data:
    st.session_state.current_step = 1

step = st.session_state.current_step
current_info = step_data[step]

# ----------------------------------------------------
# 8. 현재 단계 설명
# ----------------------------------------------------
st.markdown("## 📋 현재 안내 기능")

st.markdown(
    f"""
    <div class="feature-card">
        <h2 style="font-size:28px;color:#111111;">
            {current_info["title"]}
        </h2>
        <p style="font-size:21px;color:#222222;font-weight:bold;">
            {current_info["desc"]}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 9. 기능 페이지 이동
# ----------------------------------------------------
link_url = current_info["link_url"]
link_text = current_info["link_text"]

# 주소가 실제 URL인지 확인
is_valid_url = bool(
    re.fullmatch(r"https?://[^\s<>\"']+", link_url)
)

if is_valid_url:
    st.markdown(
        f"""
        <a href="{link_url}" target="_blank"
           rel="noopener noreferrer"
           class="single-main-btn {current_info["bg_class"]}">
           {link_text}
        </a>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info(
        f"{link_text}\n\n"
        "아직 페이지 주소가 설정되지 않았습니다. "
        "실제 배포된 페이지 주소를 코드에 입력해 주세요."
    )

st.markdown("---")

# ----------------------------------------------------
# 10. 이전 / 음성 다시 듣기 / 다음
# ----------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    if st.button(
        "⬅️ 이전 안내",
        key="prev_btn",
        use_container_width=True,
    ):
        st.session_state.current_step = (
            3 if step == 1 else step - 1
        )
        st.rerun()

with col_ctrl2:
    if st.button(
        "🔊 음성 다시 듣기",
        key="replay_btn",
        use_container_width=True,
    ):
        speak_text(
            current_info["script"],
            st.session_state.speech_rate,
        )

with col_ctrl3:
    if st.button(
        "다음 안내 ➡️",
        key="next_btn",
        use_container_width=True,
    ):
        st.session_state.current_step = (
            1 if step == 3 else step + 1
        )
        st.rerun()

# ----------------------------------------------------
# 11. 안내 음성 자동 실행
# 단계가 바뀌었을 때만 자동 안내
# ----------------------------------------------------
if st.session_state.get("last_spoken_step") != step:
    st.session_state.last_spoken_step = step
    speak_text(
        current_info["script"],
        st.session_state.speech_rate,
    )

st.markdown("---")

st.caption(
    "시각장애인 버스 탑승 보조 안내 앱 | "
    "음성 안내는 브라우저 기능을 사용합니다."
)
