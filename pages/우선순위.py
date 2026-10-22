
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="버스 위치 안내",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- 디자인 ----------
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }

    .block-container {
        padding: 1.2rem 1.2rem 2rem 1.2rem;
        max-width: 1500px;
    }

    .location-title {
        background: #cfe2f3;
        border: 1.5px solid #222;
        height: 68px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 25px;
        color: #111;
        margin-bottom: 8px;
    }

    .map-panel {
        background: #cfe2f3;
        border: 1.5px solid #222;
        min-height: 570px;
        height: 68vh;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: #111;
        font-size: 24px;
        padding: 15px;
        box-sizing: border-box;
    }

    .speaker-area {
        min-height: 570px;
        height: 68vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .speaker-button {
        width: 130px;
        height: 130px;
        border: 2px solid #222;
        background: #cfe2f3;
        color: #111;
        border-radius: 12px;
        font-size: 65px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .hint {
        color: #333;
        text-align: center;
        font-size: 18px;
        margin-top: 20px;
    }

    div.stButton > button {
        min-height: 52px;
        font-size: 19px;
        border: 1.5px solid #333;
        border-radius: 8px;
    }

    @media (max-width: 700px) {
        .map-panel {
            min-height: 350px;
            height: 48vh;
            font-size: 19px;
        }

        .location-title {
            height: 58px;
            font-size: 22px;
        }

        .speaker-area {
            min-height: 180px;
            height: auto;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- 제목 ----------
st.markdown("""
<div style="
    border: 1.5px solid #222;
    padding: 12px 18px;
    margin-bottom: 16px;
    font-size: 25px;
    font-weight: 600;
">
    🚌 버스 위치 안내
</div>
""", unsafe_allow_html=True)

# ---------- 입력 정보 ----------
with st.expander("탑승 정보 설정", expanded=True):
    c1, c2 = st.columns(2)

    with c1:
        bus_number = st.selectbox(
            "타려는 버스 번호",
            ["701번", "702번", "703번", "704번"],
        )

    with c2:
        bus_position = st.radio(
            "안내할 버스 위치",
            ["앞쪽 버스", "뒤쪽 버스"],
            horizontal=True,
        )

# ---------- 메인 화면 ----------
left, right = st.columns([1.05, 0.95], gap="medium")

with left:
    st.markdown(
        '<div class="location-title">현재 위치</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="map-panel">
        <div>
            <div style="font-size:48px;">📍</div>
            <div>지도 사진(터치 시 음성 인식)</div>
            <div style="font-size:16px; margin-top:16px;">
                지도와 현재 위치를 표시하는 영역
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "현재는 화면 예시입니다. 실제 GPS 위치와 지도는 별도 연동이 필요합니다."
    )

with right:
    st.markdown(
        '<div class="location-title">음성 안내</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="speaker-area">
        <div style="
            font-size:105px;
            line-height:1.4;
            color:#111;
        ">◀</div>
        <div style="
            font-size:78px;
            color:#5d8db8;
            line-height:1;
        ">)) )</div>
        <div class="hint">
            아래 버튼을 눌러<br>버스 안내를 음성으로 들어보세요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 음성 안내 듣기", use_container_width=True):
        message = (
            f"탑승할 버스는 {bus_number}입니다. "
            f"선택한 위치는 {bus_position}입니다. "
            "실제 버스 위치 정보는 아직 연결되어 있지 않습니다. "
            "주변을 확인하고 안전하게 탑승하세요."
        )

        # 브라우저에서 음성 합성 실행
        safe_message = (
            message.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

        components.html(
            f"""
            <html>
            <body>
            <script>
                const message = "{safe_message}";
                if ("speechSynthesis" in window) {{
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(message);
                    utterance.lang = "ko-KR";
                    utterance.rate = 0.9;
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    document.body.innerText =
                        "이 브라우저에서는 음성 안내를 지원하지 않습니다.";
                }}
            </script>
            </body>
            </html>
            """,
            height=0,
        )

        st.info(f"안내 내용: {message}")

# ---------- 사용법 ----------
st.divider()
st.subheader("사용 방법")

guide1, guide2, guide3 = st.columns(3)

with guide1:
    st.markdown("### 1. 📍 위치 확인")
    st.write("지도 영역에서 현재 위치를 확인합니다.")

with guide2:
    st.markdown("### 2. 🚌 버스 선택")
    st.write("타려는 버스 번호와 안내할 위치를 선택합니다.")

with guide3:
    st.markdown("### 3. 🔊 음성 안내")
    st.write("음성 안내 버튼을 눌러 선택한 정보를 듣습니다.")

st.warning(
    "주의: 현재 버스 번호와 앞뒤 위치는 사용자가 직접 선택한 예시입니다. "
    "실제 버스의 GPS 정보와 연결된 서비스가 아니므로 "
    "실제 탑승 여부를 판단하는 용도로 사용하지 마세요."
)
