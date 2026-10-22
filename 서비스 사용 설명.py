import json
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="시각장애인 버스 탑승 보조 시스템",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 세션 상태 초기화
if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = 1.0
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "is_first_load" not in st.session_state:
    st.session_state.is_first_load = True
if "replay_requested" not in st.session_state:
    st.session_state.replay_requested = False

# 3. 브라우저 음성 안내
# 음성 안내 텍스트를 JSON으로 안전하게 전달해 따옴표로 인한 JS 오류를 방지합니다.
def speak_text(text, rate):
    safe_text = json.dumps(text, ensure_ascii=False)
    html_content = (
        "<script>"
        "(function(){"
        "if ('speechSynthesis' in window) {"
        "window.speechSynthesis.cancel();"
        "var msg = new SpeechSynthesisUtterance();"
        f"msg.text = {safe_text};"
        "msg.lang = 'ko-KR';"
        f"msg.rate = {float(rate)};"
        "window.speechSynthesis.speak(msg);"
        "}"
        "})();"
        "</script>"
    )
    components.html(html_content, height=0, width=0)

# 4. 화면 CSS 스타일링
# 삼중 따옴표를 사용하지 않고 문자열 목록으로 구성해 따옴표 미종료 오류를 방지합니다.
css_lines = [
    "<style>",
    ".stApp { background-color: #FFFFFF !important; color: #000000 !important; }",
    ".st-key-slow_btn button { background-color: #0055FF !important; color: #FFFFFF !important; width: 100% !important; height: 140px !important; min-height: 140px !important; border-radius: 24px !important; border: 7px solid #002288 !important; box-shadow: 0 10px 22px rgba(0,85,255,.40) !important; transition: transform .2s ease-in-out !important; }",
    ".st-key-slow_btn button p, .st-key-slow_btn button div, .st-key-slow_btn button span { color: #FFFFFF !important; font-size: 34px !important; font-weight: 900 !important; line-height: 1.3 !important; }",
    ".st-key-slow_btn button:hover { background-color: #003FCC !important; border-color: #001766 !important; transform: scale(1.02); }",
    ".st-key-fast_btn button { background-color: #FF0000 !important; color: #FFFFFF !important; width: 100% !important; height: 140px !important; min-height: 140px !important; border-radius: 24px !important; border: 7px solid #880000 !important; box-shadow: 0 10px 22px rgba(255,0,0,.40) !important; transition: transform .2s ease-in-out !important; }",
    ".st-key-fast_btn button p, .st-key-fast_btn button div, .st-key-fast_btn button span { color: #FFFFFF !important; font-size: 34px !important; font-weight: 900 !important; line-height: 1.3 !important; }",
    ".st-key-fast_btn button:hover { background-color: #CC0000 !important; border-color: #660000 !important; transform: scale(1.02); }",
    ".st-key-slow_btn button:focus-visible, .st-key-fast_btn button:focus-visible { outline: 5px solid #000000 !important; outline-offset: 4px !important; }",
    ".single-main-btn { display:block; width:100%; box-sizing:border-box; padding:35px 20px; margin:20px 0; font-size:32px; font-weight:900; line-height:1.4; text-align:center; text-decoration:none; border-radius:30px; border:6px solid #000000; box-shadow:0 12px 24px rgba(0,0,0,.25); transition:transform .2s ease-in-out; }",
    ".bg-step-1 { background-color:#FFD700 !important; color:#000000 !important; }",
    ".bg-step-2 { background-color:#00CC55 !important; color:#FFFFFF !important; }",
    ".bg-step-3 { background-color:#AA00FF !important; color:#FFFFFF !important; }",
    ".single-main-btn:hover { transform:scale(1.02); }",
    ".feature-card { background-color:#F0F4F8; border:5px solid #111111; border-radius:25px; padding:30px; margin-top:10px; }",
    "[data-testid='stHorizontalBlock'] button { min-height:65px; font-size:24px; font-weight:900; border-radius:15px; }",
    "@media (max-width:768px) { .st-key-slow_btn button, .st-key-fast_btn button { height:110px !important; min-height:110px !important; border-width:5px !important; border-radius:18px !important; } .st-key-slow_btn button p, .st-key-slow_btn button div, .st-key-slow_btn button span, .st-key-fast_btn button p, .st-key-fast_btn button div, .st-key-fast_btn button span { font-size:25px !important; } .single-main-btn { font-size:25px; padding:25px 15px; } }",
    "</style>",
]
st.markdown("\n".join(css_lines), unsafe_allow_html=True)

# 5. 단계 데이터
step_data = {
    1: {
        "title": "1️⃣ 기능 1: 경로 우선순위 탐색 안내",
        "desc": "목적지를 입력하면 어떤 경로가 가장 적합한지 알려줍니다.",
        "script": "기능 1번 안내입니다. 목적지를 입력하시면 가장 적합한 경로를 알려드립니다. 아래의 큰 버튼을 누르면 기능 1번 페이지로 이동합니다.",
        "link_text": "👉 [기능 1] 경로 우선순위 탐색",
        "link_url": "https://blindbus.streamlit.app/%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84",
        "bg_class": "bg-step-1",
    },
    2: {
        "title": "2️⃣ 기능 2: 버스 승하차 예약 알림",
        "desc": "타야 할 버스를 미리 선택하면 기사님에게 승차 의사를 전달하고 도착 시 알려줍니다.",
        "script": "기능 2번 안내입니다. 버스 승하차 예약을 돕는 기능입니다. 아래의 큰 버튼을 누르면 기능 2번 페이지로 이동합니다.",
        "link_text": "👉 [기능 2] 승하차 예약 페이지로 이동하기",
        "link_url": "https://blindbus.streamlit.app/%EC%B9%B4%EB%A9%94%EB%9D%BC_%EC%9D%B8%EC%8B%9D_%EC%8B%9C%EC%8A%A4%ED%85%9C",
        "bg_class": "bg-step-2",
    },
    3: {
        "title": "3️⃣ 기능 3: 정류장 주변 위험 안내",
        "desc": "정류장 주변의 보도블록, 벤치, 위험 장애물을 감지하여 안전하게 대기하도록 돕습니다.",
        "script": "마지막 기능 3번 안내입니다. 정류장 주변 위험 요소를 안내합니다. 아래의 큰 버튼을 누르면 기능 3번 페이지로 이동합니다.",
        "link_text": "👉 [기능 3] 주변 위험 안내 페이지로 이동하기",
        # 아래 주소를 실제 기능 3 페이지 주소로 교체하세요.
        "link_url": "3번링크를 넣으시오",
        "bg_class": "bg-step-3",
    },
}

# 6. 현재 단계
