
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="버스 위치 안내",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .stApp {
        background: white;
        color: black;
    }

    [data-testid="stHeader"] {
        background: white;
    }

    .block-container {
        max-width: 1500px;
        padding: 20px 20px 30px 20px;
    }

    .outer-frame {
        border: 1px solid black;
        padding: 12px;
        min-height: 700px;
        box-sizing: border-box;
    }

    .location-title {
        height: 68px;
        background: #cfe2f3;
        border: 1.5px solid black;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        margin-bottom: 6px;
        box-sizing: border-box;
    }

    .map-panel {
        min-height: 560px;
        height: 68vh;
        background: #cfe2f3;
        border: 1.5px solid black;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 23px;
        padding: 10px;
        box-sizing: border-box;
    }

    .speaker-panel {
        height: 68vh;
        min-height: 560px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .speaker-svg {
        width: 100%;
        max-width: 420px;
        height: auto;
    }

    div.stButton > button {
        background: #cfe2f3;
        color: black;
        border: 1px solid black;
        border-radius: 5px;
        min-height: 50px;
        font-size: 18px;
    }

    @media (max-width: 700px) {
        .map-panel {
            min-height: 330px;
            height: 48vh;
            font-size: 18px;
        }

        .speaker-panel {
            min-height: 220px;
            height: 30vh;
        }

        .location-title {
            height: 55px;
            font-size: 21px;
        }
    }
</style>
""", unsafe_allow_html=True)

# 바깥 테두리
st.markdown('<div class="outer-frame">', unsafe_allow_html=True)

left, right = st.columns([1.05, 0.95], gap="small")

with left:
    st.markdown(
        '<div class="location-title">현재 위치</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="map-panel">
        지도 사진(터치시 음성인식)
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="speaker-panel">
      <svg class="speaker-svg"
           viewBox="0 0 360 300"
           xmlns="http://www.w3.org/2000/svg"
           role="img"
           aria-label="음성 안내 스피커 아이콘">

        <g fill="#cfe2f3"
           stroke="#111111"
           stroke-width="1.4"
           stroke-linejoin="round">

          <path d="M25 150 L125 60 L125 240 Z"/>

          <path d="
            M145 110
            C176 118 176 182 145 190
            C160 176 160 124 145 110 Z"/>

          <path d="
            M190 80
            C235 94 235 206 190 220
            C215 193 215 107 190 80 Z"/>

          <path d="
            M250 55
            C310 72 310 228 250 245
            C282 207 282 93 250 55 Z"/>

        </g>
      </svg>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 음성 안내 듣기", use_container_width=True):
        components.html("""
        <script>
        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(
                "현재 위치 안내입니다. 버스 안내 서비스를 이용해 주세요."
            );
            msg.lang = "ko-KR";
            window.speechSynthesis.speak(msg);
        }
        </script>
        """, height=0)

st.markdown('</div>', unsafe_allow_html=True)

st.caption(
    "※ 현재 화면은 디자인 예시입니다. "
    "실제 지도, GPS 위치 및 터치 음성 인식은 별도 연동이 필요합니다."
)
