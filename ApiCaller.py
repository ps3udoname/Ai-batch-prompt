from openai import OpenAI
import time
import config
import logging
logging.basicConfig(level=logging.INFO)
class ApiCaler:
    """
    A class to handle API calls to OpenRouter.
    """
    # def __init__(self):
    #     self.RETRIES = 3
    #     self.delay = 2  # seconds
    def requestResponse (prompt,model):
        # lo
        print("ApiCaler: " + prompt)
        RETRIES = 3
        delay = 2 #seconds
        # model = "deepseek/deepseek-r1:free"
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.API_KEY,
        )
        for attempt in range(RETRIES):
            time.sleep(1)
            if prompt:
                try:
                    completion = client.chat.completions.create(
                    extra_body={
                        "provider": {
                        "sort": "throughput"
                        }
                    },
                    model=model,
                    messages=[
                        {
                        "role": "user",
                        "content": prompt
                        }
                    ]
                    )
                except Exception as e:
                    return (str(e),model)
                try:
                    if completion:
                        return completion.choices[0].message.content,model
                    elif completion.choices[0].message.content == None:
                        return "Error: No completion returned",model
                except TypeError as e:
                    # Handle 'NoneType' error and retry
                    print(f"Attempt {attempt + 1} failed with error: {e}. Retrying...")
                    time.sleep(delay)
            else:
                return "Error: No prompt provided",model

# if __name__ == "__main__":
#     a = requestResponse("what is your name?")
#     print(a)

