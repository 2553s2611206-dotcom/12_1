
import streamlit as st

st.set_page_config(
    page_title="버스 우선순위 안내",
    page_icon="🚌",
    layout="centered",
)

st.title("🚌 버스 우선순위 안내")
st.caption("시각장애인의 안전하고 편리한 버스 승차를 위한 안내 시스템")

st.divider()

st.subheader("서비스 소개")
st.write(
    """
    여러 대의 버스가 정류장에 동시에 도착하면
    시각장애인은 어떤 버스가 자신이 타려는 버스인지
    알아보기 어려울 수 있습니다.

    이 서비스는 버스의 우선순위와 위치 정보를 활용해
    앞쪽과 뒤쪽에 있는 버스를 구분하고,
    탑승할 버스를 쉽게 찾도록 돕는 것을 목표로 합니다.
    """
)

st.info(
    "왼쪽 메뉴에서 '버스 우선순위 설명' 페이지를 선택하면 "
    "시스템의 원리와 사용법을 확인할 수 있습니다."
)

st.subheader("핵심 기능")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 위치 구분")
    st.write("버스의 상대적인 앞뒤 위치를 구분합니다.")

with col2:
    st.markdown("### 🔢 우선순위")
    st.write("탑승 대상 버스를 우선순위에 따라 식별합니다.")

st.divider()

st.subheader("이용 시 알아둘 점")
st.write(
    "현재 앱은 시스템을 설명하는 안내용 페이지입니다. "
    "실시간 버스 위치 확인과 실제 음성 안내는 별도 연동이 필요합니다."
)

if st.button("버스 우선순위 설명 읽기", use_container_width=True):
    st.switch_page("pages/우선순위.py")
