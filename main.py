import streamlit as st
st.title('안녕하십니까 이곳은 저의 처음입니다.^v^')
name=st.text_input('이름을 입력해주세요.^ㅇ^')
m=st.selectbox('좋아하는 음식을 선택해주세요.^o^',['치킨','떡볶이','규카츠','찜닭'])
if st.button('인사말 생성'):
  st.info(name+'님 하요!!!>v<')
  st.warning(m+'을 좋아하시는군요. 저도 좋아해요!>_<')
  st.error('반갑습니당~!^~^')
  st.chicken()
