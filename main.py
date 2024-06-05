#pip install python-dotenv, openai, langchain, langchain-openai

#from dotenv import load_dotenv
import streamlit as st
import json
from langchain_openai import ChatOpenAI

# Settings
st.title('AI Poem Writer')
chatModel = ChatOpenAI()

# Main
sub = st.text_input('시의 주제 혹은 글을 입력하세요: ')
st.markdown(f"<p style='color:Gray; font-size: 13px;'>시의 주제: {sub}</p>", unsafe_allow_html=True)

if(st.button("시 작성")):
    with st.spinner("시 작성중 ..."):
        res = chatModel.invoke(sub + "에서 시의 주제를 추출해. 추출한 주제에 관한 시를 하나 써줘.\우선 시를 작성해.\작성한 시를 10점 만점으로 평가해.\만약 시가 8점을 넘지 못했다면 다시 생성해.\8점이 넘은 시를 결과로 해.\json 형식으로 시도 횟수(attempts), 제목(head), 내용(body), 점수(rating)와 간단한 분석(reason)을 출력해.\시에서 줄바꿈은 <br>로 처리해.\프롬프트에 적힌 내용을 echo하지 말것.")
        print(res.content)
        #try:
        response_json = res.content.json()

        st.markdown(
            f"""
            <p style='color:Blue; font-size: 30px;'>{response_json['head']}</p>
            <p style='color:Black; font-size: 20px;'>{response_json['body']}</p>
            <p style='color:Violet; font-size: 15px;'>시도 횟수: {response_json['attempts']}</p>
            <p style='color:Orange; font-size: 15px;'>점수: {response_json['rating']}</p>
            <p style='color:Green; font-size: 15px;'>분석: {response_json['reason']}</p>
            """,
            unsafe_allow_html=True
        )
        # except Exception as e:
        #     st.markdown(
        #         f"""
        #         <p style='color:Red; font-size: 20px;'>시 생성에 실패했습니다. 다시 시도해주세요.</p>
        #         """,
        #         unsafe_allow_html=True
        #     )
