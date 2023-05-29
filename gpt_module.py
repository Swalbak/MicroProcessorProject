from config import key_config
import openai

'''
gpt_response(messages)
messages(list): 유저마다 gpt와 진행했던 문답 정보
usage: messages 객체를 전달, 답변 정보를 추가한 messages와 gpt가 답변한 내용 반환

유저가 추가로 질문할 내용을 추가해야함(messages.append({"role": "user", "content": "질문내용"}))
'''

openai.api_key = key_config['gpt_apikey']

def gpt_response(messages):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=messages,
    max_tokens=180
    )

    messages.append(response['choices'][0]['message'])

    return messages, response['choices'][0]['message']['content']
    # print(response['choices'][0]['message']['content'])
