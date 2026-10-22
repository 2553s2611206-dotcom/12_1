
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
                "message": "사진 용량이 10MB를 초과합니다. 더 작은 사진을 사용해 주세요.",
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
                        "Gemini API 키가 유효하지 않습니다. "
                        "Streamlit Cloud의 Secrets 설정을 확인해 주세요."
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
