
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
