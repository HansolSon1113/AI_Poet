#pip install python-dotenv, openai, langchain, langchain-openai

#from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
import json

# Settings
st.title('AI Poem Writer')
#load_dotenv()
chatModel = ChatOpenAI()

# Main
sub = st.text_input('시의 주제를 입력하세요: ')
st.markdown(f"<p style='color:Gray; font-size: 13px;'>시의 주제: {sub}</p>", unsafe_allow_html=True)

if(st.button("시 작성")):
    with st.spinner("시 작성중 ..."):
        res = chatModel.invoke(sub + "에 관한 시를 써줘. 우선 시를 작성해. 작성한 시를 10점 만점으로 평가해. 만약 시가 8점을 넘지 못했다면 다시 생성해. 8점이 넘은 시를 결과로 해. json 형식으로 시도 횟수(attempts), 제목(head), 내용(body), 점수(rating)와 간단한 분석(reason)을 출력해.\시에서 줄바꿈은 <br>로 처리해.")
        response_json = json.loads(res.content)
        
        st.markdown(
            f"""
            <p style='color:Blue; font-size: 30px;'>{response_json['head']}</p>
            <p style='color:Black; font-size: 20px;'>{response_json['body']}</p>
            <p style='color:Violet; font-size: 15px;'>시도 횟수: {response_json['attempts']}</p>
            <p style='color:Red; font-size: 15px;'>점수: {response_json['rating']}</p>
            <p style='color:Green; font-size: 15px;'>분석: {response_json['reason']}</p>
            """,
            unsafe_allow_html=True
        )
