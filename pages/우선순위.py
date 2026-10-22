
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="시각장애인 버스 자동 안내",
    page_icon="🚌",
    layout="wide",
)

# 10초마다 화면 자동 갱신
st_autorefresh(interval=10_000, key="bus_refresh")

st.title("🚌 시각장애인 버스 자동 안내")
st.caption("가상 버스 도착 정보 · 10초마다 자동 갱신")

st.info(
    "현재는 시뮬레이션입니다. 실제 버스 위치와 도착 정보를 "
    "가져오려면 교통정보 API 연결이 필요합니다."
)

# 초기 버스 데이터
if "buses" not in st.session_state:
    st.session_state.buses = [
        {"번호": "271", "도착": 4},
        {"번호": "7016", "도착": 7},
        {"번호": "162", "도착": 2},
    ]

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# 실제로 약 10초가 지났을 때만 가상 도착 시간 갱신
now = datetime.now()
elapsed = (now - st.session_state.last_update).total_seconds()

if elapsed >= 9:
    for bus in st.session_state.buses:
        bus["도착"] = max(
            1,
            bus["도착"] + random.choice([-1, 0, 0, 1])
        )
    st.session_state.last_update = now

ordered = sorted(
    st.session_state.buses,
    key=lambda bus: bus["도착"]
)

left, right = st.columns([1, 1])

with left:
    st.subheader("📍 정류장 지도")

    map_url = (
        "https://www.openstreetmap.org/export/embed.html?"
        "bbox=126.95%2C37.54%2C127.01%2C37.59"
        "&layer=mapnik&marker=37.5665%2C126.9780"
    )

    components.iframe(map_url, height=350, scrolling=True)

    st.caption("서울 시청 주변 예시 지도이며 실제 버스 위치는 아닙니다.")

with right:
    st.subheader("🔊 버스 도착 안내")

    for i, bus in enumerate(ordered):
        if i == 0:
            st.success(
                f"가장 먼저 도착: {bus['번호']}번 · 약 {bus['도착']}분"
            )
        else:
            st.write(
                f"{i + 1}번째 도착: {bus['번호']}번 · 약 {bus['도착']}분"
            )

    # 음성 설정
    volume = st.slider(
        "음성 크기",
        min_value=1,
        max_value=100,
        value=100,
        step=1,
        help="브라우저에서 지원하는 음성의 상대적 음량입니다."
    )

    rate = st.slider(
        "말하는 속도",
        min_value=5,
        max_value=10,
        value=8,
        step=1,
        help="숫자가 클수록 빠르게 말합니다."
    )

    speech = (
        f"버스 도착 안내입니다. "
        f"가장 먼저 도착할 버스는 {ordered[0]['번호']}번입니다. "
        f"도착 예정 시간은 약 {ordered[0]['도착']}분입니다."
    )

    # 버튼 자체를 크게 표시하고 음성도 크게 설정
    safe_text = (
        speech.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    html = f"""
    <div style="width:100%;">
      <button id="speak"
        style="
          width:100%;
          min-height:100px;
          font-size:28px;
          font-weight:bold;
          background:#0757C8;
          color:white;
          border:0;
          border-radius:16px;
          cursor:pointer;
        ">
        🔊 도착 정보 크게 듣기
      </button>
      <script>
        const button = document.getElementById("speak");
        button.addEventListener("click", function() {{
          const msg = new SpeechSynthesisUtterance('{safe_text}');
          msg.lang = "ko-KR";
          msg.volume = {volume / 100};
          msg.rate = {rate / 10};
          msg.pitch = 1;
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(msg);
        }});
      </script>
    </div>
    """

    components.html(html, height=115)

st.divider()

st.write(
    "마지막 화면 갱신 시각: "
    + datetime.now().strftime("%H:%M:%S")
)
st.caption("화면은 10초마다 자동으로 갱신됩니다.")
