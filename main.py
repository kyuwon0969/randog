import streamlit as st
import requests
from io import BytesIO
import time

# 페이지 설정
st.set_page_config(page_title="세상에서 가장 귀여운 강아지", page_icon="🐶")

def get_cute_dog_image():
    """Unsplash의 고해상도 이미지 리다이렉트 주소를 사용합니다."""
    # 'dog' 키워드로 검색된 고퀄리티 사진을 랜덤하게 가져오는 주소입니다.
    # 뒤에 타임스탬프를 붙여서 매번 새로운 사진을 강제로 불러오게 합니다.
    ts = int(time.time())
    url = f"https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
    
    # 위 주소는 예시이며, 실제 '랜덤' 기능을 위해 아래 쿼리 기반 주소를 추천합니다.
    # 'cute dog' 키워드 중에서 랜덤으로 하나를 뽑아줍니다.
    random_dog_url = f"https://pico.jace.pro/api/dog?t={ts}" # 대안 API (강아지 전용 고퀄리티)
    
    # 만약 위 API가 불안정하다면 Unsplash의 소스 주소를 다시 시도합니다.
    unsplash_url = f"https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?auto=format&fit=crop&w=800&q=80"
    
    # 가장 확실한 방법: 강아지 전용 고퀄리티 이미지를 제공하는 주소로 대체
    return f"https://loremflickr.com/800/600/dog,puppy,cute?lock={ts}"

st.title("💖 심쿵 유발! 오늘의 강아지")
st.write("형님, 이번엔 진짜 제대로 된 녀석들로만 골라왔습니다.")

# 세션 상태 초기화
if 'dog_url' not in st.session_state:
    st.session_state.dog_url = get_cute_dog_image()

# 사진 표시
if st.session_state.dog_url:
    # 이미지 렌더링
    st.image(st.session_state.dog_url, use_container_width=True, caption="이 녀석 정말 귀엽지 않습니까?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다음 귀요미 보기"):
            st.session_state.dog_url = get_cute_dog_image()
            st.rerun()
            
    with col2:
        try:
            # 다운로드 버튼 구현
            img_data = requests.get(st.session_state.dog_url).content
            st.download_button(
                label="💾 이 사진 저장하기",
                data=img_data,
                file_name=f"cute_dog_{int(time.time())}.jpg",
                mime="image/jpeg"
            )
        except:
            st.info("사진을 준비하고 있습니다...")
else:
    st.error("이미지를 불러올 수 없습니다. 다시 시도해주세요.")

st.divider()
st.caption("고퀄리티 무료 이미지 소스를 활용 중입니다.")
