
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

# 3. 브라우저 Web Speech API(TTS) 함수
# text 안에 따옴표나 줄바꿈이 있어도 JavaScript 문자열이 깨지지 않도록 처리합니다.
def speak_and_auto_next(text, rate, wait_ms=12000):
    import json

    safe_text = json.dumps(text, ensure_ascii=False)
    html_content = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance();
                msg.text = {safe_text};
                msg.lang = 'ko-KR';
                msg.rate = {rate};
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
