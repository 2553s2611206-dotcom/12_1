```python
# pages/카메라 인식 시스템.py
# 프로토타입용 가짜 버스 인식 결과
# 실제 AI 분석 및 실제 버스 번호 확인 기능은 포함하지 않습니다.

import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="버스 번호 카메라 인식",
    page_icon="🚌",
    layout="centered",
)

# -----------------------------
# 제목 및 설명
# -----------------------------
st.title("🚌 버스 번호 카메라 인식")
st.write(
    "카메라로 버스를 촬영하는 상황을 체험하고 "
    "버스 번호 음성 안내 기능을 시연할 수 있습니다."
)

st.warning(
    "프로토타입 시연 모드입니다. 아래에 표시되는 버스 번호는 "
    "가짜 테스트 데이터이며 사진을 실제로 분석한 결과가 아닙니다."
)

# -----------------------------
# 가짜 테스트 데이터
# -----------------------------
TEST_RESULTS = {
    "인식 성공 — 273번": {
        "recognized": True,
        "bus_number": "273",
        "message": "테스트 안내입니다. 273번 버스입니다.",
    },
    "인식 성공 — 7016번": {
        "recognized": True,
        "bus_number": "7016",
        "message": "테스트 안내입니다. 7016번 버스입니다.",
    },
    "인식 성공 — 143번": {
        "recognized": True,
        "bus_number": "143",
        "message": "테스트 안내입니다. 143번 버스입니다.",
    },
    "인식 실패": {
        "recognized": False,
        "bus_number": "",
        "message": (
            "테스트 안내입니다. 버스 번호를 확인할 수 없습니다. "
            "카메라를 버스 번호 쪽으로 다시 맞춰 주세요."
        ),
    },
}

# -----------------------------
# 사진 촬영 및 업로드
# -----------------------------
st.subheader("📷 1. 버스 사진 촬영")

camera_photo = st.camera_input(
    "버스 번호가 보이도록 촬영해 주세요"
)

uploaded_photo = st.file_uploader(
    "또는 버스 사진 업로드",
    type=["jpg", "jpeg", "png", "webp"],
)

selected_photo = (
    camera_photo if camera_photo is not None else uploaded_photo
)

if selected_photo is not None:
    try:
        photo = Image.open(
            BytesIO(selected_photo.getvalue())
        ).convert("RGB")

        st.image(
            photo,
            caption="선택한 사진 — 테스트용",
            width="stretch",
        )
    except Exception:
        st.error("사진을 열 수 없습니다. 다른 사진을 선택해 주세요.")

st.divider()

# -----------------------------
# 테스트 결과 선택
# -----------------------------
st.subheader("🧪 2. 시연할 테스트 결과 선택")

scenario = st.selectbox(
    "버튼을 눌렀을 때 보여 줄 결과",
    options=list(TEST_RESULTS.keys()),
    index=0,
)

st.caption(
    "시연할 결과를 선택할 수 있습니다. 사진이 없어도 테스트할 수 있습니다."
)

# -----------------------------
# 결과 표시
# -----------------------------
if st.button(
    "🔍 버스 번호 인식하기 (테스트)",
    type="primary",
    width="stretch",
):
    st.session_state["prototype_bus_result"] = TEST_RESULTS[scenario]

result = st.session_state.get("prototype_bus_result")

if result is not None:
    st.divider()
    st.subheader("📢 3. 테스트 인식 결과")

    if result["recognized"]:
        st.success("테스트 인식 성공")

        st.markdown(
            f"# 🚌 {result['bus_number']}번 버스"
        )
    else:
        st.error("테스트 인식 실패")

    st.info(result["message"])

    st.caption(
        "위 결과는 미리 지정한 가짜 데이터입니다. "
        "실제 버스 번호를 인식하거나 확인한 결과가 아닙니다."
    )

    # -----------------------------
    # 음성 안내 시연용 텍스트
    # -----------------------------
    st.subheader("🔊 음성 안내 시연")

    st.write("아래 문장을 음성 안내 문구로 사용합니다.")

    st.text_area(
        "안내 문구",
        value=result["message"],
        height=90,
        disabled=True,
    )

    # 브라우저에서 직접 읽어 주는 기능 대신,
    # 시연용 안내 문구를 화면에 표시합니다.
    st.caption(
        "현재 버전은 안내 문구 표시까지만 구현되어 있습니다. "
        "실제 음성 재생은 별도로 연결해야 합니다."
    )

# -----------------------------
# 다시 테스트
# -----------------------------
st.divider()

if st.button("🔄 테스트 결과 초기화", width="stretch"):
    st.session_state.pop("prototype_bus_result", None)
    st.rerun()

# -----------------------------
# 하단 안내
# -----------------------------
with st.expander("ℹ️ 프로토타입 안내"):
    st.markdown(
        """
        - **사진 촬영:** 카메라 화면을 표시합니다.
        - **사진 업로드:** 저장된 사진을 선택할 수 있습니다.
        - **테스트 결과:** 미리 설정된 가짜 버스 번호를 표시합니다.
        - **인식 실패 시나리오:** 번호를 확인하지 못한 상황을 시연합니다.

        이 버전은 화면과 사용자 흐름을 시연하기 위한 프로토타입입니다.
        실제 버스 번호 인식 기능은 포함되어 있지 않습니다.
        """
    )
```
