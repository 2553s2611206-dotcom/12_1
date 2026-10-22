
import html
import json
import os
import re
import hashlib

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="버스 번호 카메라 인식",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #F4F8FC; }
    .main .block-container {
        max-width: 760px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: #123B64;
        color: white;
        padding: 26px 22px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero h1 { font-size: 30px; margin: 0 0 10px 0; }
    .hero p { font-size: 17px; margin: 0; line-height: 1.6; }
    .number-card {
        background: white;
        border: 2px solid #D5E5F5;
        border-radius: 18px;
        padding: 24px 12px;
        text-align: center;
        margin: 12px 0;
    }
    .bus-number {
        font-size: 54px;
        font-weight: 800;
        color: #123B64;
        overflow-wrap: anywhere;
    }
    div.stButton > button {
        min-height: 52px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 650;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🚌 버스 번호 카메라 인식</h1>
      <p>버스 앞면을 촬영하면 번호를 읽어 드립니다.<br>
      천천히, 안전하게 이용해 주세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Gemini API
# -----------------------------
def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GEMINI_API_KEY", "")


@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)


def recognize_bus_number(image_bytes, mime_type):
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다. "
            "Streamlit Cloud의 Secrets 설정을 확인해 주세요."
        )

    if mime_type not in (
        "image/jpeg", "image/png", "image/webp"
    ):
        raise RuntimeError(
            "JPG, PNG 또는 WEBP 이미지 파일을 사용해 주세요."
        )

    client = get_gemini_client(api_key)

    prompt = """
당신은 시각장애인을 돕는 버스 번호 판독 도우미입니다.
버스 전면 또는 측면에 표시된 노선 번호만 판독하세요.
차량 번호판, 광고, 사람, 정류장 표지판의 숫자는 제외하세요.
번호가 흐리거나 여러 버스 중 대상을 구별할 수 없다면
추측하지 말고 null을 반환하세요.

JSON 객체만 반환하세요.
판독 성공 예시:
{"bus_number":"152","confidence":"high"}

판독 불가 예시:
{"bus_number":null,"confidence":"low"}

confidence는 high, medium, low 중 하나여야 합니다.
high는 번호를 명확하게 읽었을 때만 사용하세요.
"""

    try:
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
    except Exception as exc:
        print(f"Gemini API error: {type(exc).__name__}: {exc}")
        raise RuntimeError(
            "Gemini API 요청에 실패했습니다. API 키, 모델 접근 권한, "
            "인터넷 연결 및 API 사용량을 확인해 주세요."
        ) from exc

    if not response.text:
        raise RuntimeError("AI가 판독 결과를 반환하지 않았습니다.")

    try:
        result = json.loads(response.text)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("AI 응답을 해석하지 못했습니다.") from exc

    if not isinstance(result, dict):
        return None, "low"

    number = result.get("bus_number")
    confidence = result.get("confidence", "low")

    if not isinstance(number, str):
        return None, "low"

    number = number.strip()

    if (
        not number
        or len(number) > 12
        or not re.fullmatch(r"[0-9A-Za-z가-힣-]+", number)
        or not re.search(r"\d", number)
    ):
        return None, "low"

    if confidence not in ("high", "medium", "low"):
        confidence = "low"

    return number, confidence


# -----------------------------
# 음성 안내
# -----------------------------
def speak(text, key="bus_voice"):
    safe_text = json.dumps(text, ensure_ascii=False)

    components.html(
        f"""
        <div style="font-family:sans-serif;text-align:center;">
          <button id="speakBtn"
            style="width:100%;min-height:52px;padding:12px;
            font-size:18px;font-weight:bold;border:0;
            border-radius:12px;background:#123B64;color:white;">
            🔊 안내 다시 듣기
          </button>
          <p id="voiceStatus" role="status">
            음성 안내를 들으려면 버튼을 누르세요.
          </p>
        </div>
        <script>
          const message = {safe_text};
          const btn = document.getElementById("speakBtn");
          const status = document.getElementById("voiceStatus");

          btn.addEventListener("click", function() {{
            if (!("speechSynthesis" in window)) {{
              status.textContent =
                "이 브라우저는 음성 안내를 지원하지 않습니다.";
              return;
            }}

            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.lang = "ko-KR";
            utterance.rate = 0.9;

            utterance.onstart = function() {{
              status.textContent = "음성 안내 중입니다.";
            }};
            utterance.onerror = function() {{
              status.textContent = "음성 안내에 실패했습니다.";
            }};

            window.speechSynthesis.speak(utterance);
          }});
        </script>
        """,
        height=125,
        key=key,
    )


# -----------------------------
# 사용 안내
# -----------------------------
with st.expander("📖 사용 방법", expanded=True):
    st.markdown(
        """
        1. 안전한 위치에서 버스를 향합니다.
        2. 카메라로 촬영하거나 사진을 업로드합니다.
        3. 버스 번호 확인하기 버튼을 누릅니다.
        4. 결과를 확인하고 음성 안내 버튼을 누릅니다.
        """
    )

st.warning(
    "차도에 들어가거나 움직이는 버스를 쫓아가며 촬영하지 마세요. "
    "인식 결과는 실제 노선과 다를 수 있으므로 탑승 전에 확인하세요."
)


# -----------------------------
# 카메라 / 사진 업로드
# -----------------------------
st.subheader("📷 버스 촬영")

camera_image = st.camera_input(
    "버스 전면의 번호 표시를 촬영하세요",
    key="bus_camera",
)

uploaded_image = st.file_uploader(
    "또는 버스 사진을 선택하세요",
    type=["jpg", "jpeg", "png", "webp"],
    help="번호 표시가 선명하게 보이는 사진을 선택하세요.",
    key="bus_upload",
)

image_source = (
    camera_image
    if camera_image is not None
    else uploaded_image
)

if image_source is not None:
    current_bytes = image_source.getvalue()
    fingerprint = hashlib.sha256(current_bytes).hexdigest()

    if fingerprint != st.session_state.get("image_fingerprint"):
        st.session_state.pop("bus_result", None)
        st.session_state["image_fingerprint"] = fingerprint

    st.image(
        image_source,
        caption="선택한 버스 사진",
        use_container_width=True,
    )
else:
    st.session_state.pop("image_fingerprint", None)
    st.session_state.pop("bus_result", None)

st.markdown("---")


# -----------------------------
# 판독 실행
# -----------------------------
if st.button("🔎 버스 번호 확인하기", type="primary"):
    if image_source is None:
        st.session_state["bus_result"] = {
            "status": "retry",
            "message": "먼저 버스 사진을 촬영하거나 업로드해 주세요.",
        }
    else:
        image_bytes = image_source.getvalue()
        mime_type = image_source.type or "image/jpeg"

        if len(image_bytes) > 10 * 1024 * 1024:
            st.session_state["bus_result"] = {
                "status": "retry",
                "message": "사진 용량은 10MB 이하여야 합니다.",
            }
        else:
            try:
                with st.spinner("버스 번호를 확인하고 있습니다..."):
                    number, confidence = recognize_bus_number(
                        image_bytes, mime_type
                    )

                if number is None or confidence != "high":
                    st.session_state["bus_result"] = {
                        "status": "retry",
                        "message": (
                            "버스 번호를 확실하게 확인하지 못했습니다. "
                            "번호 표시가 크게 보이도록 다시 촬영해 주세요."
                        ),
                    }
                else:
                    st.session_state["bus_result"] = {
                        "status": "success",
                        "number": number,
                    }

            except Exception as exc:
                error_type = type(exc).__name__
                error_text = str(exc)
                print(
                    f"Bus recognition error: {error_type}: {error_text}"
                )

                if "GEMINI_API_KEY가 설정되지 않았습니다" in error_text:
                    message = error_text
                elif (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):
                    message = (
                        "Gemini API 사용 한도에 도달했습니다. "
                        "API 사용량을 확인해 주세요."
                    )
                elif (
                    "API key" in error_text
                    or "API_KEY_INVALID" in error_text
                    or "401" in error_text
                ):
                    message = (
                        "API 키가 유효하지 않습니다. "
                        "Streamlit Secrets 설정을 확인해 주세요."
                    )
                else:
                    message = (
                        f"번호 인식 중 오류가 발생했습니다 ({error_type}). "
                        "Manage app → Logs에서 상세 오류를 확인해 주세요."
                    )

                st.session_state["bus_result"] = {
                    "status": "error",
                    "message": message,
                }


# -----------------------------
# 판독 결과
# -----------------------------
result = st.session_state.get("bus_result")

if result:
    st.markdown("---")
    st.subheader("📢 안내 결과")

    if result["status"] == "success":
        number = result["number"]
        safe_number = html.escape(number)

        st.markdown(
            f"""
            <div class="number-card">
              <div style="font-size:19px;color:#333;">
                인식된 버스 번호
              </div>
              <div class="bus-number">{safe_number}</div>
              <div style="font-size:21px;color:#123B64;font-weight:700;">
                {safe_number}번 버스입니다.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        speak(
            f"{number}번 버스입니다.",
            key="success_voice",
        )

    elif result["status"] == "retry":
        st.error("🔁 다시 촬영해 주세요")
        st.markdown(result["message"])
        st.info(
            "번호 표시를 화면 중앙에 두고 흔들림과 빛 반사를 줄여 주세요."
        )
        speak(result["message"], key="retry_voice")

    else:
        st.error("확인 중 문제가 발생했습니다.")
        st.write(result["message"])

    if st.button("🔄 다른 버스 확인하기"):
        st.session_state.pop("bus_result", None)
        st.session_state.pop("image_fingerprint", None)
        st.rerun()


st.markdown("---")
st.caption(
    "버스 번호 카메라 인식 | 시각장애인을 위한 보조 도구 "
    "| 인식 결과는 실제 노선과 다를 수 있습니다."
)
