
import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="버스 위치 안내",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 화면 디자인
st.markdown("""
<style>
    .block-container {
        padding: 1rem;
        max-width: 1400px;
    }

    .location-title {
        background-color: #cfe2f3;
        border: 1px solid #222;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        margin-bottom: 8px;
        color: #111;
    }

    .map-note {
        background: #cfe2f3;
        border: 1px solid #222;
        padding: 12px;
        font-size: 16px;
        color: #111;
    }

    div.stButton > button {
        min-height: 48px;
        font-size: 18px;
        background-color: #cfe2f3;
        color: #111;
        border: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚌 버스 위치 안내")

left, right = st.columns([1.05, 0.95], gap="medium")

with left:
    st.markdown(
        '<div class="location-title">현재 위치</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="map-note">실제 지도 · OpenStreetMap</div>',
        unsafe_allow_html=True,
    )

    # 실제 온라인 지도 삽입
    map_url = (
        "https://www.openstreetmap.org/"
        "export/embed.html?"
        "bbox=126.95%2C37.54%2C127.01%2C37.59"
        "&layer=mapnik"
        "&marker=37.5665%2C126.9780"
    )

    components.iframe(
        map_url,
        height=520,
        scrolling=True,
    )

    st.caption(
        "서울 시청 부근을 기본으로 표시합니다. "
        "실제 GPS 현재 위치는 아닙니다."
    )

with right:
    st.markdown(
        '<div class="location-title">음성 안내</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div style="
        height: 350px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 90px;
        color: #cfe2f3;
        -webkit-text-stroke: 1.5px #222;
    ">
        ◀ )))
    </div>
    """, unsafe_allow_html=True)

    bus_number = st.selectbox(
        "탑승할 버스 번호",
        ["701번", "702번", "703번", "704번"],
    )

    bus_position = st.selectbox(
        "버스 위치",
        ["앞쪽 버스", "뒤쪽 버스", "위치 미확인"],
    )

    if st.button("🔊 음성 안내 듣기", use_container_width=True):
        if bus_position == "위치 미확인":
            message = (
                f"{bus_number}의 위치를 아직 확인하지 못했습니다. "
                "실제 버스 위치 정보를 확인해 주세요."
            )
        else:
            message = (
                f"선택한 버스는 {bus_number}입니다. "
                f"선택한 위치는 {bus_position}입니다. "
                "실제 버스 위치와 일치하는지는 확인되지 않았습니다."
            )

        st.info(message)

        # 브라우저 음성 합성
        speech_text = json.dumps(message, ensure_ascii=False)

        components.html(
            f"""
            <script>
            const message = {speech_text};
            if ("speechSynthesis" in window) {{
                window.speechSynthesis.cancel();
                const utterance =
                    new SpeechSynthesisUtterance(message);
                utterance.lang = "ko-KR";
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }}
            </script>
            """,
            height=10,
        )

st.divider()

st.subheader("사용 방법")
st.write("1. 지도에서 주변 도로와 위치를 확인합니다.")
st.write("2. 탑승할 버스 번호를 선택합니다.")
st.write("3. 버스 위치를 선택하고 음성 안내 버튼을 누릅니다.")

st.warning(
    "이 앱은 지도와 시험용 음성 안내를 제공합니다. "
    "GPS 자동 위치 확인 및 실시간 버스 위치 정보는 "
    "아직 연결되지 않았습니다."
)
