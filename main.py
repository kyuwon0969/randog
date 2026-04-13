import streamlit as st
import requests
from io import BytesIO
import time

# 페이지 설정
st.set_page_config(page_title="견종별 귀요미 모음", page_icon="🐶")

def get_cute_dog_image(breed_keyword):
    """선택된 견종 키워드를 사용하여 고퀄리티 이미지를 가져옵니다."""
    ts = int(time.time())
    # 검색어에 'cute', 'puppy'를 조합해서 더 귀여운 사진이 나올 확률을 높입니다.
    search_query = f"{breed_keyword},puppy,cute"
    return f"https://loremflickr.com/800/600/{search_query}?lock={ts}"

st.title("RANDOG : 랜덤 강아지 사진 사이트")

# --- 사이드바: 견종 선택 ---
st.sidebar.header("🐾 어떤 강아지를 볼까요?")
breed_options = {
    "포메라니안": "pomeranian",
    "골든 리트리버": "retriever",
    "시바견": "shiba",
    "푸들": "poodle",
    "말티즈": "maltese",
    "비숑 프리제": "bichon",
    "랜덤 모두보기": "dog"
}

# 사용자 선택 (기본값은 포메라니안으로 해뒀습니다, 형님!)
selected_name = st.sidebar.selectbox("견종을 선택하세요", list(breed_options.keys()), index=0)
selected_breed = breed_options[selected_name]

# 견종이 바뀌면 사진도 새로 가져오기 위해 세션 상태 관리
if 'current_breed' not in st.session_state:
    st.session_state.current_breed = selected_breed
    st.session_state.dog_url = get_cute_dog_image(selected_breed)

# 만약 사이드바에서 견종을 바꾸면 즉시 업데이트
if st.session_state.current_breed != selected_breed:
    st.session_state.current_breed = selected_breed
    st.session_state.dog_url = get_cute_dog_image(selected_breed)

# --- 메인 화면 ---
st.subheader(f"지금 보고 계신 견종: {selected_name}")

if st.session_state.dog_url:
    st.image(st.session_state.dog_url, use_container_width=True, caption=f"정말 사랑스러운 {selected_name} 아닙니까?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다른 사진 보기"):
            st.session_state.dog_url = get_cute_dog_image(selected_breed)
            st.rerun()
            
    with col2:
        try:
            # 다운로드 버튼
            img_data = requests.get(st.session_state.dog_url).content
            st.download_button(
                label="💾 이 사진 저장",
                data=img_data,
                file_name=f"{selected_breed}_{int(time.time())}.jpg",
                mime="image/jpeg"
            )
        except:
            st.info("사진 로딩 중...")
else:
    st.error("사진을 가져오지 못했습니다.")

st.divider()
st.caption(f"본 서비스는 {selected_name}의 고퀄리티 무료 이미지를 실시간으로 제공합니다.")
