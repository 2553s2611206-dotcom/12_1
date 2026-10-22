
import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="버스 위치 자동 안내",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.block-container {
    max-width: 1400px;
    padding: 1rem;
}
.location-title {
    background: #cfe2f3;
    border: 1px solid #222;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    margin-bottom: 10px;
    color: #111;
}
div.stButton > button {
    min-height: 48px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚌 버스 위치 자동 안내")
st.write("버스별 정류장까지의 거리를 비교해 앞쪽과 뒤쪽 버스를 자동으로 안내합니다.")

left, right = st.columns([1.05, 0.95], gap="medium")

with left:
    st.markdown(
        '<div class="location-title">정류장 주변 지도</div>',
        unsafe_allow_html=True,
    )

    map_url = (
        "https://www.openstreetmap.org/"
        "export/embed.html?"
        "bbox=126.95%2C37.54%2C127.01%2C37.59"
        "&layer=mapnik&marker=37.5665%2C126.9780"
    )

    components.iframe(map_url, height=430, scrolling=True)

    st.caption("서울 시청 부근 예시 지도입니다. 실제 GPS 위치는 아닙니다.")

with right:
    st.markdown(
        '<div class="location-title">버스 위치 정보</div>',
        unsafe_allow_html=True,
    )

    st.write("버스 번호와 정류장까지의 거리를 입력하세요.")

    count = st.number_input(
        "확인할 버스 수",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
    )

    buses = []

    for i in range(int(count)):
        st.markdown(f"**버스 {i + 1}**")

        c1, c2 = st.columns(2)

        with c1:
            number = st.text_input(
                "버스 번호",
                value=f"{701 + i}번",
                key=f"bus_number_{i}",
            )

        with c2:
            distance = st.number_input(
                "정류장까지 거리(m)",
                min_value=0.0,
                max_value=100000.0,
                value=float(100 + i * 80),
                step=10.0,
                key=f"bus_distance_{i}",
            )

        buses.append({
            "number": number.strip(),
            "distance": distance,
        })

    if st.button("🔎 앞쪽·뒤쪽 버스 확인", use_container_width=True):
        valid = all(bus["number"] for bus in buses)
        unique = len({bus["number"] for bus in buses}) == len(buses)

        if not valid:
            st.error("모든 버스의 번호를 입력해 주세요.")
        elif not unique:
            st.error("버스 번호가 중복되지 않도록 입력해 주세요.")
        else:
            # 정류장까지 거리가 짧은 버스부터 정렬
            ordered = sorted(buses, key=lambda bus: bus["distance"])

            st.session_state["ordered_buses"] = ordered

            st.success("버스 위치 순서를 계산했습니다.")

            for i, bus in enumerate(ordered):
                position = "앞쪽" if i == 0 else (
                    "뒤쪽" if i == len(ordered) - 1 else f"{i + 1}번째"
                )

                st.write(
                    f"**{position} 버스:** {bus['number']} "
                    f"— 정류장까지 {bus['distance']:.0f}m"
                )

            if len(ordered) >= 2:
                front = ordered[0]["number"]
                rear = ordered[-1]["number"]

                message = (
                    f"앞쪽에는 {front} 버스가 있습니다. "
                    f"뒤쪽에는 {rear} 버스가 있습니다."
                )

                st.info(message)

                speech_text = json.dumps(
                    message,
                    ensure_ascii=False,
                )

                components.html(
                    f"""
                    <script>
                    if ("speechSynthesis" in window) {{
                        window.speechSynthesis.cancel();
                        const speech = new SpeechSynthesisUtterance(
                            {speech_text}
                        );
                        speech.lang = "ko-KR";
                        speech.rate = 0.9;
                        window.speechSynthesis.speak(speech);
                    }}
                    </script>
                    """,
                    height=0,
                )

st.divider()

st.subheader("작동 원리")
st.markdown("""
1. 각 버스의 정류장까지의 거리 정보를 받습니다.
2. 거리가 짧은 순서대로 버스를 자동 정렬합니다.
3. 가장 가까운 버스를 앞쪽, 가장 먼 버스를 뒤쪽으로 안내합니다.
4. 안내 결과를 화면과 음성으로 제공합니다.
""")

st.warning(
    "현재는 테스트용 거리 입력 방식입니다. "
    "실제 버스의 위치를 자동으로 알아내려면 실시간 버스 위치 API와 "
    "운행 방향 및 동일 노선 정보를 연동해야 합니다. "
    "정류장까지의 거리만으로 실제 차량의 앞뒤 순서가 항상 정확하게 "
    "판별되는 것은 아닙니다."
)
