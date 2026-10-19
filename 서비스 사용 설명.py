import streamlit as st
import streamlit.components.v1 as components
import time

# 1. 페이지 기본 설정 (와이드 레이아웃 및 밝은 테마)
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 초기화 (음성 속도 및 현재 안내 단계)
if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 1.0  # 기본 속도 (1.0x)

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 기본 1단계(기능 1 안내)부터 시작

# 3. 브라우저 Web Speech API(TTS) 호출 함수
def speak_text(text, rate=1.0):
    js_code = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // 기존 재생 음성 중단
                var msg = new SpeechSynthesisUtterance();
                msg.text = `{text}`;
                msg.lang = 'ko-KR';
                msg.rate = {rate};
                window.speechSynthesis.speak(msg);
            }}
        }}
        speak();
    </script>
    """
    components.html(js_code, height=0, width=0)

# 4. 하얀색 배경 및 파랑/빨강/대형 가변 버튼 커스텀 CSS
st.markdown("""
<style>
    /* 1. 바탕화면 전체 하얀색으로 설정 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    /* 2. 좌측 상단 - 음성 느리게 버튼 (파란색) */
    div.stButton > button[key="slow_btn"] {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 85px !important;
        width: 100% !important;
        border-radius: 16px !important;
        border: 2px solid #0033AA !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 3. 우측 상단 - 음성 빠르게 버튼 (빨간색) */
    div.stButton > button[key="fast_btn"] {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 85px !important;
        width: 100% !important;
        border-radius: 16px !important;
        border: 2px solid #AA0000 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 4. 음성 다시듣기 및 단계 변경 보조 버튼 */
    div.stButton > button.sub-btn {
        background-color: #EFEFEF !important;
        color: #111111 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 55px !important;
        border-radius: 12px !important;
        border: 2px solid #CCCCCC !important;
    }

    /* 5. 하나만 위치하는 가장 큰 가변 이동 대형 버튼 */
    .single-main-btn {
        display: block;
        width: 100%;
        padding: 40px 20px;
        margin: 25px 0;
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        text-decoration: none;
        border-radius: 25px;
        border: 4px solid #000000;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out, filter 0.2s;
    }
    
    /* 단계별 개별 고대비 색상 적용 */
    .bg-step-1 { background-color: #FFD700; color: #000000; } /* 기능 1: 선명한 노란색 */
    .bg-step-2 { background-color: #00CC55; color: #FFFFFF; } /* 기능 2: 진한 연두색 */
    .bg-step-3 { background-color: #AA00FF; color: #FFFFFF; } /* 기능 3: 자홍색 */

    .single-main-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.1);
    }

    /* 안내 박스 스타일 */
    .feature-card {
        background-color: #F8F9FA;
        border: 3px solid #222222;
        border-radius: 20px;
        padding: 25px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# [앱 헤더 및 타이틀]
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")
st.markdown(f"**현재 음성 안내 속도:** `{st.session_state.speech_rate}x` | **현재 안내 단계:** `기능 {st.session_state.current_step} / 3`")

# ----------------------------------------------------
# [상단 속도 조절 버튼 (좌: 파란색 느리게 / 우: 빨간색 빠르게)]
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🐢 음성 느리게 (Blue)", key="slow_btn"):
        st.session_state.speech_rate = max(0.5, round(st.session_state.speech_rate - 0.25, 2))
        st.rerun()

with col_right:
    if st.button("⚡ 음성 빠르게 (Red)", key="fast_btn"):
        st.session_state.speech_rate = min(2.0, round(st.session_state.speech_rate + 0.25, 2))
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# [단계별 안내 데이터 정의]
# ----------------------------------------------------
step = st.session_state.current_step

step_data = {
    1: {
        "title": "1️⃣ 기능 1: 버스 번호 카메라 인식 및 음성 안내",
        "desc": "카메라로 다가오는 버스를 비추면 버스 번호를 자동으로 인식하여 음성으로 크게 알려줍니다.",
        "script": "안내입니다. 현재 기능 1번 페이지 안내 중입니다. 다가오는 버스 번호를 카메라로 인식해 알려줍니다. 아래의 큰 버튼을 누르면 기능 1번 페이지로 이동합니다.",
        "link_text": "👉 [기능 1] 버스 번호 인식 페이지로 이동하기",
        "link_url": "1번링크를 넣으시오",
        "bg_class": "bg-step-1"
    },
    2: {
        "title": "2️⃣ 기능 2: 버스 승하차 예약 알림",
        "desc": "타야 할 버스를 미리 선택하면 버스 기사님에게 승차 의사를 전달하고, 도착 시 진동과 음성으로 알려줍니다.",
        "script": "안내입니다. 현재 기능 2번 페이지 안내 중입니다. 버스 승하차 예약을 돕는 기능입니다. 아래의 큰 버튼을 누르면 기능 2번 페이지로 이동합니다.",
        "link_text": "👉 [기능 2] 승하차 예약 페이지로 이동하기",
        "link_url": "2번링크를 넣으시오",
        "bg_class": "bg-step-2"
    },
    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "desc": "정류장 주변의 보도블록 상태, 벤치 위치, 위험 장애물을 실시간으로 감지하여 안전하게 대기하도록 돕습니다.",
        "script": "안내입니다. 현재 기능 3번 페이지 안내 중입니다. 정류장 주변 장애물과 위험 요소를 안내합니다. 아래의 큰 버튼을 누르면 기능 3번 페이지로 이동합니다.",
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3"
    }
}

current_info = step_data[step]

# ----------------------------------------------------
# [앱 접속 및 단계 변경 시 자동 음성 재생]
# ----------------------------------------------------
speak_text(current_info["script"], rate=st.session_state.speech_rate)

# ----------------------------------------------------
# [중앙 단일 가변 대형 버튼 UI 구역]
# ----------------------------------------------------
st.markdown("## 📋 현재 안내 중인 기능")

# 카드 안내 영역
card_html = f"""
<div class="feature-card">
    <h2 style="margin-top:0;">{current_info['title']}</h2>
    <p style="font-size:20px; color:#333333;">{current_info['desc']}</p>
    <a href="{current_info['link_url']}" target="_blank" class="single-main-btn {current_info['bg_class']}">
        {current_info['link_text']}
    </a>
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# [하단 컨트롤러: 단계 이동 및 음성 제어]
# ----------------------------------------------------
col_prev, col_replay, col_next = st.columns([1, 1.5, 1])

with col_prev:
    if st.button("⬅️ 이전 기능 안내", use_container_width=True):
        st.session_state.current_step = 3 if step == 1 else step - 1
        st.rerun()

with col_replay:
    if st.button("🔊 음성 다시 듣기", use_container_width=True):
        speak_text(current_info["script"], rate=st.session_state.speech_rate)

with col_next:
    if st.button("다음 기능 안내 ➡️", use_container_width=True):
        st.session_state.current_step = 1 if step == 3 else step + 1
        st.rerun()
