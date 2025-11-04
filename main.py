import streamlit as st
st.title('안녕하십니까 이곳은 저의 처음입니다.^v^')
name=st.text_input('이름을 입력해주세요.^ㅇ^')
st.selectbox('좋아하는 음식을 선택해주세요.^o^',['치킨','떡볶이','규카츠','찜닭')
if st.button('인사말 생성'):
  st.write(name+'님 하요!!!>v<')
