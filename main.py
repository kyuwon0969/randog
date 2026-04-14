import streamlit as st
import requests
from io import BytesIO
import time

# 페이지 설정
st.set_page_config(page_title="RANDOG : 랜덤 강아지 사진", page_icon="🐶")

def get_cute_dog_data(breed_keyword):
    """이미지 URL과 실제 데이터(바이너리)를 한꺼번에 가져옵니다."""
    ts = int(time.time())
    search_query = f"{breed_keyword},puppy,cute"
    url = f"https://loremflickr.com/800/600/{search_query}?lock={ts}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content  # 이미지 바이너리 데이터 자체를 리턴
    except:
        return None
    return None

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

selected_name = st.sidebar.selectbox("견종을 선택하세요", list(breed_options.keys()), index=0)
selected_breed = breed_options[selected_name]

# --- 사진 데이터 관리 (세션 상태) ---
# 핵심: 이미지 바이너리 데이터를 세션에 저장해서 재사용합니다.
if 'current_img_data' not in st.session_state or st.session_state.get('last_breed') != selected_breed:
    st.session_state.last_breed = selected_breed
    st.session_state.current_img_data = get_cute_dog_data(selected_breed)

# --- 메인 화면 ---
st.subheader(f"지금 보고 계신 견종: {selected_name}")

if st.session_state.current_img_data:
    # 1. 화면에 이미지 표시 (저장된 데이터를 그대로 사용)
    st.image(st.session_state.current_img_data, use_container_width=True, caption=f"이 {selected_name} 정말 귀엽죠?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 새로운 사진 불러오기
        if st.button("🔄 다른 사진 보기"):
            st.session_state.current_img_data = get_cute_dog_data(selected_breed)
            st.rerun()
            
    with col2:
        # 2. 다운로드 버튼 (이미 세션에 저장된 데이터를 그대로 다운로드)
        st.download_button(
            label="💾 이 사진 그대로 저장",
            data=st.session_state.current_img_data,
            file_name=f"{selected_breed}_{int(time.time())}.jpg",
            mime="image/jpeg"
        )
else:
    st.error("사진을 가져오지 못했습니다. 새로고침을 눌러주세요.")

st.divider()
st.caption(f"본 서비스는 {selected_name}의 고퀄리티 무료 이미지를 실시간으로 제공합니다.")
