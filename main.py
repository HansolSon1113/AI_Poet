#pip install python-dotenv, openai, langchain, langchain-openai

#from dotenv import load_dotenv
import streamlit as st
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

# Settings
st.title('AI Poem Writer')
chatModel = ChatOpenAI()
word_temp = "{input}에 관한 시를 써줘.\작성한 시를 10점 만점으로 평가해.\만약 시가 8점을 넘지 못했다면 다시 생성해.\8점이 넘었다면 시 생성은 멈추고 8점이 넘은 시를 결과로 해.\json 형식으로 시도 횟수(attempts), 제목(head), 내용(body), 점수(rating)와 간단한 분석(reason)을 출력해.\\head의 크기와 색상은 markdown을 활용해 시에 알맞게 조절해.\body도 크기와 색상을 markdown을 활용해 조정하는데 각 단어별로 다르게 해도 돼.\시에서 줄바꿈은 <br>로 처리해.\프롬프트에 적힌 내용을 echo하지 말것.\제목과 내용의 키는 각각 head, body여야만 해.\시는 다른 언어일 수 있지만 평가는 항상 한국어여야만 해."
sentence_temp = "{input}에서 시의 주제를 추출해.\추출한 주제에 관한 시를 하나 써줘.\작성한 시를 10점 만점으로 평가해.\만약 시가 8점을 넘지 못했다면 다시 생성해.\8점이 넘었다면 시 생성은 멈추고 8점이 넘은 시를 결과로 해.\json 형식으로 시도 횟수(attempts), 제목(head), 내용(body), 점수(rating)와 간단한 분석(reason)을 출력해.\\head의 크기와 색상은 markdown을 활용해 시에 알맞게 조절해.\body도 크기와 색상을 markdown을 활용해 조정하는데 각 단어별로 다르게 해도 돼.\시에서 줄바꿈은 <br>로 처리해.\프롬프트에 적힌 내용을 echo하지 말것.\제목과 내용의 키는 각각 head, body여야만 해.\시는 다른 언어일 수 있지만 평가는 항상 한국어여야만 해."
subRoute = [
        {
            "name": "word",
            "description": "단어가 입력되었을때",
            "prompt_template": word_temp
            },
        {
            "name": "sentence",
            "description": "문장이 입력되었을때",
            "prompt_template": sentence_temp
        }
        ]

destination_chains = {}
for p_info in subRoute:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = LLMChain(llm=chatModel, prompt=prompt)
    destination_chains[name] = chain  
    
destinations = [f"{p['name']}: {p['description']}" for p in subRoute]
destinations_str = "\n".join(destinations)
default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=chatModel, prompt=default_prompt)
MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt \
names specified below OR it can be "DEFAULT" if the input is not\
well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

router_chain = LLMRouterChain.from_llm(chatModel, router_prompt)
chain = MultiPromptChain(router_chain=router_chain, 
                         destination_chains=destination_chains, 
                         default_chain=default_chain, verbose=True)


# Main
sub = st.text_input('시의 주제 혹은 글을 입력하세요(글은 주제를 추출하는 것으로 연관성이 떨어질 수 있습니다.): ')
st.markdown(f"<p style='color:Gray; font-size: 13px;'>시의 주제: {sub}</p>", unsafe_allow_html=True)

if(st.button("시 작성")):
    with st.spinner("시 작성중 ..."):
        res = chain.run(sub)
        try:
            response_json = json.loads(res)

            st.markdown(
                f"""
                {response_json['head']}<br>
                {response_json['body']}<br><br>
                <p style='color:Violet; font-size: 15px;'>시도 횟수: {response_json['attempts']}</p>
                <p style='color:Orange; font-size: 15px;'>점수: {response_json['rating']}</p>
                <p style='color:Green; font-size: 15px;'>분석: {response_json['reason']}</p>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.markdown(
                f"""
                <p style='color:Red; font-size: 20px;'>시 생성에 실패했습니다. 다시 시도해주세요.<br>
                오류 내용: {e}</p>
                """,
                unsafe_allow_html=True
            )
            if(st.button("응답 보기")):
                st.write(res.content)
