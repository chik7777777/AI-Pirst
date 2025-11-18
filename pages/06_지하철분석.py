import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data
def load_data():
return pd.read_csv('../subway.csv', encoding='cp949')


df = load_data()


st.title("🚇 2025년 10월 지하철 이용량 분석")


unique_dates = sorted(df['사용일자'].unique())
unique_lines = sorted(df['노선명'].unique())


selected_date = st.selectbox("📅 날짜를 선택하세요", unique_dates)
selected_line = st.selectbox("🚉 호선을 선택하세요", unique_lines)


filtered_df = df[(df['사용일자'] == selected_date) & (df['노선명'] == selected_line)].copy()
filtered_df['총이용객수'] = filtered_df['승차총승객수'] + filtered_df['하차총승객수']
filtered_df = filtered_df.sort_values('총이용객수', ascending=False)


colors = ['red'] + [f'rgba(0,0,255,{opacity})' for opacity in np.linspace(1, 0.2, len(filtered_df)-1)]


fig = px.bar(
filtered_df,
x='역명',
y='총이용객수',
title=f"{selected_line} {selected_date} 역별 총 이용객수 순위",
)
fig.update_traces(marker_color=colors)
fig.update_layout(xaxis_title="역명", yaxis_title="총 이용객수")


st.plotly_chart(fig, use_container_width=True)
