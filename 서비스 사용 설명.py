
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

if "is_first_load" not in st.session_state:
    st.session_state.is_first_load = True

# 3. 브라우저 음성 안내 함수
def speak_and_auto_next(text, rate, wait_ms=12000):
    safe_text = json.dumps(text, ensure_ascii=False)

    html_content = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();

                var msg = new SpeechSynthesisUtterance({safe_text});
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

                msg.onend = function() {{
                    setTimeout(goToNext, {wait_ms});
                }};

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
    /* 전체 배경 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 상단 버튼 공통 스타일 */
    [data-testid="column"] button {
        height: 280px !important;
        min-height: 280px !important;
        width: 100% !important;
        border-radius: 35px !important;
        border-width: 10px !important;
        border-style: solid !important;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.28) !important;
        transition: transform 0.15s ease-in-out !important;
    }

    /* 버튼 글씨 크게 */
    [data-testid="column"] button p,
    [data-testid="column"] button div,
    [data-testid="column"] button span {
        font-size: 52px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
    }

    /* 왼쪽: 빠르게 - 빨간색 */
    [data-testid="column"]:nth-child(1) button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border-color: #880000 !important;
    }

    [data-testid="column"]:nth-child(1) button p,
    [data-testid="column"]:nth-child(1) button div,
    [data-testid="column"]:nth-child(1) button span {
        color: #FFFFFF !important;
    }

    /* 오른쪽: 느리게 - 파란색 */
    [data-testid="column"]:nth-child(2) button {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        border-color: #002288 !important;
    }

    [data-testid="column"]:nth-child(2) button p,
    [data-testid="column"]:nth-child(2) button div,
    [data-testid="column"]:nth-child(2) button span {
        color: #FFFFFF !important;
    }

    /* 마우스 올리기 효과 */
    [data-testid="column"] button:hover {
        filter: brightness(1.12);
        transform: scale(1.02);
    }

    /* 중앙 메인 이동 버튼 */
    .single-main-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 48px 24px;
        margin: 24px 0;
        font-size: 42px;
        font-weight: 900;
        line-height: 1.4;
        text-align: center;
        text-decoration: none !important;
        border-radius: 30px;
        border: 7px solid #000000;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease-in-out;
    }

    .bg-step-1 {
        background-color: #FFD700 !important;
        color: #000000 !important;
    }

    .bg-step-2 {
        background-color: #00AA44 !important;
        color: #FFFFFF !important;
    }

    .bg-step-3 {
        background-color: #8800DD !important;
        color: #FFFFFF !important;
    }

    .single-main-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.08);
    }

    /* 안내 정보 카드 */
    .feature-card {
        background-color: #F0F4F8;
        border: 5px solid #111111;
        border-radius: 25px;
        padding: 30px;
        margin-top: 10px;
    }

    /* 하단 컨트롤 버튼도 크게 */
    [data-testid="stHorizontalBlock"] button {
        min-height: 85px;
        font-size: 28px !important;
        font-weight: 900 !important;
        border: 4px solid #222222 !important;
        border-radius: 18px !important;
    }

    /* 작은 화면에서도 글씨가 잘 보이도록 */
    @media (max-width: 768px) {
        [data-testid="column"] button {
            height: 180px !important;
            min-height: 180px !important;
        }

        [data-testid="column"] button p,
        [data-testid="column"] button div,
        [data-testid="column"] button span {
            font-size: 30px !important;
        }

        .single-main-btn {
            font-size: 27px;
            padding: 30px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 단계별 데이터
# ----------------------------------------------------
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 버스 번호 카메라 인식 및 음성 안내",
        "desc": "카메라로 다가오는 버스를 비추면 버스 번호를 자동으로 인식하여 음성으로 알려줍니다.",
        "script": "기능 1번 안내입니다. 다가오는 버스 번호를 카메라로 인식합니다. 아래의 큰 버튼을 누르면 기능 1번 페이지로 이동합니다.",
        "link_text": "👉 [기능 1] 버스 번호 인식 페이지로 이동하기",
        "link_url": "1번링크를 넣으시오",
        "bg_class": "bg-step-1"
    },
    2: {
        "title": "2️⃣ 기능 2: 버스 승하차 예약 알림",
        "desc": "타야 할 버스를 미리 선택하면 기사님에게 승차 의사를 전달하고 도착 시 알려줍니다.",
        "script": "기능 2번 안내입니다. 버스 승하차 예약을 돕는 기능입니다. 아래의 큰 버튼을 누르면 기능 2번 페이지로 이동합니다.",
        "link_text": "👉 [기능 2] 승하차 예약 페이지로 이동하기",
        "link_url": "2번링크를 넣으시오",
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
# 7. 앱 타이틀 및 정보
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")

st.markdown(
    f"### 🔊 현재 속도: **{st.session_state.speech_rate}x** "
    f"| 안내 단계: **기능 {step} / 3**"
)

# ----------------------------------------------------
# 8. 상단 속도 조절 버튼
#    왼쪽: 빠르게(빨간색)
#    오른쪽: 느리게(파란색)
# ----------------------------------------------------
col_fast, col_slow = st.columns(2)

with col_fast:
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

with col_slow:
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

st.markdown("---")

# ----------------------------------------------------
# 9. 첫 실행 오프닝 멘트
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
    <h2 style="margin-top:0; font-size:36px; color:#000000;">
        {current_info['title']}
    </h2>

    <p style="
        font-size:28px;
        color:#222222;
        font-weight:bold;
        line-height:1.6;
    ">
        {current_info['desc']}
    </p>

    <a href="{current_info['link_url']}"
       target="_blank"
       rel="noopener noreferrer"
       class="single-main-btn {current_info['bg_class']}">
        {current_info['link_text']}
    </a>
</div>
"""

st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# 11. 하단 조작 버튼
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
# 12. 자동 단계 전환
# ----------------------------------------------------
# 자동 전환을 위한 별도의 브라우저 타이머는
# 아래 음성 안내 함수에서 실행됩니다.
# 단계는 다음 Streamlit 실행에서 갱신됩니다.

speak_and_auto_next(
    full_script,
    st.session_state.speech_rate,
    wait_ms=12000
)
