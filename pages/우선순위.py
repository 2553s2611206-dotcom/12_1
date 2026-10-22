
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
from streamlit.components.v1 import html

st.set_page_config(
    page_title="시각장애인 버스 자동 안내",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 시각장애인 버스 자동 안내")
st.caption("가상 버스 도착 정보")

if "buses" not in st.session_state:
    st.session_state.buses = [
        {"번호": "271", "도착": 4},
        {"번호": "7016", "도착": 7},
        {"번호": "162", "도착": 2},
    ]

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

now = datetime.now()
elapsed = (now - st.session_state.last_update).total_seconds()

if elapsed >= 10:
    for bus in st.session_state.buses:
        bus["도착"] = max(
            1,
            bus["도착"] + random.choice([-1, 0, 1])
        )
    st.session_state.last_update = now

ordered = sorted(
    st.session_state.buses,
    key=lambda bus: bus["도착"]
)

left, right = st.columns(2)

with left:
    st.subheader("📍 정류장 지도")
    map_url = (
        "https://www.openstreetmap.org/export/embed.html?"
        "bbox=126.95%2C37.54%2C127.01%2C37.59"
        "&layer=mapnik&marker=37.5665%2C37.9780"
    )
    components.iframe(map_url, height=350)

with right:
    st.subheader("🔊 버스 도착 안내")

    for i, bus in enumerate(ordered):
        st.write(
            f"{i + 1}번째 도착: {bus['번호']}번 · "
            f"약 {bus['도착']}분"
        )

    volume = st.slider(
        "음성 크기",
        min_value=10,
        max_value=100,
        value=100
    )

    rate = st.slider(
        "음성 속도",
        min_value=5,
        max_value=10,
        value=8
    )

    speech = (
        f"가장 먼저 도착할 버스는 {ordered[0]['번호']}번입니다. "
        f"도착 예정 시간은 약 {ordered[0]['도착']}분입니다."
    )

    # 안전하게 문자열 전달
    import json
    speech_json = json.dumps(speech, ensure_ascii=False)

    html(
        f"""
        <button onclick="speakBus()"
            style="
                width:100%;
                height:100px;
                font-size:28px;
                font-weight:bold;
                background:#0757C8;
                color:white;
                border:none;
                border-radius:16px;
            ">
            🔊 도착 정보 크게 듣기
        </button>

        <script>
        function speakBus() {{
            const text = {speech_json};
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = "ko-KR";
            msg.volume = {volume / 100};
            msg.rate = {rate / 10};
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        }}
        </script>
        """,
        height=115
    )

st.divider()
st.write("현재 시각:", datetime.now().strftime("%H:%M:%S"))
st.caption("현재 버스 정보는 가상 데이터입니다.")
