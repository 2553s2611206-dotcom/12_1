import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (와이드 레이아웃)
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 음성 속도 세션 상태 초기화
if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 1.0  # 기본 속도

# 3. 브라우저 Web Speech API(TTS) 호출용 JavaScript 함수 정의
def speak_text(text, rate=1.0):
    # 크로스 브라우징 및 자바스크립트 스크립트 실행
    js_code = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // 기존 음성 중단
                var msg = new SpeechSynthesisUtterance();
                msg.text = `{text}`;
                msg.lang = 'ko-KR';
                msg.rate = {rate};
                window.speechSynthesis.speak(msg);
            }} else {{
                alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
            }}
        }}
        speak();
    </script>
    """
    components.html(js_code, height=0, width=0)

# 4. 고대비 대형 버튼 커스텀 CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 고대비 처리 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 상단 속도 조절 버튼 스타일 */
    div.stButton > button.btn-slow {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 80px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: 3px solid #FFFFFF !important;
    }
    
    div.stButton > button.btn-fast {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        height: 80px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: 3px solid #FFFFFF !important;
    }

    /* 가장 큰 기능 페이지 이동 링크 버튼 스타일 */
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
        box-shadow: 0px 8px 15px rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    .btn-feature-1 {
        background-color: #FFD700; /* 밝은 노란색 */
        color: #000000;
    }
    .btn-feature-2 {
        background-color: #00FF66; /* 밝은 연두색 */
        color: #000000;
    }
    .btn-feature-3 {
        background-color: #FF00FF; /* 네온 자홍색 */
        color: #FFFFFF;
    }
    .main-feature-btn:hover {
        transform: scale(1.02);
        filter: brightness(1.2);
    }
    
    /* 카드 및 안내 박스 */
    .info-card {
        background-color: #1A1A1A;
        border: 2px solid #555555;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_unsafe_html=True)

# ----------------------------------------------------
# [앱 헤더 및 타이틀]
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")
st.write(f"현재 음성 속도: **{st.session_state.speech_rate}x**")

# ----------------------------------------------------
# [요청사항 1: 상단 속도 조절 버튼 (좌: 느리게 / 우: 빠르게)]
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🐢 음성 느리게 (Blue)", key="slow_btn", help="음성 안내 속도를 줄입니다"):
        st.session_state.speech_rate = max(0.5, round(st.session_state.speech_rate - 0.25, 2))
        st.rerun()

with col_right:
    if st.button("⚡ 음성 빠르게 (Red)", key="fast_btn", help="음성 안내 속도를 늘립니다"):
        st.session_state.speech_rate = min(2.0, round(st.session_state.speech_rate + 0.25, 2))
        st.rerun()

# CSS 클래스 적용을 위한 스크립트 실행
components.html("""
<script>
    var buttons = window.parent.document.querySelectorAll('button');
    buttons.forEach(function(btn) {
        if (btn.innerText.includes('음성 느리게')) {
            btn.classList.add('btn-slow');
        } else if (btn.innerText.includes('음성 빠르게')) {
            btn.classList.add('btn-fast');
        }
    });
</script>
""", height=0)

st.markdown("---")

# ----------------------------------------------------
# [요청사항 2: 앱 소개 및 기능 설명 음성 재생]
# ----------------------------------------------------
intro_script = (
    f"안녕하세요. 시각장애인 버스 탑승 보조 앱입니다. "
    f"이 앱은 접근하는 버스 번호를 확인하고 안전하게 탑승할 수 있도록 돕습니다. "
    f"아래에 위치한 큰 버튼을 통해 3가지 주요 기능을 이용하실 수 있습니다. "
    f"첫 번째, 버스 번호 카메라 인식 및 음성 안내 기능. "
    f"두 번째, 버스 승하차 예약 및 알림 기능. "
    f"세 번째, 정류장 주변 장애물 및 안전 안내 기능입니다. "
    f"원하시는 기능의 대형 버튼을 눌러 이동해 주세요."
)

# 페이지 로드 시 설정된 속도로 자동으로 음성 안내 시작
speak_text(intro_script, rate=st.session_state.speech_rate)

# 음성 재요청 버튼
if st.button("🔊 음성 안내 다시 듣기", use_container_width=True):
    speak_text(intro_script, rate=st.session_state.speech_rate)

st.markdown("---")

# ----------------------------------------------------
# [요청사항 3: 기능 페이지 설명 및 가장 큰 이동 버튼]
# ----------------------------------------------------
st.subheader("📋 주요 기능 안내 및 이동")

# --- 기능 1 ---
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.markdown("### 1️⃣ 기능 1: 버스 번호 카메라 인식 및 음성 안내")
st.write("카메라로 다가오는 버스를 비추면 버스 번호를 자동으로 인식하여 음성으로 크게 알려줍니다.")
# 1번 링크 요청사항 반영 (가장 큰 대형 버튼)
st.markdown(
    '<a href="1번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-1">'
    '👉 [기능 1] 버스 번호 인식 페이지로 이동'
    '</a>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# --- 기능 2 ---
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.markdown("### 2️⃣ 기능 2: 버스 승하차 예약 알림")
st.write("타야 할 버스를 미리 선택하면 버스 기사님에게 승차 의사를 전달하고, 도착 시 진동과 음성으로 알려줍니다.")
# 2번 링크 요청사항 반영 (가장 큰 대형 버튼)
st.markdown(
    '<a href="2번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-2">'
    '👉 [기능 2] 승하차 예약 페이지로 이동'
    '</a>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# --- 기능 3 ---
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.markdown("### 3️⃣ 기능 3: 정류장 주변 위험 안내")
st.write("정류장 주변의 보도블록 상태, 벤치 위치, 위험 장애물을 실시간으로 감지하여 안전하게 대기하도록 돕습니다.")
# 3번 링크 요청사항 반영 (가장 큰 대형 버튼)
st.markdown(
    '<a href="3번링크를 넣으시오" target="_blank" class="main-feature-btn btn-feature-3">'
    '👉 [기능 3] 주변 위험 안내 페이지로 이동'
    '</a>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)
