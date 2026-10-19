    import json
import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="버스 우선순위 안내",
    page_icon="🚌",
    layout="centered",
)

st.markdown("""
<style>
.stApp { background: #101820; color: white; }
.block-container { max-width: 800px; padding-top: 2rem; }
h1, h2, h3, p, label, li { color: white !important; }
.stButton > button, .stFormSubmitButton > button {
    width: 100%;
    min-height: 50px;
    background: #F9D648;
    color: #101820;
    font-size: 17px;
    font-weight: bold;
    border-radius: 12px;
}
.bus-card {
    background: #1D2B36;
    border: 2px solid #F9D648;
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

if "buses" not in st.session_state:
    st.session_state.buses = [
        {"number": "701", "destination": "시청"},
        {"number": "702", "destination": "서울역"},
    ]

if "announcement" not in st.session_state:
    st.session_state.announcement = ""


def speak(message):
    """브라우저에서 한국어 음성 안내를 재생합니다."""
    text = json.dumps(str(message), ensure_ascii=False)
    components.html(
        f"""
        <button onclick="speakBus()"
        style="padding:12px;width:100%;font-size:18px;">
        🔊 음성 안내 듣기
        </button>
        <script>
        function speakBus() {{
            if (!window.speechSynthesis) {{
                alert("이 브라우저에서는 음성 안내를 지원하지 않습니다.");
                return;
            }}
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance({text});
            msg.lang = "ko-KR";
            msg.rate = 0.9;
            window.speechSynthesis.speak(msg);
        }}
        </script>
        """,
        height=65,
    )


st.title("🚌 버스 우선순위 안내")
st.subheader("시각장애인을 위한 버스 탑승 도우미")

st.info(
    "원하는 버스를 등록하고 우선순위를 설정해 보세요. "
    "현재 버전은 실제 버스 위치를 자동으로 감지하지 않는 체험용 앱입니다."
)

st.header("1. 버스 등록")

with st.form("bus_form", clear_on_submit=True):
    number = st.text_input("버스 번호", placeholder="예: 701")
    destination = st.text_input("행선지", placeholder="예: 시청")
    submitted = st.form_submit_button("버스 등록")

    if submitted:
        number = number.strip()
        destination = destination.strip()

        if not number or not destination:
            st.error("버스 번호와 행선지를 입력해 주세요.")
        elif not re.fullmatch(r"[0-9A-Za-z가-힣 -]+", number):
            st.error("버스 번호를 올바르게 입력해 주세요.")
        elif any(b["number"] == number for b in st.session_state.buses):
            st.error("이미 등록된 버스입니다.")
        elif len(st.session_state.buses) >= 20:
            st.error("버스는 최대 20대까지 등록할 수 있습니다.")
        else:
            st.session_state.buses.append({
                "number": number,
                "destination": destination,
            })
            st.success(f"{number}번 버스를 등록했습니다.")
            st.rerun()


st.header("2. 우선순위 설정")

if st.session_state.buses:
    numbers = [b["number"] for b in st.session_state.buses]

    priority_order = st.multiselect(
        "먼저 타고 싶은 버스부터 순서대로 선택하세요.",
        options=numbers,
        default=numbers,
        max_selections=len(numbers),
    )

    for bus in st.session_state.buses:
        if bus["number"] not in priority_order:
            priority_order.append(bus["number"])

    for rank, number in enumerate(priority_order, start=1):
        bus = next(
            b for b in st.session_state.buses
            if b["number"] == number
        )
        st.markdown(
            f"""
            <div class="bus-card">
                <h3>{rank}순위 · {bus['number']}번</h3>
                <p>행선지: {bus['destination']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.header("3. 앞·뒤 버스 안내")

    selected_number = st.selectbox(
        "확인할 버스",
        priority_order,
        format_func=lambda n: (
            f"{n}번 · "
            + next(
                b["destination"] for b in st.session_state.buses
                if b["number"] == n
            )
        ),
    )

    position = st.radio(
        "버스 위치 선택",
        ["앞쪽에 있는 버스", "뒤쪽에 있는 버스"],
    )

    if st.button("탑승 안내 확인"):
        rank = priority_order.index(selected_number) + 1
        bus = next(
            b for b in st.session_state.buses
            if b["number"] == selected_number
        )

        if rank == 1:
            message = (
                f"가장 높은 우선순위입니다. "
                f"{bus['number']}번 {bus['destination']}행 버스가 "
                f"{position}에 있다고 선택했습니다. "
                "실제 버스 번호와 행선지를 확인하세요."
            )
        else:
            message = (
                f"{bus['number']}번 {bus['destination']}행 버스는 "
                f"{rank}순위입니다. 위치는 {position}입니다. "
                "우선순위를 확인하고 실제 버스 번호를 확인하세요."
            )

        st.session_state.announcement = message

    if st.session_state.announcement:
        st.success(st.session_state.announcement)
        speak(st.session_state.announcement)

    st.header("4. 버스 삭제")

    delete_number = st.selectbox(
        "삭제할 버스 번호",
        [b["number"] for b in st.session_state.buses],
        key="delete_bus",
    )

    if st.button("선택한 버스 삭제"):
        st.session_state.buses = [
            b for b in st.session_state.buses
            if b["number"] != delete_number
        ]
        st.session_state.announcement = ""
        st.rerun()

else:
    st.warning("등록된 버스가 없습니다.")

st.divider()
st.caption(
    "안전 안내: 실제 차량 번호와 행선지를 확인한 후 탑승하세요. "
    "이 앱은 실제 버스를 자동으로 인식하지 않습니다."
)
3. pages/우선순위.py
버스 우선순위 사용법과 음성 안내를 설명하는 서브 페이지입니다.


python

import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="버스 우선순위 설명",
    page_icon="📢",
    layout="centered",
)

st.markdown("""
<style>
.stApp { background: #101820; color: white; }
.block-container { max-width: 800px; padding-top: 2rem; }
h1, h2, h3, p, li { color: white !important; }
.stButton > button {
    width: 100%;
    min-height: 50px;
    background: #F9D648;
    color: #101820;
    font-weight: bold;
    font-size: 17px;
}
.guide {
    background: #1D2B36;
    border: 2px solid #F9D648;
    padding: 18px;
    border-radius: 12px;
    margin: 12px 0;
    line-height: 1.9;
}
</style>
""", unsafe_allow_html=True)


def speak(message):
    text = json.dumps(message, ensure_ascii=False)
    components.html(
        f"""
        <button onclick="playGuide()"
        style="padding:12px;width:100%;font-size:18px;">
        🔊 안내 음성 듣기
        </button>
        <script>
        function playGuide() {{
            if (!window.speechSynthesis) {{
                alert("음성 안내를 지원하지 않는 브라우저입니다.");
                return;
            }}
            window.speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance({text});
            msg.lang = "ko-KR";
            msg.rate = 0.9;
            window.speechSynthesis.speak(msg);
        }}
        </script>
        """,
        height=65,
    )


st.title("📢 버스 우선순위 설명")
st.subheader("시각장애인을 위한 버스 이용 안내")

st.markdown("""
<div class="guide">
<strong>앱 소개</strong><br>
타려는 버스를 미리 등록하고 우선순위를 정해
버스 탑승을 준비할 수 있도록 도와주는 서비스입니다.
</div>
""", unsafe_allow_html=True)

st.header("1. 버스 우선순위란?")

st.markdown("""
<div class="guide">
<strong>1순위</strong><br>
가장 먼저 타고 싶은 버스<br><br>
<strong>2순위</strong><br>
두 번째로 타고 싶은 버스<br><br>
<strong>3순위</strong><br>
세 번째로 타고 싶은 버스
</div>
""", unsafe_allow_html=True)

st.header("2. 사용 방법")

steps = [
    "메인 화면에서 버스 번호와 행선지를 입력합니다.",
    "먼저 타고 싶은 버스부터 우선순위를 정합니다.",
    "확인할 버스를 선택합니다.",
    "앞쪽 또는 뒤쪽 버스 위치를 선택합니다.",
    "안내 내용을 읽거나 음성으로 듣습니다.",
    "실제 버스 번호와 행선지를 확인하고 탑승합니다.",
]

for i, step in enumerate(steps, start=1):
    st.markdown(
        f'<div class="guide"><strong>{i}단계</strong><br>{step}</div>',
        unsafe_allow_html=True,
    )

st.header("3. 앞쪽 버스와 뒤쪽 버스")

st.markdown("""
<div class="guide">
<strong>🚌 앞쪽에 있는 버스</strong><br>
앞에 있는 버스가 내가 타려는 버스인지
번호와 행선지를 확인합니다.<br><br>
<strong>🚌 뒤쪽에 있는 버스</strong><br>
뒤에 있는 버스도 번호와 행선지를 확인하여
탑승할 버스인지 판단합니다.
</div>
""", unsafe_allow_html=True)

st.warning(
    "현재 버전은 위치를 직접 선택하는 시뮬레이션입니다. "
    "실제 버스 번호와 위치를 자동으로 감지하려면 "
    "실시간 버스 정보와 별도 연동이 필요합니다."
)

st.header("4. 음성 안내 체험")

if st.button("사용법 음성으로 듣기"):
    st.session_state["voice_guide"] = True

if st.session_state.get("voice_guide", False):
    speak(
        "버스 우선순위 사용법입니다. "
        "메인 화면에서 버스를 등록하고 먼저 타고 싶은 "
        "버스를 1순위로 정하세요. "
        "버스에 탑승하기 전에 번호와 행선지를 확인하세요."
    )

st.header("5. 안전 수칙")

st.markdown("""
<div class="guide">
- 앞에 있는 버스가 반드시 내가 타려는 버스는 아닙니다.
- 뒤에 있는 버스도 내가 타려는 버스일 수 있습니다.
- 실제 버스 번호와 행선지를 확인하세요.
- 도로로 나가거나 움직이는 버스를 향해 이동하지 마세요.
</div>
""", unsafe_allow_html=True)
