import streamlit as st
import requests
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="오늘의 랜덤 강아지", page_icon="🐶")

def get_random_dog_image():
    """Dog CEO API에서 랜덤 강아지 사진 URL을 가져옵니다."""
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        if data["status"] == "success":
            return data["message"]
    except Exception as e:
        st.error(f"사진을 불러오는데 실패했습니다: {e}")
    return None

st.title("🐶 오늘의 랜덤 강아지")
st.write("접속할 때마다 새로운 강아지가 형님을 반겨줍니다!")

# 세션 상태에 이미지 URL 저장 (새로고침 전까지 유지)
if 'dog_url' not in st.session_state:
    st.session_state.dog_url = get_random_dog_image()

# 사진 표시 구역
if st.session_state.dog_url:
    st.image(st.session_state.dog_url, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # '새로고침' 버튼
        if st.button("🔄 새로운 사진 보기"):
            st.session_state.dog_url = get_random_dog_image()
            st.rerun()
            
    with col2:
        # '사진 저장' 버튼 (이미지 다운로드 기능)
        try:
            img_response = requests.get(st.session_state.dog_url)
            img_bytes = BytesIO(img_response.content)
            
            st.download_button(
                label="💾 사진 저장 (다운로드)",
                data=img_bytes,
                file_name="random_dog.jpg",
                mime="image/jpeg"
            )
        except:
            st.write("다운로드 준비 중...")

else:
    st.warning("강아지 사진을 가져올 수 없습니다. 인터넷 연결을 확인해 주세요.")

st.divider()
st.caption("Powered by Dog CEO API (Free & Open Source)")
