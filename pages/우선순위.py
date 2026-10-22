
import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

st.set_page_config(
    page_title="시각장애인 버스 안내",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 시각장애인 버스 자동 안내")
st.caption("버스 도착 정보를 자동으로 확인하는 시뮬레이션")

st.info(
    "현재는 가상 버스 정보입니다. "
    "실제 버스 위치 및 도착 시간과 연결된 것은 아닙니다."
)

# 가상 버스 정보 초기화
if "buses" not in st.session_state:
    st.session_state.buses = [
        {"번호": "271", "도착": 4},
        {"번호": "7016", "도착": 7},
        {"번호": "162", "도착": 2},
    ]

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# 10초마다 가상 도착 시간 갱신
now = time.time()

if now - st.session_state.last_update >= 10:
    for bus in st.session_state.buses:
        bus["도착"] = max(
            1,
            bus["도착"] + random.choice([-1, 0, 0, 1])
        )

    st.session_state.last_update = now

# 도착 시간이 짧은 순서로 정렬
ordered = sorted(
    st.session_state.buses,
    key=lambda bus: bus["도착"]
)

left, right = st.columns([1, 1])

with left:
    st.subheader("📍 정류장 지도")

    map_url = (
        "https://www.openstreetmap.org/"
        "export/embed.html?"
        "bbox=126.95%2C37.54%2C127.01%2C37.59"
        "&layer=mapnik"
        "&marker=37.5665%2C126.9780"
    )

    components.iframe(
        map_url,
        height=350,
        scrolling=True
    )

    st.caption(
        "지도는 서울 시청 주변 예시이며, "
        "실제 버스 위치를 표시하지 않습니다."
    )

with right:
    st.subheader("🔊 버스 도착 안내")

    st.write(
        "시스템이 확인한 가상 도착 정보를 "
        "빠른 순서대로 안내합니다."
    )

    for i, bus in enumerate(ordered):
        if i == 0:
            st.success(
                f"가장 먼저 도착할 버스: "
                f"{bus['번호']}번 · 약 {bus['도착']}분"
            )
        else:
            st.write(
                f"{i + 1}번째: {bus['번호']}번 버스 "
                f"· 약 {bus['도착']}분"
            )

    speech = (
        f"버스 도착 안내입니다. "
        f"가장 먼저 도착할 버스는 "
        f"{ordered[0]['번호']}번 버스입니다. "
        f"도착 예정 시간은 약 "
        f"{ordered[0]['도착']}분입니다."
    )

    if st.button("🔊 도착 정보 음성으로 듣기"):
        safe_text = speech.replace("\\", "\\\\").replace("'", "\\'")
        components.html(
            f"""
            <script>
            const msg = new SpeechSynthesisUtterance('{safe_text}');
            msg.lang = 'ko-KR';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
            </script>
            """,
            height=0
        )

st.divider()

st.write(
    "마지막 갱신 시각: "
    + datetime.now().strftime("%H:%M:%S")
)

if st.button("🔄 정보 새로고침"):
    st.rerun()

# 10초 후 화면 자동 갱신
time.sleep(10)
st.rerun()

