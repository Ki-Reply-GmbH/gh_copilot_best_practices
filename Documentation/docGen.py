# TODO: Create docstrings for this file (Class, Module, Functions)
import os
import openai
import pandas as pd
import json
import ast
from github import Github, Auth
import prompts
from functions import encode_to_base64, decode_from_base64
from cache import Cache
 
EXPLANATION, ANSWER = 0, 0
CODE, COMMIT_MSG = 1, 1
downstream_path = os.path.join(os.path.dirname(__file__), ".tmp/downstream")
git_access_token = os.environ["GIT_ACCESS_TOKEN"]
openai.api_key = os.environ["OPENAI_API_KEY"]
def get_completion(prompt, model="gpt-3.5-turbo-1106", type="text"):

    messages = [
        {
            "role": "system",
            "content": "You are a system designed to solve GitHub merge conflicts."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = openai.OpenAI().chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output,
        response_format={"type": type}
    )
    return response.choices[0].message.content
 
class Agent():

 
    def __init__(self, downstream, upstream):
    
        self._upstream = upstream
        self._downstream = downstream
        self._file_paths = []
        self._prompt = ""
 
        self.explanations = []
        self.responses = []
        self.commit_msg = ""
 
        self._cache = Cache()
       
    def solve_merge_conflict(self):
       
        base64_prompt = encode_to_base64(self._prompt)
        if self._cache.lookup(base64_prompt):
            print("Cache hit!\n")
            cache_content = self._cache.get_answer(base64_prompt)
            response = decode_from_base64(cache_content)
            response = ast.literal_eval(response) #Prevent json.loads from throwing an error
        else:
            print("Cache miss!")
            response = json.loads(get_completion(self._prompt, type="json_object"))
            self._cache.update(
                base64_prompt,
                encode_to_base64(response)
                )                
        self.explanations += [response["explanation"]]
        self.responses += [response["code"]] # merge conflict resolved file content
        return response
   
    def make_commit_msg(self):
      
        commit_prompt = prompts.commit_prompt
        for i, explanation in enumerate(self.explanations):
            commit_prompt += "Explanation " + str(i) + ":\n"
            commit_prompt += explanation + "\n"
        self.commit_msg = get_completion(commit_prompt)
 
    def make_prompt(self, file_path: str, file_content:str) -> str:
        
        self._file_paths += [file_path]
        self._prompt = prompts.merge_prompt.format(file_content=file_content)
        return self._prompt
   
    def write_responses(self):
       
        for i, file_path in enumerate(self._file_paths):
            with open(os.path.join(downstream_path, file_path), 'w') as file:
                file.write(self.responses[i])
 
    def git_actions(self):
       
        self._downstream.git.add(self._file_paths)
        self._downstream.git.commit("-m", self.commit_msg)
        self._downstream.git.push("--set-upstream", "origin", self._downstream.active_branch.name)
 
    def create_pull_request(self):
      
        auth = Auth.Token(git_access_token)   #TODO Als env-Variable dynamisch lesen
        g = Github(auth=auth)
        g.get_user().login
        downstream_repo = g.get_repo("Ki-Reply-GmbH/test") #TODO dynamisch zuweisen
        body = "**Our AI has resolved the merge conflicts in the following files:**\n\n"
        for i, file_path in enumerate(self._file_paths):
            body += "**" + file_path + "**" + ":\n"
            body += self.explanations[i] + "\n\n"
        downstream_repo.create_pull(
            title="Automated AI merge conflict resolution",
            body=body,
            head=self._downstream.active_branch.name,
            base="main"
        )
        print("Created pull request.")
 
 
    def __str__(self):
       
        out = "Merged File_Paths:\n"
        for file_path in self._file_paths:
            out += file_path + "\n"
        return out
       
