import streamlit as st
import requests
from io import BytesIO
import random

# 페이지 설정
st.set_page_config(page_title="세상에서 가장 귀여운 강아지", page_icon="🐶")

def get_cute_dog_image():
    """Unsplash API를 활용해 고퀄리티 강아지 사진을 가져옵니다."""
    # 별도의 API 키 없이도 소스 URL을 통해 '강아지(dog)', '귀여운(cute)' 태그가 달린 사진을 불러옵니다.
    # 뒤에 랜덤 숫자를 붙여야 새로고침 시 진짜로 새로운 사진이 옵니다.
    random_id = random.randint(1, 10000)
    url = f"https://source.unsplash.com/featured/?dog,puppy,cute&sig={random_id}"
    return url

st.title("💖 심쿵 유발! 오늘의 강아지")
st.write("형님, 오늘은 보기만 해도 힐링되는 예쁜 강아지들만 모셔왔습니다.")

# 세션 상태에 이미지 URL 저장
if 'dog_url' not in st.session_state:
    st.session_state.dog_url = get_cute_dog_image()

# 사진 표시 구역
if st.session_state.dog_url:
    # Unsplash 이미지는 고화질이라 로딩 시간이 있을 수 있어 placeholder를 사용하면 좋습니다.
    st.image(st.session_state.dog_url, use_container_width=True, caption="이 녀석 정말 귀엽지 않습니까?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다음 귀요미 보기"):
            st.session_state.dog_url = get_cute_dog_image()
            st.rerun()
            
    with col2:
        try:
            # 이미지 다운로드를 위해 실제 이미지 데이터를 가져옵니다.
            img_response = requests.get(st.session_state.dog_url)
            img_bytes = BytesIO(img_response.content)
            
            st.download_button(
                label="💾 이 사진은 소장해야 돼!",
                data=img_bytes,
                file_name="cute_dog.jpg",
                mime="image/jpeg"
            )
        except:
            st.write("이미지 준비 중...")

else:
    st.warning("강아지들이 잠시 산책을 갔나 봅니다. 잠시 후 다시 시도해 주세요.")

st.divider()
st.caption("Photo from Unsplash (Free to use under the Unsplash License)")
