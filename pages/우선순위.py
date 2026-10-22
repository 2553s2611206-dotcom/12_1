
import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import datetime

st.set_page_config(
    page_title="시각장애인 버스 자동 안내",
    page_icon="🚌",
    layout="wide"
)

# 10초마다 화면 자동 새로고침
components.html(
    """
    <script>
    setTimeout(function() {
        window.parent.location.reload();
    }, 10000);
    </script>
    """,
    height=0
)

st.title("🚌 시각장애인 버스 자동 안내")
st.caption("천안오성고등학교 주변 · 10초마다 자동 갱신")

st.warning(
    "현재 버스 도착 시간은 시연용 가상 데이터입니다. "
    "실제 버스 정보와 연결되어 있지 않습니다."
)

# 버스 번호와 가상 도착 시간
if "buses" not in st.session_state:
    st.session_state.buses = [
        {"번호": "14", "도착": 4},
        {"번호": "5", "도착": 7},
        {"번호": "3", "도착": 2},
    ]

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# 도착 시간 갱신
now = datetime.now()
elapsed = (now - st.session_state.last_update).total_seconds()

if elapsed >= 9:
    for bus in st.session_state.buses:
        bus["도착"] = max(
            1,
            bus["도착"] + random.choice([-1, 0, 1])
        )
    st.session_state.last_update = now

# 가장 빨리 도착하는 버스를 먼저 표시
ordered = sorted(
    st.session_state.buses,
    key=lambda bus: bus["도착"]
)

left, right = st.columns([1, 1])

with left:
    st.subheader("📍 천안오성고등학교 주변 지도")

    map_url = (
        "https://www.openstreetmap.org/"
        "export/embed.html?"
        "bbox=127.132%2C36.836%2C127.152%2C36.847"
        "&layer=mapnik"
        "&marker=36.84157%2C127.14215"
    )

    components.iframe(
        map_url,
        height=400,
        scrolling=True
    )

    st.caption(
        "천안시 성성동 천안오성고등학교 주변 지도"
    )

with right:
    st.subheader("🔊 버스 도착 안내")

    for i, bus in enumerate(ordered):
        if i == 0:
            st.success(
                f"가장 먼저 도착: {bus['번호']}번 버스 · "
                f"약 {bus['도착']}분"
            )
        else:
            st.write(
                f"{i + 1}번째 도착: {bus['번호']}번 버스 · "
                f"약 {bus['도착']}분"
            )

    volume = st.slider(
        "🔊 음성 크기",
        min_value=10,
        max_value=100,
        value=100,
        step=10
    )

    rate = st.slider(
        "🗣️ 음성 속도",
        min_value=5,
        max_value=10,
        value=8,
        step=1
    )

    speech = (
        "버스 도착 안내입니다. "
        f"가장 먼저 도착할 버스는 {ordered[0]['번호']}번입니다. "
        f"도착 예정 시간은 약 {ordered[0]['도착']}분입니다. "
        "다른 버스는 "
        + ", ".join(
            f"{bus['번호']}번, 약 {bus['도착']}분"
            for bus in ordered[1:]
        )
    )

    speech_json = json.dumps(speech, ensure_ascii=False)

    components.html(
        f"""
        <button id="speakButton"
            style="
                width:100%;
                height:110px;
                font-size:28px;
                font-weight:bold;
                background:#0757C8;
                color:white;
                border:none;
                border-radius:18px;
                cursor:pointer;
            ">
            🔊 도착 정보 크게 듣기
        </button>

        <script>
        document.getElementById("speakButton")
          .addEventListener("click", function() {{
            const message = new SpeechSynthesisUtterance(
                {speech_json}
            );

            message.lang = "ko-KR";
            message.volume = {volume / 100};
            message.rate = {rate / 10};
            message.pitch = 1;

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(message);
        }});
        </script>
        """,
        height=125
    )

st.divider()

st.write(
    "마지막 갱신 시각: "
    + datetime.now().strftime("%H:%M:%S")
)

st.caption(
    "현재 버스 도착 시간은 가상 데이터입니다. "
    "실제 버스 위치 및 도착 정보를 표시하지 않습니다."
)
