from config import key_config
import openai

openai.api_key = key_config['gpt_apikey']

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-0301",
  messages=[
      {"role": "system", "content": "안녕하세요, 육정훈님! 무엇을 도와드릴까요?"},
      {"role": "user", "content": "내 이름으로 삼행시 지어줘"}
  ],
  max_tokens=100
)

print(response['choices'][0]['message']['content'])