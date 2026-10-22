
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
st.write("버스의 도착 예정 시간을 비교해 먼저 도착할 버스를 안내합니다.")

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

    st.caption("서울 시청 부근 예시 지도이며, 실제 GPS 위치는 아닙니다.")

with right:
    st.markdown(
        '<div class="location-title">버스 도착 예정 시간</div>',
        unsafe_allow_html=True,
    )

    st.write("버스 번호와 도착까지 남은 시간을 입력하세요.")

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
            minutes = st.number_input(
                "도착까지 남은 시간(분)",
                min_value=0,
                max_value=180,
                value=2 + i * 3,
                step=1,
                key=f"bus_time_{i}",
            )

        buses.append({
            "number": number.strip(),
            "minutes": int(minutes),
        })

    if st.button("🔎 도착 순서 확인", use_container_width=True):
        valid = all(bus["number"] for bus in buses)
        unique = len({bus["number"] for bus in buses}) == len(buses)

        if not valid:
            st.error("모든 버스의 번호를 입력해 주세요.")
        elif not unique:
            st.error("버스 번호가 중복되지 않도록 입력해 주세요.")
        else:
            ordered = sorted(buses, key=lambda bus: bus["minutes"])

            st.success("도착 예정 시간이 짧은 순서입니다.")

            for i, bus in enumerate(ordered):
                if i == 0:
                    position = "먼저 도착 예정"
                elif i == len(ordered) - 1:
                    position = "가장 늦게 도착 예정"
                else:
                    position = f"{i + 1}번째 도착 예정"

                st.write(
                    f"**{position}: {bus['number']}** "
                    f"— 약 {bus['minutes']}분 후"
                )

            if len(ordered) >= 2:
                first = ordered[0]
                last = ordered[-1]

                message = (
                    f"가장 먼저 도착할 예정인 버스는 "
                    f"{first['number']}이며 약 {first['minutes']}분 후입니다. "
                    f"가장 늦게 도착할 예정인 버스는 "
                    f"{last['number']}이며 약 {last['minutes']}분 후입니다."
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
st.subheader("사용 방법")

st.markdown("""
1. 버스 번호를 입력합니다.
2. 각 버스의 도착 예정 시간을 입력합니다.
3. '도착 순서 확인' 버튼을 누릅니다.
4. 시스템이 먼저 도착할 버스부터 정렬해 음성으로 안내합니다.
""")

st.warning(
    "도착 예정 시간은 실제 차량의 앞뒤 위치와 다를 수 있습니다. "
    "현재는 입력값으로 순서를 계산하며, 실제 버스 도착 정보는 "
    "연동되지 않았습니다."
)
