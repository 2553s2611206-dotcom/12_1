python

import streamlit as st
import streamlit.components.v1 as components
import html
import re

st.set_page_config(
    page_title="버스 우선순위 안내",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background-color: #101820;
    color: #FFFFFF;
}
[data-testid="stHeader"] {
    background-color: #101820;
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label, li {
    color: #FFFFFF !important;
}
.stButton > button, .stFormSubmitButton > button {
    min-height: 52px;
    width: 100%;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 700;
    border: 2px solid #F9D648;
    color: #101820;
    background: #F9D648;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #FFE985;
    color: #101820;
    border-color: #FFE985;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
.bus-card {
    border: 2px solid #F9D648;
    border-radius: 14px;
    padding: 18px;
    margin: 10px 0;
    background: #1D2B36;
}
.bus-number {
    color: #F9D648;
    font-size: 30px;
    font-weight: 800;
}
.bus-info {
    color: white;
    font-size: 17px;
    line-height: 1.8;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: white;
}
</style>
""", unsafe_allow_html=True)

if "buses" not in st.session_state:
    st.session_state.buses = [
        {"number": "701", "destination": "시청", "priority": 1},
        {"number": "702", "destination": "서울역", "priority": 2},
    ]

if "announcement" not in st.session_state:
    st.session_state.announcement = ""

def speak(text):
    """브라우저의 음성 합성 기능을 이용한 한국어 안내."""
    safe_text = html.escape(str(text), quote=True)
    components.html(
        f"""
        <div style="font-family:sans-serif;color:#fff;background:#1D2B36;
                    padding:8px;border-radius:8px;">
          <p>🔊 음성 안내를 실행합니다.</p>
        </div>
        <script>
        (function() {{
          const message = "{safe_text}";
          if (!('speechSynthesis' in window)) {{
            document.body.insertAdjacentHTML(
              'beforeend',
              '<p>이 브라우저에서는 음성 안내를 지원하지 않습니다.</p>'
            );
            return;
          }}
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(message);
          utterance.lang = 'ko-KR';
          utterance.rate = 0.9;
          window.speechSynthesis.speak(utterance);
        }})();
        </script>
        """,
        height=65,
    )

st.title("🚌 버스 우선순위 안내")
st.markdown("### 시각장애인을 위한 더 쉬운 버스 탑승")
st.markdown(
    "타려는 버스를 미리 등록하고, 우선순위를 확인해 보세요. "
    "큰 글씨와 음성 안내로 탑승 준비를 도와드립니다."
)

st.info(
    "체험용 앱입니다. 실제 버스 위치나 도착 정보를 자동으로 수신하지 않습니다. "
    "아래 버스 위치 안내는 사용자가 선택하는 시뮬레이션입니다."
)

st.header("1. 탈 버스 등록")

with st.form("add_bus_form", clear_on_submit=True):
    number = st.text_input(
        "버스 번호",
        placeholder="예: 701",
        max_chars=12,
    )
    destination = st.text_input(
        "행선지",
        placeholder="예: 시청",
        max_chars=30,
    )
    submitted = st.form_submit_button("버스 등록하기")

    if submitted:
        clean_number = number.strip()
        clean_destination = destination.strip()

        if not clean_number or not clean_destination:
            st.error("버스 번호와 행선지를 모두 입력해 주세요.")
        elif not re.fullmatch(r"[0-9A-Za-z가-힣 -]+", clean_number):
            st.error("버스 번호에는 문자와 숫자만 입력해 주세요.")
        elif any(b["number"] == clean_number for b in st.session_state.buses):
            st.error("이미 등록한 버스 번호입니다.")
        elif len(st.session_state.buses) >= 20:
            st.error("버스는 최대 20대까지 등록할 수 있습니다.")
        else:
            st.session_state.buses.append({
                "number": clean_number,
                "destination": clean_destination,
                "priority": len(st.session_state.buses) + 1,
            })
            st.success(f"{clean_number}번 버스를 등록했습니다.")
            st.rerun()

st.header("2. 버스 우선순위 정하기")
st.markdown(
    "숫자가 작을수록 먼저 타고 싶은 버스입니다. "
    "우선순위는 각 버스 카드에서 직접 변경할 수 있습니다."
)

if not st.session_state.buses:
    st.warning("등록된 버스가 없습니다. 먼저 버스를 등록해 주세요.")
else:
    for bus in sorted(
        st.session_state.buses,
        key=lambda b: b["priority"],
    ):
        with st.container(border=True):
            st.markdown(
                f"### 🚌 {bus['number']}번 · {bus['destination']}행"
            )
            current_index = st.session_state.buses.index(bus)
            priority_options = list(
                range(1, len(st.session_state.buses) + 1)
            )
            selected_priority = st.selectbox(
                f"{bus['number']}번 우선순위",
                priority_options,
                index=bus["priority"] - 1,
                key=f"priority_{bus['number']}",
                format_func=lambda x: f"{x}순위",
            )
            bus["priority"] = selected_priority

            if st.button(
                f"{bus['number']}번 삭제",
                key=f"delete_{bus['number']}",
            ):
                st.session_state.buses = [
                    b for b in st.session_state.buses
                    if b["number"] != bus["number"]
                ]
                for i, item in enumerate(
                    sorted(
                        st.session_state.buses,
                        key=lambda b: b["priority"],
                    ),
                    start=1,
                ):
                    item["priority"] = i
                st.rerun()

    # 동일 순위가 생기면 등록 순서대로 안정적으로 표시합니다.
    ordered_buses = sorted(
        st.session_state.buses,
        key=lambda b: b["priority"],
    )

    st.subheader("현재 탑승 우선순위")
    for index, bus in enumerate(ordered_buses, start=1):
        st.markdown(
            f"""
            <div class="bus-card">
              <div class="bus-number">{index}순위 · {bus['number']}번</div>
              <div class="bus-info">행선지: {html.escape(bus['destination'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 실제 순위 값도 표시 순서대로 정리합니다.
    for index, bus in enumerate(ordered_buses, start=1):
        bus["priority"] = index

st.header("3. 앞 버스 / 뒤 버스 안내")
st.markdown(
    "버스가 정류장에 접근한다고 가정하고 위치를 선택하면 "
    "등록한 우선순위를 기준으로 안내 문구를 만들 수 있습니다."
)

if st.session_state.buses:
    ordered_buses = sorted(
        st.session_state.buses,
        key=lambda b: b["priority"],
    )
    bus_options = [
        f"{b['number']}번 · {b['destination']}행"
        for b in ordered_buses
    ]
    selected_bus_label = st.selectbox(
        "확인할 버스",
        bus_options,
        key="target_bus",
    )
    selected_bus = ordered_buses[bus_options.index(selected_bus_label)]

    position = st.radio(
        "버스의 위치",
        ["앞쪽에 있는 버스", "뒤쪽에 있는 버스"],
        horizontal=False,
    )

    if st.button("탑승 안내 확인하기"):
        if selected_bus["priority"] == 1:
            message = (
                f"우선순위 1순위 버스입니다. "
                f"{selected_bus['number']}번 "
                f"{selected_bus['destination']}행 버스를 확인하세요. "
                f"선택한 위치는 {position}입니다. "
                "실제 차량 번호를 확인한 뒤 탑승해 주세요."
            )
        else:
            message = (
                f"{selected_bus['number']}번 "
                f"{selected_bus['destination']}행 버스는 "
                f"{selected_bus['priority']}순위입니다. "
                f"선택한 위치는 {position}입니다. "
                "더 높은 우선순위의 버스가 있는지 확인해 주세요."
            )

        st.session_state.announcement = message

    if st.session_state.announcement:
        st.markdown("### 📢 탑승 안내")
        st.success(st.session_state.announcement)
        if st.button("안내 음성 듣기"):
            speak(st.session_state.announcement)
else:
    st.warning("안내할 버스를 먼저 등록해 주세요.")

st.divider()
st.caption(
    "안전 안내: 이 앱은 실제 버스 번호를 자동 인식하지 않습니다. "
    "차량 번호와 행선지를 운전자에게 확인한 후 탑승하세요."
)
4. pages/우선순위.py — 버스 우선순위 설명 서브 페이지
pages 폴더를 만든 뒤, 그 안에 우선순위.py 파일을 만들고 아래 코드를 붙여 넣으세요. 페이지 이름은 Streamlit 사이드바에 우선순위로 표시되며, 화면 제목은 요청한 대로 버스 우선순위 설명으로 구성했습니다.


python

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="버스 우선순위 설명",
    page_icon="📢",
    layout="centered",
)

st.markdown("""
<style>
.stApp {
    background: #101820;
    color: white;
}
.block-container {
    max-width: 800px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, li, label {
    color: white !important;
}
.stButton > button {
    min-height: 52px;
    width: 100%;
    border-radius: 12px;
    background: #F9D648;
    color: #101820;
    border: 2px solid #F9D648;
    font-size: 17px;
    font-weight: bold;
}
.guide-card {
    background: #1D2B36;
    border: 2px solid #F9D648;
    border-radius: 14px;
    padding: 18px;
    margin: 12px 0;
    color: white;
    font-size: 17px;
    line-height: 1.9;
}
.big-number {
    color: #F9D648;
    font-size: 27px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


def speak(text):
    """브라우저에서 한국어 음성 안내를 실행합니다."""
    import json

    message = json.dumps(text, ensure_ascii=False)
    components.html(
        f"""
        <button id="speak-button"
          style="width:100%;padding:15px;border-radius:10px;
          border:2px solid #F9D648;background:#F9D648;
          color:#101820;font-size:17px;font-weight:bold;">
          🔊 음성 안내 재생
        </button>
        <script>
        document.getElementById("speak-button").onclick = function() {{
            if (!("speechSynthesis" in window)) {{
                alert("이 브라우저는 음성 안내를 지원하지 않습니다.");
                return;
            }}
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance({message});
            utterance.lang = "ko-KR";
            utterance.rate = 0.9;
            window.speechSynthesis.speak(utterance);
        }};
        </script>
        """,
        height=80,
    )


st.title("📢 버스 우선순위 설명")
st.markdown("### 시각장애인을 위한 버스 탑승 도우미")

st.markdown("""
<div class="guide-card">
<strong>이 앱은 무엇인가요?</strong><br>
시각장애인이 타려는 버스를 미리 등록하고,
어떤 버스를 먼저 타고 싶은지 순서를 정해 두는
버스 탑승 보조 앱입니다.
</div>
""", unsafe_allow_html=True)

st.header("1. 버스 우선순위란?")
st.write(
    "여러 버스를 등록한 뒤 먼저 타고 싶은 버스부터 "
    "순서를 정하는 기능입니다."
)

st.markdown("""
<div class="guide-card">
<div class="big-number">1순위</div>
가장 먼저 타고 싶은 버스
<hr>
<div class="big-number">2순위</div>
첫 번째 버스가 아니라면 고려할 버스
<hr>
<div class="big-number">3순위</div>
그다음으로 고려할 버스
</div>
""", unsafe_allow_html=True)

st.header("2. 사용 방법")

steps = [
    (
        "첫 번째",
        "메인 화면에서 버스 번호와 행선지를 입력합니다."
    ),
    (
        "두 번째",
        "등록된 버스의 우선순위를 선택합니다. 숫자가 작을수록 우선입니다."
    ),
    (
        "세 번째",
        "정류장에 버스가 접근하면 안내 화면에서 확인할 버스를 선택합니다."
    ),
    (
        "네 번째",
        "앞쪽 버스인지 뒤쪽 버스인지 선택해 안내 문구를 확인하고 음성으로 들을 수 있습니다."
    ),
    (
        "다섯 번째",
        "실제 버스 번호와 행선지를 확인한 후 안전하게 탑승합니다."
    ),
]

for title, description in steps:
    st.markdown(
        f"""
        <div class="guide-card">
          <div class="big-number">{title}</div>
          {description}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.header("3. 앞 버스와 뒤 버스 안내")

st.markdown("""
<div class="guide-card">
<strong>🚌 앞쪽에 있는 버스</strong><br>
앞에 접근한 버스가 내가 타려는 버스인지
등록한 번호와 행선지를 확인합니다.
<hr>
<strong>🚌 뒤쪽에 있는 버스</strong><br>
뒤에서 접근한 버스도 등록한 번호와 행선지를
확인해 탑승할 버스인지 판단합니다.
</div>
""", unsafe_allow_html=True)

st.warning(
    "현재 버전은 앞·뒤 위치를 직접 선택하는 체험용입니다. "
    "실제 차량 위치나 버스 번호를 자동으로 감지하지 않습니다."
)

st.header("4. 음성 안내 체험")

st.write(
    "아래 버튼을 눌러 앱이 버스 이용 안내를 음성으로 "
    "읽어 주는 방식을 체험해 보세요."
)

if st.button("음성 안내 듣기", key="show_voice"):
    st.session_state["play_guide"] = True

if st.session_state.get("play_guide", False):
    speak(
        "버스 우선순위 안내입니다. "
        "먼저 타고 싶은 버스를 1순위로 설정하세요. "
        "버스가 도착하면 번호와 행선지를 확인하고 "
        "안전하게 탑승해 주세요."
    )

st.header("5. 꼭 기억해 주세요")

st.markdown("""
<div class="guide-card">
- 우선순위는 내가 타고 싶은 버스의 순서입니다.
- 앞에 있다고 해서 반드시 내가 타려는 버스는 아닙니다.
- 뒤에 있다고 해서 타면 안 되는 버스도 아닙니다.
- 차량 번호와 행선지는 반드시 실제로 확인해야 합니다.
- 이 앱만 믿고 도로에 가까이 다가가거나 움직이는 버스를 향해 이동하지 마세요.
</div>
""", unsafe_allow_html=True)

st.caption(
    "더 정확한 자동 안내를 제공하려면 실제 버스 도착정보 API와 "
    "차량 위치 정보의 연동이 필요합니다."
)
