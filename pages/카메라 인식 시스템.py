
import json
import os
import re

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types


# ==================================================
# 1. 페이지 설정
# ==================================================
st.set_page_config(
    page_title="버스 번호 카메라 인식",
    page_icon="🚌",
    layout="centered",
)

# ==================================================
# 2. 화면 디자인
# ==================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3F7FC;
    }

    .main .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: #123B64;
        color: white;
        padding: 26px 18px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 24px;
    }

    .hero h1 {
        font-size: 30px;
        margin-bottom: 12px;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.6;
    }

    .number-card {
        background: white;
        border: 3px solid #123B64;
        border-radius: 20px;
        padding: 24px 12px;
        margin: 16px 0;
        text-align: center;
    }

    .number {
        font-size: 52px;
        font-weight: 900;
        color: #123B64;
        overflow-wrap: anywhere;
    }

    div.stButton > button {
        min-height: 56px;
        font-size: 19px;
        font-weight: 750;
        border-radius: 13px;
    }

    .stAlert {
        font-size: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🚌 버스 번호 카메라 인식</h1>
        <p>
            버스 앞면의 번호를 촬영해 주세요.<br>
            번호를 확인하고 음성 안내를 받을 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 3. API 키 확인
# ==================================================
def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    return os.environ.get("GEMINI_API_KEY", "")


# ==================================================
# 4. 버스 번호 판독
# ==================================================
def recognize_bus_number(image_bytes, mime_type):
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "Gemini API 키가 설정되지 않았습니다. "
            "Streamlit의 Settings → Secrets에서 "
            "GEMINI_API_KEY를 등록해 주세요."
        )

    client = genai.Client(api_key=api_key)

    prompt = """
당신은 시각장애인을 위한 버스 번호 판독 도우미입니다.

이미지에서 버스 전면 또는 측면에 표시된 버스 노선 번호를 찾으세요.

규칙:
1. 차량 번호판, 사람의 옷, 광고, 정류장 표지판에 있는 숫자는
   버스 노선 번호로 판단하지 마세요.
2. 실제 버스에 표시된 노선 번호만 읽으세요.
3. 여러 버스가 있거나 어느 버스의 번호인지 확실하지 않으면
   null을 반환하세요.
4. 숫자가 흐리거나 가려졌다면 추측하지 말고 null을 반환하세요.
5. 이미지에 보이는 번호를 임의로 만들어 내지 마세요.
6. 숫자뿐 아니라 실제로 표시된 노선 번호의 문자도 보존하세요.

반드시 다음 JSON 형식으로만 응답하세요.

{"bus_number": "152", "confidence": "high"}

번호를 확실하게 판독할 수 없으면:

{"bus_number": null, "confidence": "low"}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),
            prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0,
        ),
    )

    if not response.text:
        raise RuntimeError("AI 판독 결과가 비어 있습니다.")

    try:
        result = json.loads(response.text)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("AI 판독 결과를 읽을 수 없습니다.") from exc

    number = result.get("bus_number")
    confidence = result.get("confidence", "low")

    if not isinstance(number, str):
        return None, "low"

    number = number.strip()

    # 번호에 숫자가 반드시 포함되어야 한다.
    # 공백, 코드, HTML 등 예상하지 못한 값은 거부한다.
    if (
        not number
        or len(number) > 15
        or not re.fullmatch(r"[0-9A-Za-z가-힣-]+", number)
        or not re.search(r"\d", number)
    ):
        return None, "low"

    if confidence not in ("high", "medium", "low"):
        confidence = "low"

    return number, confidence


# ==================================================
# 5. 음성 안내
# ==================================================
def speak(text, key=None):
    """
    key 인자는 이전 코드와의 호환성을 위해 받지만,
    components.html()에는 전달하지 않는다.
    """
    safe_text = json.dumps(str(text), ensure_ascii=False)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:sans-serif;">
        <button id="speakBtn"
            style="
                width:100%;
                min-height:54px;
                padding:12px;
                border:0;
                border-radius:12px;
                background:#123B64;
                color:white;
                font-size:19px;
                font-weight:bold;
                cursor:pointer;
            ">
            🔊 음성 안내 다시 듣기
        </button>

        <p id="voiceStatus" aria-live="polite"
            style="font-size:15px;">
            버튼을 눌러 안내를 들으세요.
        </p>

        <script>
        (function() {{
            const message = {safe_text};
            const button = document.getElementById("speakBtn");
            const status = document.getElementById("voiceStatus");

            button.addEventListener("click", function() {{
                if (!("speechSynthesis" in window)) {{
                    status.textContent =
                        "이 브라우저는 음성 안내를 지원하지 않습니다.";
                    return;
                }}

                window.speechSynthesis.cancel();

                const utterance =
                    new SpeechSynthesisUtterance(message);

                utterance.lang = "ko-KR";
                utterance.rate = 0.9;

                utterance.onstart = function() {{
                    status.textContent = "음성 안내 중입니다.";
                }};

                utterance.onend = function() {{
                    status.textContent = "음성 안내가 끝났습니다.";
                }};

                utterance.onerror = function() {{
                    status.textContent =
                        "음성 안내에 실패했습니다. 다시 눌러 주세요.";
                }};

                window.speechSynthesis.speak(utterance);
            }});
        }})();
        </script>
    </body>
    </html>
    """

    # 핵심 수정: key=key를 전달하지 않는다.
    components.html(
        html_code,
        height=125,
        scrolling=False,
    )


# ==================================================
# 6. 사용 방법
# ==================================================
with st.expander("📖 사용 방법", expanded=True):
    st.markdown(
        """
        1. 안전한 장소에서 정차한 버스를 향합니다.
        2. 카메라로 촬영하거나 기존 사진을 선택합니다.
        3. 버스 번호 확인하기 버튼을 누릅니다.
        4. 인식 결과를 확인하고 음성 안내 버튼을 누릅니다.
        5. 번호가 보이지 않으면 다시 촬영합니다.
        """
    )

st.warning(
    "안전을 위해 차도로 들어가거나 움직이는 버스를 쫓아가며 "
    "촬영하지 마세요. 번호가 불확실하면 탑승 전에 다시 확인하세요."
)

# ==================================================
# 7. 사진 촬영 및 업로드
# ==================================================
st.subheader("📷 버스 촬영")

camera_image = st.camera_input(
    "버스 앞면의 번호 표시를 촬영하세요",
    key="bus_camera",
)

uploaded_image = st.file_uploader(
    "또는 사진 파일 선택하기",
    type=["jpg", "jpeg", "png", "webp"],
    help="버스 번호가 선명하게 보이는 사진을 선택하세요.",
)

# 업로드 사진이 있으면 업로드 사진을 사용하고,
# 없으면 카메라로 촬영한 사진을 사용한다.
image_source = (
    uploaded_image
    if uploaded_image is not None
    else camera_image
)

if image_source is not None:
    st.image(
        image_source,
        caption="선택한 버스 사진",
        use_container_width=True,
    )

# ==================================================
# 8. 판독 실행
# ==================================================
if st.button(
    "🔎 버스 번호 확인하기",
    type="primary",
    use_container_width=True,
):
    if image_source is None:
        st.session_state["bus_result"] = {
            "status": "retry",
            "message": (
                "먼저 버스 사진을 촬영하거나 "
                "사진 파일을 선택해 주세요."
            ),
        }
    else:
        image_bytes = image_source.getvalue()
        mime_type = image_source.type or "image/jpeg"

        if len(image_bytes) > 10 * 1024 * 1024:
            st.session_state["bus_result"] = {
                "status": "retry",
                "message": (
                    "사진 용량이 10MB를 초과합니다. "
                    "더 작은 사진으로 다시 시도해 주세요."
                ),
            }
        else:
            try:
                with st.spinner(
                    "사진에서 버스 번호를 확인하고 있습니다..."
                ):
                    number, confidence = recognize_bus_number(
                        image_bytes,
                        mime_type,
                    )

                if number is None or confidence == "low":
                    st.session_state["bus_result"] = {
                        "status": "retry",
                        "message": (
                            "버스 번호를 확실하게 인식하지 못했습니다. "
                            "번호 표시가 화면 중앙에 크게 보이도록 "
                            "다시 촬영해 주세요."
                        ),
                    }
                else:
                    st.session_state["bus_result"] = {
                        "status": "success",
                        "number": number,
                        "confidence": confidence,
                    }

            except Exception as exc:
                error_message = str(exc)

                if "API 키가 설정되지 않았습니다" in error_message:
                    user_message = error_message
                else:
                    user_message = (
                        "버스 번호를 확인하는 중 오류가 발생했습니다. "
                        "인터넷 연결, Gemini API 키, API 사용량을 "
                        "확인한 후 다시 시도해 주세요."
                    )

                st.session_state["bus_result"] = {
                    "status": "error",
                    "message": user_message,
                }

# ==================================================
# 9. 판독 결과
# ==================================================
result = st.session_state.get("bus_result")

if result:
    st.markdown("---")
    st.subheader("📢 안내 결과")

    if result["status"] == "success":
        number = result["number"]

        st.markdown(
            f"""
            <div class="number-card">
                <div style="font-size:20px;color:#222;">
                    인식된 버스 번호
                </div>
                <div class="number">{number}</div>
                <div style="
                    font-size:24px;
                    font-weight:800;
                    color:#123B64;
                ">
                    {number}번 버스입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result.get("confidence") == "medium":
            st.warning(
                "번호 판독의 확신도가 높지 않습니다. "
                "실제 버스 번호를 반드시 다시 확인하세요."
            )

        speak(f"{number}번 버스입니다.", key="success_voice")

    elif result["status"] == "retry":
        st.error("🔁 다시 촬영해 주세요")
        st.markdown(f"### {result['message']}")

        st.info(
            "촬영 팁: 버스 번호 표시가 잘 보이도록 방향을 조정하고, "
            "흔들림과 빛 반사를 줄여 촬영해 주세요."
        )

        speak(result["message"], key="retry_voice")

    elif result["status"] == "error":
        st.error("확인 중 문제가 발생했습니다.")
        st.write(result["message"])

    if st.button(
        "🔄 다른 버스 확인하기",
        use_container_width=True,
    ):
        st.session_state.pop("bus_result", None)
        st.rerun()

# ==================================================
# 10. 하단 안내
# ==================================================
st.markdown("---")

st.caption(
    "버스 번호 카메라 인식 | 시각장애인을 위한 보조 도구 | "
    "인식 결과는 실제 노선과 다를 수 있습니다."
)
