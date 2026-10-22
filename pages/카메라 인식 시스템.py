except Exception as exc:
    print(
        f"Unexpected error: {type(exc).__name__}: {exc}"
    )

    st.session_state["bus_result"] = {
        "status": "error",
        "message": (
            "예상하지 못한 오류가 발생했습니다. "
            "잠시 후 다시 시도해 주세요."
        ),
    }
