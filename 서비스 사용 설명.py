import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (와이드 레이아웃 및 하얀색 배경 기본 설정)
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 초기화
if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 1.0  # 기본 속도

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1단계부터 시작

if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True  # 자동 연속 음성 안내 기본 활성화

# 3. 브라우저 Web Speech API(TTS) 호출 함수
def speak_text(text, rate=1.0):
    js_code = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // 이전 음성 중단
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

# 4. 강제 스타일링 CSS (하얀 배경, 매우 큰 파란색/빨간색 버튼)
st.markdown("""
<style>
    /* 1. 전체 화면 배경 하얀색 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 2. 좌측 상단 - 음성 느리게 버튼 (강제 파란색 & 초대형 크기) */
    button[data-testid="baseButton-secondary"]:has(div:contains("음성 느리게")),
    div.stButton > button:first-child {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        height: 120px !important;
        width: 100% !important;
        border-radius: 20px !important;
        border: 4px solid #002288 !important;
        box-shadow: 0px 8px 15px rgba(0, 85, 255, 0.4) !important;
    }

    /* 3. 우측 상단 - 음성 빠르게 버튼 (강제 빨간색 & 초대형 크기) */
    button[data-testid="baseButton-secondary"]:has(div:contains("음성 빠르게")) {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        height: 120px !important;
        width: 100% !important;
        border-radius: 20px !important;
        border: 4px solid #880000 !important;
        box-shadow: 0px 8px 15px rgba(255, 0, 0, 0.4) !important;
    }

    /* 4. 음성 설명에 맞춰 바뀌는 가장 큰 단일 이동 버튼 */
    .single-main-btn {
        display: block;
        width: 100%;
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
    
    /* 단계별 고대비 색상 */
    .bg-step-1 { background-color: #FFD700 !important; color: #000000 !important; } /* 기능 1: 노란색 */
    .bg-step-2 { background-color: #00CC55 !important; color: #FFFFFF !important; } /* 기능 2: 연두색 */
    .bg-step-3 { background-color: #AA00FF !important; color: #FFFFFF !important; } /* 기능 3: 자홍색 */

    .single-main-btn:hover {
        transform: scale(1.02);
    }

    /* 안내 박스 스타일 */
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
# [앱 타이틀 및 정보 표시]
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")
st.markdown(f"### 🔊 현재 속도: **{st.session_state.speech_rate}x** | 안내 단계: **기능 {st.session_state.current_step} / 3**")

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
# [단계별 안내 정보 정의]
# ----------------------------------------------------
step = st.session_state.current_step

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
        "script": "기능 3번 안내입니다. 정류장 주변 위험 요소를 안내합니다. 아래의 큰 버튼을 누르면 기능 3번 페이지로 이동합니다.",
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3"
    }
}

current_info = step_data[step]

# ----------------------------------------------------
# [음성 안내 실행]
# ----------------------------------------------------
speak_text(current_info["script"], rate=st.session_state.speech_rate)

# ----------------------------------------------------
# [중앙 메인 가변 대형 버튼 UI]
# ----------------------------------------------------
st.markdown("## 📋 현재 음성 설명 중인 기능")

card_html = f"""
<div class="feature-card">
    <h2 style="margin-top:0; font-size:32px;">{current_info['title']}</h2>
    <p style="font-size:22px; color:#222222; font-weight:bold;">{current_info['desc']}</p>
    <a href="{current_info['link_url']}" target="_blank" class="single-main-btn {current_info['bg_class']}">
        {current_info['link_text']}
    </a>
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# [연속 음성 안내 제어 및 순환 처리]
# ----------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
    if st.button("⬅️ 이전 안내", use_container_width=True):
        st.session_state.current_step = 3 if step == 1 else step - 1
        st.rerun()

with col_ctrl2:
    toggle_text = "⏸️ 자동 연속 안내 멈춤" if st.session_state.auto_play else "▶️ 자동 연속 안내 시작"
    if st.button(toggle_text, use_container_width=True):
        st.session_state.auto_play = not st.session_state.auto_play
        st.rerun()

with col_ctrl3:
    if st.button("다음 안내 ➡️", use_container_width=True):
        st.session_state.current_step = 1 if step == 3 else step + 1
        st.rerun()

# 자동 연속 재생이 활성화되어 있을 경우 음성이 끝나는 타이밍에 맞춰 다음 단계로 자동 전환
if st.session_state.auto_play:
    # 속도에 비례하여 다음 단계 전환 시간 자동 계산 (기본 약 6.5초)
    wait_time = int(6500 / st.session_state.speech_rate)
    
    components.html(f"""
    <script>
        setTimeout(function() {{
            window.parent.postMessage({{type: 'streamlit:render'}, '*');
            // 부모 창 새로고침으로 다음 안내 단계 이동
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {{
                if (buttons[i].innerText.includes("다음 안내")) {{
                    buttons[i].click();
                    break;
                }}
            }}
        }}, {wait_time});
    </script>
    """, height=0)
