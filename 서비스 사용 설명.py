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
    st.session_state.speech_rate = 1.0  # 기본 속도 (1.0x)

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1단계부터 시작

if 'is_first_load' not in st.session_state:
    st.session_state.is_first_load = True  # 앱 첫 실행 여부

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
                        window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
                    }}
                }}

                // 음성이 정상 종료된 후 지정된 시간(12초) 뒤 이동
                msg.onend = function() {{
                    setTimeout(goToNext, {wait_ms});
                }};

                // 재생 실패 대비 안전 타이머
                setTimeout(goToNext, {wait_ms} + 8000);

                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    components.html(html_content, height=0, width=0)

# 4. 화면 CSS 스타일링 (초고대비 대형 버튼)
st.markdown("""
<style>
    /* 전체 화면 배경 하얀색 설정 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 좌측 파란색 버튼 (음성 느리게) 초대형 설정 */
    [data-testid="column"]:nth-child(1) button {
        background-color: #0055FF !important;
        color: #FFFFFF !important;
        height: 220px !important;
        width: 100% !important;
        border-radius: 30px !important;
        border: 8px solid #002288 !important;
        box-shadow: 0px 12px 25px rgba(0, 85, 255, 0.5) !important;
    }
    
    [data-testid="column"]:nth-child(1) button p,
    [data-testid="column"]:nth-child(1) button div,
    [data-testid="column"]:nth-child(1) button span {
        font-size: 45px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }

    /* 우측 빨간색 버튼 (음성 빠르게) 초대형 설정 */
    [data-testid="column"]:nth-child(2) button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        height: 220px !important;
        width: 100% !important;
        border-radius: 30px !important;
        border: 8px solid #880000 !important;
        box-shadow: 0px 12px 25px rgba(255, 0, 0, 0.5) !important;
    }

    [data-testid="column"]:nth-child(2) button p,
    [data-testid="column"]:nth-child(2) button div,
    [data-testid="column"]:nth-child(2) button span {
        font-size: 45px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }

    /* 메인 이동 대형 버튼 스타일 */
    .single-main-btn {
        display: block;
        width: 100%;
        padding: 45px 20px;
        margin: 20px 0;
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        text-decoration: none;
        border-radius: 30px;
        border: 6px solid #000000;
        box-shadow: 0px 12px 24px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease-in-out;
    }

    /* 단계별 고대비 색상 */
    .bg-step-1 { background-color: #FFD700 !important; color: #000000 !important; }
    .bg-step-2 { background-color: #00CC55 !important; color: #FFFFFF !important; }
    .bg-step-3 { background-color: #AA00FF !important; color: #FFFFFF !important; }

    .single-main-btn:hover {
        transform: scale(1.02);
    }

    /* 안내 박스 스타일 */
    .feature-card {
        background-color: #F0F4F8;
        border: 5px solid #111111;
        border-radius: 25px;
        padding: 30px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# [단계 데이터 정의 (1번 -> 2번 -> 3번 고정)]
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

# 현재 단계 확인 (1~3 범위 유효성 검사)
step = st.session_state.current_step
if step not in step_data:
    step = 1
    st.session_state.current_step = 1

current_info = step_data[step]

# ----------------------------------------------------
# [앱 타이틀 및 정보 표시]
# ----------------------------------------------------
st.title("🚌 시각장애인 버스 탑승 보조 안내 앱")
st.markdown(f"### 🔊 현재 속도: **{st.session_state.speech_rate}x** | 안내 단계: **기능 {step} / 3**")

# ----------------------------------------------------
# [상단 속도 조절 버튼 (좌: 파란색 느리게 / 우: 빨간색 빠르게)]
# ----------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🐢 음성 느리게", key="slow_btn"):
        st.session_state.speech_rate = max(0.5, round(st.session_state.speech_rate - 0.25, 2))
        st.rerun()

with col_right:
    if st.button("⚡ 음성 빠르게", key="fast_btn"):
        st.session_state.speech_rate = min(2.0, round(st.session_state.speech_rate + 0.25, 2))
        st.rerun()

st.markdown("---")

# ----------------------------------------------------
# [오프닝 멘트 포함 음성 생성 로직]
# ----------------------------------------------------
if st.session_state.is_first_load:
    intro_text = "안녕하세요, 지금부터 안내를 도와드릴 겁니다. 안내를 듣고 원하는 기능이 나왔을 때 색깔이 있는 버튼을 눌러주세요. "
    full_script = intro_text + current_info["script"]
    st.session_state.is_first_load = False
else:
    full_script = current_info["script"]

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
# [하단 컨트롤러: 수동 조작 및 다시 듣기]
# ----------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
    if st.button("⬅️ 이전 안내", key="prev_btn", use_container_width=True):
        st.session_state.current_step = 3 if step == 1 else step - 1
        st.rerun()

with col_ctrl2:
    if st.button("🔊 음성 다시 듣기", key="replay_btn", use_container_width=True):
        speak_and_auto_next(full_script, st.session_state.speech_rate, wait_ms=12000)

with col_ctrl3:
    if st.button("다음 안내 ➡️", key="next_btn", use_container_width=True):
        st.session_state.current_step = 1 if step == 3 else step + 1
        st.rerun()

# ----------------------------------------------------
# [다음 실행 시 적용할 단계(1 -> 2 -> 3 -> 1) 세션 반영]
# ----------------------------------------------------
st.session_state.current_step = 1 if step == 3 else step + 1

# 음성 자동 실행 및 12초 후 화면 갱신
speak_and_auto_next(full_script, st.session_state.speech_rate, wait_ms=12000)
