import json
import redis
from llama_cpp import Llama

redis_clienet = redis.from_url("redis://redis:6379", decode_responses=True)


llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=2,
    verbose=False,
    chat_format="llama-3",
)

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

def run():
    while True: # 무한루프로 하지 않으면 작업 하나 끝나면 종료되어버림

        # 1) 큐에서 task를 dequeue
        _, task = redis_clienet.brpop("queue") # rpop:아무것도 없으면 nil 반환, block rpop: 아무것도 없으면 들어올때까지 대기
        
        task_data : dict = json.loads(task)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(task_data["messages"])


        # 2) 추론 -> 토큰 -> publish (반복)
        response_generator = llm.create_chat_completion(
            messages=messages,
            max_tokens=256,
            temperature=0.7,
            stream=True, # 이게 없으면 한번에 오는건데, stream=True이면 제너레이터를 먼저 만든다. 
        )
        # 즉, 여기까지는 아직 추론을 하지 않은 상태임

        channel = task_data["channel"]
        for chunk in response_generator:
            token = chunk["choices"][0]["delta"].get("content")
             
            if token:
                redis_clienet.publish(channel, token)

        # 3) 추론이 종료되었음을 알림: [Done] 메시지 전송
        redis_clienet.publish(channel, "[DONE]")

# 이 파일이 직접 실행한 경우에만, run() 호출
if __name__ == "__main__":
    run()