
import streamlit as st

st.set_page_config(
    page_title="버스 우선순위 설명",
    page_icon="🚌",
    layout="centered",
)

st.title("🚌 버스 우선순위 설명")
st.caption("버스 위치와 우선순위를 활용한 승차 안내")

st.divider()

st.header("1. 시스템 소개")
st.write(
    """
    버스 우선순위 시스템은 여러 버스가 한 정류장에 도착했을 때
    탑승하려는 버스를 구분하도록 돕는 것을 목표로 합니다.

    버스에 설치된 위치 확인 장치에서 정보를 얻고,
    버스의 앞뒤 위치와 사전에 설정된 우선순위를 비교해
    탑승할 버스를 식별하는 방식으로 설계할 수 있습니다.
    """
)

st.header("2. 어떻게 작동할까요?")

st.markdown(
    """
    **1단계 — 버스 정보 확인**

    버스 번호와 각 버스의 위치 정보를 확인합니다.

    **2단계 — 우선순위 확인**

    사용자가 타려는 버스의 번호와 설정된 우선순위를 비교합니다.

    **3단계 — 앞차와 뒷차 구분**

    위치 정보를 바탕으로 버스의 상대적인 앞뒤 관계를 확인합니다.

    **4단계 — 탑승 대상 안내**

    확인된 버스 정보를 화면이나 음성으로 안내하도록 설계합니다.
    """
)

st.info(
    "실제 시스템에서는 버스 번호와 위치 정보를 함께 확인해야 합니다. "
    "앞에 있다는 이유만으로 해당 버스가 탑승 대상이라고 판단하면 안 됩니다."
)

st.divider()

st.header("3. 앞차와 뒷차 구분 체험")
st.write(
    "아래 예시는 원리를 이해하기 위한 가상 상황입니다. "
    "실제 버스의 위치를 읽어 오는 기능은 포함하지 않습니다."
)

target_bus = st.selectbox(
    "내가 타려는 버스 번호",
    ["701번", "702번", "703번"],
)

front_bus = st.selectbox(
    "앞쪽 버스 번호",
    ["701번", "702번", "703번"],
    index=0,
)

rear_bus = st.selectbox(
    "뒤쪽 버스 번호",
    ["701번", "702번", "703번"],
    index=1,
)

if front_bus == rear_bus:
    st.warning("앞쪽 버스와 뒤쪽 버스의 번호를 다르게 선택해 주세요.")
else:
    st.markdown("### 🚏 현재 버스 배치")
    st.markdown(
        f"""
        <div style="
            border: 1px solid #D9E2EC;
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            background-color: #F5F8FC;
            color: #183153;
        ">
            <div style="font-size: 14px;">정류장 방향 →</div>
            <div style="
                margin: 12px 0;
                padding: 12px;
                border-radius: 10px;
                background-color: #DCEBFA;
                font-size: 18px;
                font-weight: bold;
            ">앞쪽 버스: {front_bus}</div>
            <div style="
                margin: 12px 0;
                padding: 12px;
                border-radius: 10px;
                background-color: #E5E7EB;
                font-size: 18px;
                font-weight: bold;
            ">뒤쪽 버스: {rear_bus}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔊 안내 결과")

    if target_bus == front_bus:
        st.success(
            f"선택한 탑승 대상은 {target_bus}입니다. "
            "예시 배치에서 앞쪽 버스와 번호가 일치합니다."
        )
    elif target_bus == rear_bus:
        st.success(
            f"선택한 탑승 대상은 {target_bus}입니다. "
            "예시 배치에서 뒤쪽 버스와 번호가 일치합니다."
        )
    else:
        st.warning(
            f"탑승 대상은 {target_bus}이지만, "
            "현재 선택한 앞쪽·뒤쪽 버스 중에는 없습니다. "
            "추가 버스 정보를 확인해야 합니다."
        )

st.caption(
    "위 결과는 사용자가 직접 입력한 가상 정보에 따른 예시이며, "
    "실제 위치 확인이나 음성 출력 결과가 아닙니다."
)

st.divider()

st.header("4. 사용 방법")

st.markdown(
    """
    1. 메인 페이지에서 **버스 우선순위 설명**을 선택합니다.
    2. 시스템 소개와 작동 단계를 읽습니다.
    3. 체험 영역에서 내가 타려는 버스 번호를 선택합니다.
    4. 앞쪽 버스와 뒤쪽 버스 번호를 선택합니다.
    5. 안내 결과를 확인해 버스 번호와 위치의 관계를 이해합니다.
    """
)

st.header("5. 기대 효과")
st.markdown(
    """
    - 여러 버스가 동시에 도착하는 상황에서 버스 식별을 보조합니다.
    - 시각장애인이 탑승 대상 버스를 확인하는 데 도움을 줄 수 있습니다.
    - 향후 GPS, 버스 도착 정보, 음성 안내 장치와 연동할 수 있습니다.
    """
)

st.warning(
    "안전 안내: 이 체험 화면만으로 실제 버스를 찾아 탑승하지 마세요. "
    "실제 사용을 위해서는 검증된 위치 정보와 접근성 안내 기능이 필요합니다."
)
