import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (와이드 레이아웃 및 다크 테마 적용)
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 음성 속도 세션 상태 초기화
if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 1.0  # 기본 속도 (1.0x)

# 3. 브라우저 Web Speech API(TTS) 호출용 JavaScript 함수 정의
def speak_text(text, rate=1.0):
    js_code = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // 기존 재생 중인 음성 중단
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

# 4. 고대비 대형 버튼 및 UI 커스텀 CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 고대비 검은색 처리 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 상단 음성 속도 조절 버튼 (좌측: 파란색, 우측: 빨간색) */
    div.stButton > button[key="slow_btn"] {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: bold !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: 4px solid #FFFFFF !important;
    }
    
    div.stButton > button[key="fast_btn"] {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: bold !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: 4px solid #FFFFFF !important;
    }

    /* 다시 듣기 버튼 */
    div.stButton > button[key="replay_btn"] {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: bold !important;
        height: 70px !important;
        border-radius: 12px !important;
        border: 2px solid #888888 !important;
    }

    /* 가장 큰 기능 페이지 이동 대형 버튼 링크 스타일 */
    .main-feature-btn {
        display: block;
        width: 100%;
        padding: 35px 20px;
        margin: 20px 0;
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        text-decoration: none;
        border-radius: 25px;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 8px 15px rgba(255, 255, 255, 0.3);
        transition: all 0.2s ease-in-out;
    }
    
    /* 기능 1: 노란색 고대비 */
    .btn-feature-1 {
        background-color: #FFD700;
        color: #000000;
    }
    /* 기능 2: 연두색 고대비 */
    .btn-feature-2 {
        background-color: #00FF66;
        color: #000000;
    }
    /* 기능 3: 자홍색 고대비 */
    .btn-feature-3 {
        background-color: #FF00FF;
        color: #FFFFFF;
    }
    
    .main-feature-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.2);
    }
    
    /* 정보 안내 박스 */
    .info-card {
        background-color: #121212;
        border: 3px solid #444444;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# [앱 헤더 및 타이틀]
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")
st.markdown(f"### 🔊 현재 음성 안내 속도: **{st.session_state.speech_rate}x**")

# ----------------------------------------------------
# [요청사항 1: 상단 속도 조절 버튼 (좌: 파란색 느리게 / 우: 빨간색 빠르게)]
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🐢 음성 느리게 (Blue)", key="slow_btn", help="음성 안내 속도를 낮춥니다"):
        st.session_state.speech_rate = max(0.5, round(st.session_state.speech_rate - 0.25, 2))
        st.rerun()

with col_right:
    if st.button("⚡ 음성 빠르게 (Red)", key="fast_btn", help="음성 안내 속도를 높입니다"):
        st.session_state.speech_rate = min(2.0, round(st.session_state.speech_rate + 0.25, 2))
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# [요청사항 2: 앱 소개 및 각 기능 안내 음성 자동 재생]
# ----------------------------------------------------
intro_script = (
    f"안녕하세요. 시각장애인 버스 탑승 보조 안내 앱입니다. "
    f"이 앱은 접근하는 버스 번호를 확인하고 안전하게 탑승할 수 있도록 돕습니다. "
    f"아래에 위치한 대형 버튼을 눌러 주요 기능 페이지로 이동할 수 있습니다. "
    f"첫 번째, 버스 번호 카메라 인식 및 음성 안내 페이지. "
    f"두 번째, 버스 승하차 예약 및 도착 알림 페이지. "
    f"세 번째, 정류장 주변 위험 요소 안내 페이지입니다. "
    f"원하시는 기능의 대형 버튼을 선택해 주세요."
)

# 브라우저 진입 시 현재 설정된 속도로 음성 안내 실행
speak_text(intro_script, rate=st.session_state.speech_rate)

# 안내 음성 다시 듣기 버튼
if st.button("🔊 음성 안내 다시 듣기", key="replay_btn", use_container_width=True):
    speak_text(intro_script, rate=st.session_state.speech_rate)

st.markdown("---")

# ----------------------------------------------------
# [요청사항 3: 기능 페이지 설명 및 대형 이동 버튼]
# ----------------------------------------------------
st.markdown("## 📋 주요 기능 안내 및 이동")

# --- 기능 1 ---
card1_html = """
<div class="info-card">
    <h3>1️⃣ 기능 1: 버스 번호 카메라 인식 및 음성 안내</h3>
    <p>카메라로 다가오는 버스를 비추면 버스 번호를 자동으로 인식하여 음성으로 크게 알려줍니다.</p>
    <a href="1번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-1">
        👉 [기능 1] 버스 번호 인식 페이지로 이동
    </a>
</div>
"""
st.markdown(card1_html, unsafe_allow_html=True)

# --- 기능 2 ---
card2_html = """
<div class="info-card">
    <h3>2️⃣ 기능 2: 버스 승하차 예약 알림</h3>
    <p>타야 할 버스를 미리 선택하면 버스 기사님에게 승차 의사를 전달하고, 도착 시 진동과 음성으로 알려줍니다.</p>
    <a href="2번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-2">
        👉 [기능 2] 승하차 예약 페이지로 이동
    </a>
</div>
"""
st.markdown(card2_html, unsafe_allow_html=True)

# --- 기능 3 ---
card3_html = """
<div class="info-card">
    <h3>3️⃣ 기능 3: 정류장 주변 위험 안내</h3>
    <p>정류장 주변의 보도블록 상태, 벤치 위치, 위험 장애물을 실시간으로 감지하여 안전하게 대기하도록 돕습니다.</p>
    <a href="3번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-3">
        👉 [기능 3] 주변 위험 안내 페이지로 이동
    </a>
</div>
"""
st.markdown(card3_html, unsafe_allow_html=True)
