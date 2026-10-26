# pages/카메라 인식 시스템.py

import json
import re
import streamlit as st
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="버스 번호 카메라 인식",
    page_icon="🚌",
    layout="centered",
)

MODEL_NAME = "gemini-3.5-flash-lite"

st.title("🚌 버스 번호 카메라 인식")
st.write(
    "카메라로 버스를 촬영하면 버스 번호를 확인하고 "
    "음성으로 알려주는 기능입니다."
)

st.info(
    "버스 번호가 잘 보이도록 촬영해 주세요. "
    "번호를 정확히 확인할 수 없으면 다시 촬영해 주세요."
)

# -----------------------------
# 음성 안내
# -----------------------------
def speak(text: str):
    """브라우저의 한국어 음성 합성 기능으로 안내합니다."""
    safe_text = json.dumps(str(text), ensure_ascii=False)

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    <script>
        const message = {safe_text};

        if ("speechSynthesis" in window) {{
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(message);
            utterance.lang = "ko-KR";
            utterance.rate = 0.9;
            utterance.pitch = 1.0;

            window.speechSynthesis.speak(utterance);
        }}
    </script>
    </body>
    </html>
    """

    # components.html 대신 최신 Streamlit의 st.iframe 사용
    st.iframe(
        html,
        height=50,
        width="stretch",
        scrolling=False,
    )


# -----------------------------
# Gemini API 연결
# -----------------------------
def get_gemini_client():
    """Streamlit Secrets에서 API 키를 불러옵니다."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GEMINI_API_KEY를 찾을 수 없습니다. "
            "Streamlit 앱의 Settings → Secrets에 API 키를 등록해 주세요."
        )

    if not api_key or not str(api_key).strip():
        raise RuntimeError(
            "GEMINI_API_KEY 값이 비어 있습니다. API 키를 확인해 주세요."
        )

    return genai.Client(api_key=str(api_key).strip())


# -----------------------------
# 버스 번호 인식
# -----------------------------
def recognize_bus(image: Image.Image) -> dict:
    """사진 속 버스 번호를 Gemini API로 분석합니다."""
    client = get_gemini_client()

    prompt = """
당신은 시각장애인을 돕는 버스 번호 인식 도우미입니다.

입력된 사진을 분석하고, 사진에 실제로 보이는 정보만 사용하세요.

다음 규칙을 지키세요.
1. 버스의 외부에 표시된 노선 번호를 찾아보세요.
2. 번호가 불분명하거나 사진에 버스가 없다면 추측하지 마세요.
3. 버스 번호와 차량 번호, 광고 속 숫자를 혼동하지 마세요.
4. 노선 번호를 확실하게 읽을 수 있을 때만 인식 성공으로 처리하세요.
5. 아래 JSON 형식으로만 답하세요. 마크다운 코드 블록은 사용하지 마세요.

인식 성공 예시:
{
  "recognized": true,
  "bus_number": "273",
  "message": "273번 버스입니다."
}

인식 실패 예시:
{
  "recognized": false,
  "bus_number": "",
  "message": "버스 번호를 정확히 확인할 수 없습니다. 카메라를 버스 번호 쪽으로 다시 맞춰 주세요."
}
"""

    # 이미지의 EXIF 방향 정보를 반영합니다.
    image = image.convert("RGB")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            image,
        ],
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )

    response_text = response.text

    if not response_text:
        raise RuntimeError(
            "AI가 결과를 반환하지 않았습니다. 다시 시도해 주세요."
        )

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # 모델이 JSON 이외의 내용을 반환했을 때를 대비합니다.
        match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if not match:
            raise RuntimeError(
                "AI 응답을 읽을 수 없습니다. 다시 촬영해 주세요."
            )

        try:
            result = json.loads(match.group(0))
        except json.JSONDecodeError:
            raise RuntimeError(
                "AI 응답 형식이 올바르지 않습니다. 다시 시도해 주세요."
            )

    recognized = result.get("recognized") is True
    bus_number = str(result.get("bus_number", "")).strip()
    message = str(result.get("message", "")).strip()

    if not message:
        if recognized and bus_number:
            message = f"{bus_number}번 버스입니다."
        else:
            message = (
                "버스 번호를 정확히 확인할 수 없습니다. "
                "카메라를 버스 번호 쪽으로 다시 맞춰 주세요."
            )

    # 번호가 비어 있으면 성공으로 처리하지 않습니다.
    if not bus_number:
        recognized = False

    return {
        "recognized": recognized,
        "bus_number": bus_number,
        "message": message,
    }


# -----------------------------
# 카메라 및 이미지 업로드
# -----------------------------
st.subheader("📷 버스 사진 촬영")

camera_image = st.camera_input(
    "버스 번호가 보이도록 카메라를 맞춰 주세요",
)

st.write("또는 이미 촬영한 사진을 업로드할 수 있습니다.")

uploaded_image = st.file_uploader(
    "버스 사진 선택",
    type=["jpg", "jpeg", "png", "webp"],
)

# 카메라 사진이 있으면 카메라 사진을 우선 사용합니다.
selected_file = camera_image if camera_image is not None else uploaded_image

if selected_file is not None:
    try:
        image_bytes = selected_file.getvalue()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        st.image(
            image,
            caption="선택한 버스 사진",
            width="stretch",
        )

        st.caption(
            "번호가 작거나 흐릿하면 가까이에서 다시 촬영해 주세요."
        )

        if st.button(
            "🔍 버스 번호 인식하기",
            type="primary",
            width="stretch",
        ):
            with st.spinner("사진에서 버스 번호를 확인하고 있습니다..."):
                try:
                    result = recognize_bus(image)

                    st.session_state["bus_result"] = result
                    st.session_state["bus_result_error"] = None

                except Exception as error:
                    st.session_state["bus_result"] = None
                    st.session_state["bus_result_error"] = str(error)

    except Exception as error:
        st.error("이미지를 열 수 없습니다. 다른 사진을 선택해 주세요.")
        st.caption(f"오류 내용: {error}")


# -----------------------------
# 인식 결과
# -----------------------------
if st.session_state.get("bus_result_error"):
    st.error("버스 번호를 확인하는 중 문제가 발생했습니다.")

    error_text = st.session_state["bus_result_error"]
    st.code(error_text)

    st.warning(
        "오류가 계속되면 Streamlit Secrets의 API 키, "
        "Gemini API 사용 가능 여부, 모델 이름을 확인해 주세요."
    )

    if "404" in error_text or "NOT_FOUND" in error_text:
        st.info(
            "Gemini에서 모델을 찾지 못했거나 해당 모델을 사용할 수 없는 "
            "상태일 수 있습니다. 모델 이름과 API 접근 권한을 확인해 주세요."
        )

    if "403" in error_text or "PERMISSION_DENIED" in error_text:
        st.info(
            "API 키의 권한 또는 프로젝트 설정을 확인해 주세요."
        )

    if "API_KEY_INVALID" in error_text or "API key not valid" in error_text:
        st.info(
            "API 키가 올바른지 확인해 주세요. API 키를 다른 사람에게 공개하지 마세요."
        )

elif st.session_state.get("bus_result"):
    result = st.session_state["bus_result"]

    st.divider()
    st.subheader("📢 인식 결과")

    if result["recognized"]:
        st.success("버스 번호를 확인했습니다.")

        st.markdown(
            f"## 🚌 {result['bus_number']}번 버스"
        )

        st.write(result["message"])

        if st.button(
            "🔊 음성으로 다시 듣기",
            width="stretch",
        ):
            speak(result["message"])

    else:
        st.warning(result["message"])

        if st.button(
            "🔊 안내 다시 듣기",
            width="stretch",
        ):
            speak(result["message"])

        st.caption(
            "번호가 잘 보이도록 카메라 방향을 바꾼 후 다시 시도해 주세요."
        )


# -----------------------------
# 사용 방법
# -----------------------------
with st.expander("ℹ️ 사용 방법"):
    st.markdown(
        """
        1. 버스의 앞면이나 옆면에 표시된 노선 번호를 촬영합니다.
        2. **버스 번호 인식하기** 버튼을 누릅니다.
        3. 인식된 번호와 음성 안내를 확인합니다.
        4. 번호가 불분명하면 다시 촬영합니다.

        **주의:** 사진 인식은 틀릴 수 있습니다. 실제로 버스에 탑승하기 전
        안내된 번호를 가능한 범위에서 한 번 더 확인해 주세요.
        """
    )
