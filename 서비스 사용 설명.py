
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (와이드 레이아웃)
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

if 'is_first_load' not in st.session_state:
    st.session_state.is_first_load = True

# 3. 브라우저 Web Speech API(TTS) + 자동 다음 단계 전환 함수
def speak_and_auto_next(text, rate, wait_ms=12000):
    html_content = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();

                var msg = new SpeechSynthesisUtterance();
                msg.text = "{text}";
                msg.lang = 'ko-KR';
                msg.rate = {rate};

                var hasNavigated = false;

                function goToNext() {{
                    if (!hasNavigated) {{
                        hasNavigated = true;
                        window.parent.postMessage(
                            {{type: 'streamlit:rerun'}}, '*'
                        );
                    }}
                }}

                // 음성이 종료되면 12초 후 이동
                msg.onend = function() {{
                    setTimeout(goToNext, {wait_ms});
                }};

                // 재생 실패 대비 타이머
                setTimeout(goToNext, {wait_ms} + 8000);

                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(html_content, height=0, width=0)


# 4. 화면 CSS 스타일링
st.markdown("""
<style>
    /* 전체 화면 배경 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* =====================================
       음성 느리게 버튼 - 파란색
       버튼 key: slow_btn
       ===================================== */

    .st-key-slow_btn button {
        background-color: #0055FF !important;
        color: #FFFFFF !important;

        width: 100% !important;
        height: 140px !important;
        min-height: 140px !important;

        border-radius: 24px !important;
        border: 7px solid #002288 !important;

        box-shadow: 0 10px 22px rgba(0, 85, 255, 0.40) !important;
        transition: transform 0.2s ease-in-out !important;
    }

    .st-key-slow_btn button p,
    .st-key-slow_btn button div,
    .st-key-slow_btn button span {
        color: #FFFFFF !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
    }

    .st-key-slow_btn button:hover {
        background-color: #003FCC !important;
        border-color: #001766 !important;
        transform: scale(1.02);
    }


    /* =====================================
       음성 빠르게 버튼 - 빨간색
       버튼 key: fast_btn
       ===================================== */

    .st-key-fast_btn button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;

        width: 100% !important;
        height: 140px !important;
        min-height: 140px !important;

        border-radius: 24px !important;
        border: 7px solid #880000 !important;

        box-shadow: 0 10px 22px rgba(255, 0, 0, 0.40) !important;
        transition: transform 0.2s ease-in-out !important;
    }

    .st-key-fast_btn button p,
    .st-key-fast_btn button div,
    .st-key-fast_btn button span {
        color: #FFFFFF !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
    }

    .st-key-fast_btn button:hover {
        background-color: #CC0000 !important;
        border-color: #660000 !important;
        transform: scale(1.02);
    }


    /* 키보드로 버튼을 선택할 때 표시 */
    .st-key-slow_btn button:focus-visible,
    .st-key-fast_btn button:focus-visible {
        outline: 5px solid #000000 !important;
        outline-offset: 4px !important;
    }


    /* 메인 이동 대형 버튼 */
    .single-main-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 45px 20px;
        margin: 20px 0;
        font-size: 38px;
        font-weight: 900;
        line-height: 1.4;
        text-align: center;
        text-decoration: none;
        border-radius: 30px;
        border: 6px solid #000000;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease-in-out;
    }

    /* 단계별 고대비 색상 */
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

    /* 안내 박스 */
    .feature-card {
        background-color: #F0F4F8;
        border: 5px solid #111111;
        border-radius: 25px;
        padding: 30px;
        margin-top: 10px;
    }

    /* 하단 조작 버튼 */
    [data-testid="stHorizontalBlock"] button {
        min-height: 65px;
        font-size: 24px;
        font-weight: 900;
        border-radius: 15px;
    }

    /* 휴대전화 등 좁은 화면 */
    @media (max-width: 768px) {
        .st-key-slow_btn button,
        .st-key-fast_btn button {
            height: 110px !important;
            min-height: 110px !important;
            border-width: 5px !important;
            border-radius: 18px !important;
        }

        .st-key-slow_btn button p,
        .st-key-slow_btn button div,
        .st-key-slow_btn button span,
        .st-key-fast_btn button p,
        .st-key-fast_btn button div,
        .st-key-fast_btn button span {
            font-size: 25px !important;
        }

        .single-main-btn {
            font-size: 27px;
            padding: 30px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# 5. 단계 데이터 정의
# ----------------------------------------------------
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 경로 우선순위 탐색 안내",
        "desc": "목적지를 입력하면 어떤 경로가 가장 적합한지 알려줍니다.",
        "script": "기능 1번 안내입니다. 목적지를 입력하시면 가장 적합한 경로를 알려줍니다. 아래의 큰 버튼을 누르면 기능 1번 페이지로 이동합니다.",
        "link_text": "👉 [기능 1] 경로 우선순위 탐색",
        "link_url": "https://blindbus.streamlit.app/%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84",
        "bg_class": "bg-step-1"
    },
    2: {
        "title": "2️⃣ 기능 2: 버스 승하차 예약 알림",
        "desc": "타야 할 버스를 미리 선택하면 기사님에게 승차 의사를 전달하고 도착 시 알려줍니다.",
        "script": "기능 2번 안내입니다. 버스 승하차 예약을 돕는 기능입니다. 아래의 큰 버튼을 누르면 기능 2번 페이지로 이동합니다.",
        "link_text": "👉 [기능 2] 승하차 예약 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%B9%B4%EB%A9%94%EB%9D%BC_%EC%9D%B8%EC%8B%9D_%EC%8B%9C%EC%8A%A4%ED%85%9C",
        "bg_class": "bg-step-2"
    },
    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "desc": "정류장 주변의 보도블록, 벤치, 위험 장애물을 감지하여 안전하게 대기하도록 돕습니다.",
        "script": "마지막 기능 3번 안내입니다. 정류장 주변 위험 요소를 안내합니다. 아래의 큰 버튼을 누르면 기능 3번 페이지로 이동합니다.",
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3"
    }
}


# ----------------------------------------------------
# 6. 현재 단계 확인
# ----------------------------------------------------
step = st.session_state.current_step

if step not in step_data:
    step = 1
    st.session_state.current_step = 1

current_info = step_data[step]


# ----------------------------------------------------
# 7. 앱 타이틀 및 정보 표시
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")

st.markdown(
    f"### 🔊 현재 속도: **{st.session_state.speech_rate}x** "
    f"| 안내 단계: **기능 {step} / 3**"
)


# ----------------------------------------------------
# 8. 상단 속도 조절 버튼
#    왼쪽: 느리게(파란색)
#    오른쪽: 빠르게(빨간색)
# ----------------------------------------------------
col_left, col_right = st.columns(2, gap="large")

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


# ----------------------------------------------------
# 9. 오프닝 멘트 포함 음성 생성
# ----------------------------------------------------
if st.session_state.is_first_load:
    intro_text = (
        "안녕하세요, 지금부터 안내를 도와드릴 겁니다. "
        "안내를 듣고 원하는 기능이 나왔을 때 색깔이 있는 버튼을 눌러주세요. "
    )
    full_script = intro_text + current_info["script"]
    st.session_state.is_first_load = False
else:
    full_script = current_info["script"]


# ----------------------------------------------------
# 10. 현재 기능 설명 및 이동 링크
# ----------------------------------------------------
st.markdown("## 📋 현재 음성 설명 중인 기능")

card_html = f"""
<div class="feature-card">
    <h2 style="margin-top:0; font-size:32px;">
        {current_info['title']}
    </h2>

    <p style="font-size:22px; color:#222222; font-weight:bold;">
        {current_info['desc']}
    </p>

    <a href="{current_info['link_url']}"
       target="_blank"
       class="single-main-btn {current_info['bg_class']}">
        {current_info['link_text']}
    </a>
</div>
"""

st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")


# ----------------------------------------------------
# 11. 하단 컨트롤러: 이전 안내 및 다시 듣기
# ----------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

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
        speak_and_auto_next(
            full_script,
            st.session_state.speech_rate,
            wait_ms=12000
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
# 12. 다음 실행 시 적용할 단계
# ----------------------------------------------------
st.session_state.current_step = 1 if step == 3 else step + 1

# 음성 자동 실행 및 12초 후 화면 갱신
speak_and_auto_next(
    full_script,
    st.session_state.speech_rate,
    wait_ms=12000
)
