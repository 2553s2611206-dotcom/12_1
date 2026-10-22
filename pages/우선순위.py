
import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="버스 위치 안내",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- 스타일 ----------
st.markdown("""
<style>
    .stApp {
        background-color: white;
        color: black;
    }

    .block-container {
        max-width: 1500px;
        padding: 1rem;
    }

    .location-title {
        background: #cfe2f3;
        border: 1px solid black;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        margin-bottom: 8px;
    }

    div.stButton > button {
        background: #cfe2f3;
        color: black;
        border: 1px solid black;
        min-height: 52px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚌 버스 위치 안내")

left, right = st.columns([1.05, 0.95], gap="medium")

# ---------- 기본 지도 위치 ----------
# 기본값은 서울 시청 부근의 지도 중심이며, 사용자 GPS 위치가 아닙니다.
if "map_lat" not in st.session_state:
    st.session_state.map_lat = 37.5665

if "map_lon" not in st.session_state:
    st.session_state.map_lon = 126.9780

if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

# ---------- 왼쪽: 실제 지도 ----------
with left:
    st.markdown(
        '<div class="location-title">현재 위치 / 지도</div>',
        unsafe_allow_html=True,
    )

    st.caption("지도를 클릭하면 선택한 위치를 확인할 수 있습니다.")

    try:
        m = folium.Map(
            location=[
                st.session_state.map_lat,
                st.session_state.map_lon,
            ],
            zoom_start=15,
            control_scale=True,
            tiles="OpenStreetMap",
        )

        folium.Marker(
            location=[
                st.session_state.map_lat,
                st.session_state.map_lon,
            ],
            tooltip="선택한 위치",
            popup="선택한 위치",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

        map_data = st_folium(
            m,
            height=520,
            use_container_width=True,
            key="real_bus_map",
            returned_objects=["last_clicked"],
        )

        clicked = map_data.get("last_clicked") if map_data else None

        if clicked:
            lat = clicked.get("lat")
            lon = clicked.get("lng")

            if lat is not None and lon is not None:
                st.session_state.map_lat = float(lat)
                st.session_state.map_lon = float(lon)
                st.session_state.selected_location = (
                    float(lat), float(lon)
                )

        st.markdown("**선택한 위치 좌표**")
        st.write(f"위도: {st.session_state.map_lat:.6f}")
        st.write(f"경도: {st.session_state.map_lon:.6f}")

    except Exception as e:
        st.error(
            "지도를 불러오지 못했습니다. 인터넷 연결과 "
            "라이브러리 설치 상태를 확인해 주세요."
        )
        st.caption(f"오류 정보: {e}")

# ---------- 오른쪽: 버스 정보 및 음성 ----------
with right:
    st.markdown(
        '<div class="location-title">버스 안내</div>',
        unsafe_allow_html=True,
    )

    st.write("타려는 버스 정보를 선택하세요.")

    bus_number = st.selectbox(
        "버스 번호",
        ["701번", "702번", "703번", "704번"],
    )

    bus_position = st.radio(
        "버스 위치",
        ["앞쪽 버스", "뒤쪽 버스", "아직 확인하지 못함"],
    )

    st.markdown("""
    <div style="
        min-height:170px;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:100px;
        color:#cfe2f3;
        -webkit-text-stroke: 1.5px black;
    ">◀ )))</div>
    """, unsafe_allow_html=True)

    if st.button("🔊 음성 안내 듣기", use_container_width=True):
        lat = st.session_state.map_lat
        lon = st.session_state.map_lon

        if bus_position == "아직 확인하지 못함":
            message = (
                f"{bus_number}를 선택했습니다. "
                "버스의 앞뒤 위치는 아직 확인되지 않았습니다. "
                "실제 버스 위치 정보를 확인해 주세요."
            )
        else:
            message = (
                f"선택한 버스는 {bus_number}입니다. "
                f"선택한 위치는 {bus_position}입니다. "
                "이 정보는 직접 선택한 값이며, "
                "실제 버스 위치를 확인한 결과는 아닙니다."
            )

        # JSON 인코딩으로 문자열 삽입 오류 방지
        import json
        safe_message = json.dumps(message, ensure_ascii=False)

        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <body>
            <script>
                const text = {safe_message};
                if ("speechSynthesis" in window) {{
                    window.speechSynthesis.cancel();
                    const speech = new SpeechSynthesisUtterance(text);
                    speech.lang = "ko-KR";
                    speech.rate = 0.9;
                    window.speechSynthesis.speak(speech);
                }} else {{
                    document.body.innerText =
                        "이 브라우저는 음성 안내를 지원하지 않습니다.";
                }}
            </script>
            </body>
            </html>
            """,
            height=45,
        )

        st.info(message)

    st.divider()
    st.subheader("현재 선택한 지도 위치")
    st.write(
        f"위도 {st.session_state.map_lat:.5f}, "
        f"경도 {st.session_state.map_lon:.5f}"
    )

st.divider()

st.caption(
    "지도는 OpenStreetMap을 사용합니다. "
    "실제 GPS 자동 위치 확인과 실시간 버스 위치 및 도착 정보는 "
    "아직 연동되지 않았습니다."
)
