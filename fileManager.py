import json
import prompt
from datetime import datetime

class FileManager:
# Parse a JSONL file and process each line
# The function reads the file line by line, ignoring commented lines, and extracts the 'content' field from each message.
    def parseFile(file = 'input.jsonl'):
        i = 0
        with open(file, 'r') as f:
            for line in f:
                if line.strip().startswith("//"): # ignore commented lines
                    continue
                data = json.loads(line)
                messages = data.get('body', {}).get('messages', [])
                for msg in messages:
                    i = i + 1
                    content = msg.get('content')
                    if content:
                        prompt.Prompt.promptApi(content,True) # call the promptApi function with the content
            return ": number of prompts: " + str(i)

    #save to json file
    def saveResponse(content, prompt1, model, batch, file='output.jsonl'):
        now = datetime.now()
        formatted_time = now.strftime("%d%m%Y:%H:%M:%S")
        if batch:
            custom_id = "file" + "-" + formatted_time
        else:
            custom_id = "request" + "-" + formatted_time
        # Construct the JSON object
        json_line = {
            "content": content,
            "prompt": prompt1,
            "model": model,
            "t_id": custom_id
        }

        # Write the JSON object as a line to the file
        with open(file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_line) + '\n')


if __name__ == "__main__":
    saveResponse(
        content="content",
        prompt1="prompt",
        model="model",
        batch=True
)
