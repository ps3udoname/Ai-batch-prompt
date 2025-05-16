import datasets
from ApiCaller import ApiCaler
import fileManager
import json
import re

save = False
model = "deepseek/deepseek-r1:free"
class Prompt:
    def __init__(self):
        # self.save = "a"
        # self.model = "deepseek/deepseek-r1:free"
        self.api_caller = ApiCaler()
        self.file_manager = fileManager.FileManager()
    def promptApi(prmt, batch = False):
        # global model
        response = ApiCaler.requestResponse(prmt,model)
        if isinstance(response, tuple):
            text,model1 = response
            if save or batch:
                fileManager.FileManager.saveResponse(content=text,prompt1=prmt,model=model1,batch=batch)
            return "\n**********************************\n" + model1 + ": " + text + "\n"
        else:
            return "Error"    

    def dataset2(name,column,split,sampleSize,config):
        i = 0    
        # if sampleSize == 'max' or '-1':
        #     sampleSize = 
        print("name: " + name + " column: " + column + " split: " + split + " config: " + config)
        dataset = datasets.load_dataset(name, config, split=split)
        
        for prompt in dataset:
            print(prompt[column])
            i = i + 1
            a = Prompt.promptApi(str(prompt[column]), True)
            if i >= sampleSize:
                break
        return "\n number of prompts: " + str(i)
    # "AlignmentResearch/JailbreakCompletions"
    def dataset(s):
        """
        Parse a string to extract 'name', 'config', and 'column' values into separate string variables.
        """
        print("dataset: " + s)
        pattern = r'name=(\S+)\s+column=(\S+)\s+split=(\S+)\s+limit=(\S+)(?:\s+config=(\S*))?'
        match = re.fullmatch(pattern, s.strip())
        if match:
            name, column, split, sampleSize, config = match.groups()
            
            response = Prompt.dataset2(name, column, split, int(sampleSize), config)
            return response
        else:
            return "\n format error: \n example usage: name=AlignmentResearch/JailbreakCompletions column=content split=train limit=1 config="
    """def get_main_content(dataset_name, split="train", sample_size=5):

        # Load a Hugging Face dataset and try to extract its main text content.
        
        # Parameters:
        #     dataset_name (str): The name of the dataset on Hugging Face.
        #     split (str): Which split to use (default is "train").
        #     sample_size (int): Number of samples to print (for demonstration).
        
        # Returns:
        #     List[str]: Main text content extracted from the dataset.
        
        # Load the dataset
        ds = datasets.load_dataset(dataset_name, split=split)
        
        # Inspect column names
        column_names = ds.column_names
        print(f"Available columns: {column_names}")
        
        # Guess which column(s) contain text data
        preferred_keys = ["text", "content", "sentence", "article", "review"]
        text_fields = [key for key in preferred_keys if key in column_names]

        # If no preferred key found, fall back to first string column
        if not text_fields:
            for key in column_names:
                if isinstance(ds[0][key], str):
                    text_fields = [key]
                    break

        if not text_fields:
            raise ValueError("No text-like field found in the dataset.")
        
        # Extract content
        content = [example[text_fields[0]] for example in ds]

        # Print a few samples
        for i in range(min(sample_size, len(content))):
            print(f"[Sample {i+1}]: {content[i][:100]}...")  # Preview first 100 chars

        print(content)"""


    def reviewResponse(file_path, input_prefix):
        matches = []
        valid_prefixes = ["request-", "file-"]
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    t_id = data.get("t_id", "")
                    if any(t_id.startswith(prefix + input_prefix) for prefix in valid_prefixes):
                        matches.append(data)
                except json.JSONDecodeError:
                    continue  # Skip lines with bad JSON
        return matches
        
if __name__ == "__main__":
    Prompt.dataset("name=AlignmentResearch/JailbreakCompletions column=content split=train config=")
#     Prompt.promptApi("what is your name?","a")
    