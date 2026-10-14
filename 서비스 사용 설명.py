import streamlit as st

import json
import streamlit as st

st.set_page_config(
    page_title="버스 우선순위 음성 안내",
    page_icon="🚌",
    layout="centered",
)

st.title("🚌 버스 우선순위 음성 안내")
st.write("타려는 버스를 확인하고 도착 순서와 위치를 음성으로 안내합니다.")

st.warning(
    "학습용 시제품입니다. 실제 GPS와 실시간 버스정보는 연결되어 있지 않습니다. "
    "앞쪽/뒤쪽 정보는 사용자가 직접 입력합니다."
)

st.header("1. 타려는 버스")
target = st.text_input("내가 탈 버스 번호", value="701")

st.header("2. 비교할 버스 두 대")
left, right = st.columns(2)

with left:
    st.subheader("버스 A")
    route_a = st.text_input("버스 A 번호", value="701")
    eta_a = st.number_input(
        "버스 A 도착 예상 시간(분)",
        min_value=0, max_value=180, value=2,
    )
    pos_a = st.selectbox(
        "버스 A 위치",
        ["앞쪽에 있음", "뒤쪽에 있음", "위치 확인 안 됨"],
    )

with right:
    st.subheader("버스 B")
    route_b = st.text_input("버스 B 번호", value="273")
    eta_b = st.number_input(
        "버스 B 도착 예상 시간(분)",
        min_value=0, max_value=180, value=2,
    )
    pos_b = st.selectbox(
        "버스 B 위치",
        ["앞쪽에 있음", "뒤쪽에 있음", "위치 확인 안 됨"],
        index=1,
    )

def normalize(value):
    return (value or "").strip().replace("번 버스", "").replace("번", "")

if st.button("안내 결과 만들기", type="primary", use_container_width=True):
    if not route_a.strip() or not route_b.strip() or not target.strip():
        st.error("세 버스 번호 입력란을 확인해 주세요.")
    else:
        buses = [
            {"route": route_a.strip(), "eta": eta_a, "pos": pos_a},
            {"route": route_b.strip(), "eta": eta_b, "pos": pos_b},
        ]
        ordered = sorted(buses, key=lambda bus: bus["eta"])

        if eta_a == eta_b:
            order_text = (
                f"{route_a}번과 {route_b}번이 모두 약 {eta_a}분 후 "
                "도착 예정입니다. 도착 순서를 확정할 수 없습니다."
            )
        else:
            first, second = ordered
            order_text = (
                f"먼저 도착할 것으로 입력된 버스는 {first['route']}번, "
                f"약 {first['eta']}분 후입니다. "
                f"다음은 {second['route']}번, 약 {second['eta']}분 후입니다."
            )

        wanted = normalize(target)
        match = next(
            (bus for bus in buses if normalize(bus["route"]) == wanted),
            None,
        )

        if match:
            target_text = (
                f"타려는 {match['route']}번 버스는 "
                f"{match['pos']}에 있다고 입력되어 있습니다."
            )
        else:
            target_text = "입력한 두 버스 중 타려는 버스를 찾지 못했습니다."

        report = (
            f"버스 우선순위 안내입니다. {order_text} "
            f"{target_text} "
            "위치 정보는 직접 입력한 값입니다. "
            "승차 전에 버스 번호를 다시 확인하세요."
        )

        st.subheader("안내 결과")
        st.success(report)

        # 브라우저의 한국어 음성 합성 기능 사용
        safe_report = json.dumps(report, ensure_ascii=False)
        st.components.v1.html(
            f"""
            <button id="speak"
                style="font-size:18px;padding:12px;border-radius:8px">
                🔊 안내 음성 듣기
            </button>
            <button id="stop"
                style="font-size:18px;padding:12px;border-radius:8px">
                음성 중지
            </button>
            <p id="status" aria-live="polite"></p>
            <script>
                const message = {safe_report};
                const status = document.getElementById("status");

                document.getElementById("speak").onclick = () => {{
                    if (!("speechSynthesis" in window)) {{
                        status.textContent =
                            "이 브라우저는 음성 읽기를 지원하지 않습니다.";
                        return;
                    }}
                    window.speechSynthesis.cancel();
                    const speech = new SpeechSynthesisUtterance(message);
                    speech.lang = "ko-KR";
                    speech.rate = 0.88;
                    status.textContent = "안내를 읽고 있습니다.";
                    window.speechSynthesis.speak(speech);
                }};

                document.getElementById("stop").onclick = () => {{
                    if ("speechSynthesis" in window) {{
                        window.speechSynthesis.cancel();
                    }}
                    status.textContent = "음성 안내를 중지했습니다.";
                }};
            </script>
            """,
            height=110,
        )

st.divider()
st.caption(
    "이 앱은 예시 정보를 이용합니다. 실제 버스 위치나 도착 순서를 "
    "보장하지 않으며, 실제 승차 전에는 버스 번호를 별도로 확인하세요."
)
