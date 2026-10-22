
import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import datetime

# -------------------------
# 기본 화면 설정
# -------------------------
st.set_page_config(
    page_title="시각장애인 버스 안내",
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
st.subheader("천안오성고등학교 주변 버스 안내")

st.warning(
    "현재는 시연용 가상 데이터입니다. "
    "실제 버스 도착 정보와 연결되어 있지 않습니다."
)

# -------------------------
# 버스 데이터 초기화
# -------------------------
if "buses" not in st.session_state:
    st.session_state.buses = [
        {"번호": "14", "도착": 4},
        {"번호": "5", "도착": 7},
        {"번호": "3", "도착": 2},
    ]

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# 가상 도착 시간 갱신
now = datetime.now()
elapsed = (now - st.session_state.last_update).total_seconds()

if elapsed >= 9:
    for bus in st.session_state.buses:
        bus["도착"] = max(
            1,
            bus["도착"] + random.choice([-1, 0, 1])
        )

    st.session_state.last_update = now

# 도착 시간이 짧은 순서로 정렬
ordered = sorted(
    st.session_state.buses,
    key=lambda bus: bus["도착"]
)

# -------------------------
# 지도와 안내 화면
# -------------------------
left, right = st.columns([1, 1])

with left:
    st.header("📍 정류장 주변 지도")

    map_url = (
        "https://www.openstreetmap.org/"
        "export/embed.html?"
        "bbox=127.132%2C36.836%2C127.152%2C36.847"
        "&layer=mapnik"
        "&marker=36.84157%2C127.14215"
    )

    components.iframe(
        map_url,
        height=450,
        scrolling=True
    )

    st.caption(
        "천안시 성성동 천안오성고등학교 주변 지도"
    )

with right:
    st.header("🚌 버스 도착 정보")

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

    # 음성 설정
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

    # 음성 안내 문장
    speech = (
        "버스 도착 안내입니다. "
        f"가장 먼저 도착할 버스는 {ordered[0]['번호']}번입니다. "
        f"도착 예정 시간은 약 {ordered[0]['도착']}분입니다. "
        + "다른 버스 정보입니다. "
        + ", ".join(
            f"{bus['번호']}번 버스는 약 {bus['도착']}분 후 도착합니다."
            for bus in ordered[1:]
        )
    )

    speech_json = json.dumps(
        speech,
        ensure_ascii=False
    )

    # 크게 만든 음성 안내 버튼
    components.html(
        f"""
        <button id="speakButton"
            style="
                width:100%;
                height:190px;
                font-size:38px;
                font-weight:bold;
                line-height:1.4;
                background:#0757C8;
                color:white;
                border:5px solid #003477;
                border-radius:24px;
                cursor:pointer;
                box-shadow:0 5px 10px rgba(0,0,0,0.25);
            ">
            🔊<br>
            도착 정보<br>
            크게 듣기
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
        height=205
    )

# -------------------------
# 갱신 시각
# -------------------------
st.divider()

st.write(
    "마지막 화면 갱신 시각: "
    + datetime.now().strftime("%H:%M:%S")
)

st.caption(
    "화면은 10초마다 새로고침됩니다. "
    "버스 도착 시간은 시연용 가상 데이터입니다."
)
