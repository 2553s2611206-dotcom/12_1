
import base64
import json
import os
import re

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
    .stApp {
        background-color: #F4F8FC;
    }
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
    .hero h1 {
        font-size: 30px;
        margin: 0 0 10px 0;
    }
    .hero p {
        font-size: 17px;
        margin: 0;
        line-height: 1.6;
    }
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
# Gemini 클라이언트
# -----------------------------
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def recognize_bus_number(image_bytes, mime_type):
    """이미지에서 실제 버스 번호 표시를 판독한다."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "API 키가 설정되지 않았습니다. "
            "Streamlit Secrets에 GEMINI_API_KEY를 등록해 주세요."
        )

    client = genai.Client(api_key=api_key)

    prompt = """
당신은 시각장애인을 돕는 버스 번호 판독 도우미입니다.

이미지에서 버스 전면 또는 측면의 노선 번호 표시를 확인하세요.
사람, 광고, 차량 번호판, 정류장 표지판의 숫자를 버스 노선 번호로
잘못 판단하지 마세요.

명확하게 읽을 수 있는 버스 노선 번호가 하나 있을 때만 해당 번호를
반환하세요. 이미지가 흐리거나 번호가 보이지 않으면 null을 반환하세요.
여러 버스가 있거나 어느 버스의 번호인지 불확실하면 null을 반환하세요.
번호를 추측하거나 만들어 내지 마세요.

반드시 다음 JSON 형식으로만 답하세요.
{"bus_number": "152", "confidence": "high"}
번호를 판독할 수 없으면:
{"bus_number": null, "confidence": "low"}

bus_number에는 실제 이미지에서 확인한 번호만 넣으세요.
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
        raise RuntimeError("AI가 판독 결과를 반환하지 않았습니다.")

    try:
        result = json.loads(response.text)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("판독 결과를 해석하지 못했습니다.") from exc

    number = result.get("bus_number")
    confidence = result.get("confidence", "low")

    # 잘못된 값이나 이미지 속 임의 문장이 결과에 들어오는 것을 방지
    if not isinstance(number, str):
        return None, "low"

    number = number.strip()

    if not number or len(number) > 12:
        return None, "low"

    # 버스 번호는 숫자와 한글/영문 지역 접두어 등만 허용
    if not re.fullmatch(r"[0-9A-Za-z가-힣-]+", number):
        return None, "low"

    if not re.search(r"\d", number):
        return None, "low"

    if confidence not in ("high", "medium", "low"):
        confidence = "low"

    return number, confidence


# -----------------------------
# 음성 안내
# -----------------------------
def speak(text):
    """브라우저에서 한국어 음성 합성을 시도한다."""
    safe_text = json.dumps(text, ensure_ascii=False)

    components.html(
        f"""
        <div style="font-family:sans-serif; text-align:center;">
          <button id="speakBtn"
            style="width:100%;padding:14px;font-size:18px;
            font-weight:bold;border:0;border-radius:12px;
            background:#123B64;color:white;cursor:pointer;">
            🔊 안내 다시 듣기
          </button>
          <p id="voiceStatus" style="font-size:14px;color:#333;">
            음성 안내 버튼을 눌러 주세요.
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
              status.textContent =
                "음성 안내를 시작할 수 없습니다. 버튼을 다시 눌러 주세요.";
            }};

            window.speechSynthesis.speak(utterance);
          }});
        </script>
        """,
        height=115,
    )


# -----------------------------
# 사용 안내
# -----------------------------
with st.expander("📖 사용 방법", expanded=True):
    st.markdown(
        """
        1. 가능한 안전한 위치에서 정차한 버스를 향합니다.
        2. 아래 카메라를 열거나 버스 사진을 업로드합니다.
        3. **버스 번호 확인하기** 버튼을 누릅니다.
        4. 결과를 확인하고 음성 안내 버튼을 누릅니다.
        5. 번호가 보이지 않으면 위치를 조정한 뒤 다시 촬영합니다.
        """
    )

st.warning(
    "안전을 위해 차도에 들어서거나 움직이는 버스를 쫓아가며 "
    "촬영하지 마세요. 번호가 불확실하면 탑승 전에 기사님이나 "
    "주변 사람에게 확인하세요."
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
)

image_source = uploaded_image if uploaded_image is not None else camera_image

if image_source is not None:
    st.image(
        image_source,
        caption="선택한 버스 사진",
        use_container_width=True,
    )

st.markdown("---")

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
                "message": "사진 용량이 너무 큽니다. 10MB 이하의 사진을 사용해 주세요.",
            }
        else:
            try:
                with st.spinner("버스 번호를 확인하고 있습니다..."):
                    number, confidence = recognize_bus_number(
                        image_bytes,
                        mime_type,
                    )

                if number is None or confidence != "high":
                    st.session_state["bus_result"] = {
                        "status": "retry",
                        "message": (
                            "버스 번호를 확실하게 확인하지 못했습니다. "
                            "버스 전면의 번호 표시가 크게 보이도록 "
                            "다시 촬영해 주세요."
                        ),
                    }
                else:
                    st.session_state["bus_result"] = {
                        "status": "success",
                        "number": number,
                    }

            except Exception as exc:
                # 실제 API 키나 내부 오류 정보를 화면에 노출하지 않는다.
                error_text = str(exc)
                if "API 키가 설정되지 않았습니다" in error_text:
                    message = error_text
                else:
                    message = (
                        "번호를 확인하는 중 오류가 발생했습니다. "
                        "인터넷 연결을 확인한 후 다시 시도해 주세요. "
                        "문제가 반복되면 API 키와 사용량 제한을 확인해 주세요."
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

        st.markdown(
            f"""
            <div class="number-card">
              <div style="font-size:19px;color:#333;">
                인식된 버스 번호
              </div>
              <div class="bus-number">{number}</div>
              <div style="font-size:21px;color:#123B64;font-weight:700;">
                {number}번 버스입니다.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        speak(f"{number}번 버스입니다.")

        if st.button("🔄 다른 버스 확인하기"):
            st.session_state.pop("bus_result", None)
            st.rerun()

    elif result["status"] == "retry":
        st.error("🔁 다시 촬영해 주세요")
        st.markdown(f"### {result['message']}")
        st.info(
            "번호 표시가 화면 중앙에 오도록 하고, "
            "흔들림과 빛 반사를 줄여 촬영해 주세요."
        )

        speak(result["message"])

    else:
        st.error("확인 중 문제가 발생했습니다.")
        st.write(result["message"])

st.markdown("---")
st.caption(
    "버스 번호 카메라 인식 | 시각장애인을 위한 보조 도구 "
    "| 인식 결과는 실제 노선과 다를 수 있습니다."
)

