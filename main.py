#pip install python-dotenv, openai, langchain, langchain-openai

#from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st


#Settings
st.title('AI Poem Writer')
#load_dotenv()
chatModel = ChatOpenAI()


#Main
sub = st.text_input('시의 주제를 입력하세요: ')
st.markdown("<p style='color:Gray; font-size: 13px;>시의 주제: ", sub, "</p>")

if(st.button("시 작성")):
    with st.spinner("시 작성중 ..."):
        res = chatModel.invoke(sub + "밤에 관한 시를 써줘.\우선 시를 작성해.\작성한 시를 10점 만점으로 평가해.\만약 시가 8점을 넘지 못했다면 다시 생성해.\8점이 넘은 시를 결과로 해.\json 형식으로 시도 횟수(attempts), 제목(head), 내용(body), 점수(rating)와 간단한 분석(reason)을 출력해.")
        st.markdown("<p style='color:Blue; font-size: 20px;'>", res.content[head], "\n</p>",
                    "<p style='color:Black; font-size: 15px;'>", res.content[body], "\n</p>",
                    "<p style='color:Violet; font-size: 15px;'>", res.content[attempts], "\n</p>",
                    "<p style='color:Red; font-size: 15px;'>", res.content[rating], "\n</p>",
                    "<p style='color:Green; font-size: 15px;'>", res.content[reason], "\n</p>"
                    )
