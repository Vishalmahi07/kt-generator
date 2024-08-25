# %%
import js2py
from CarbonSnippets import *
from CodeParser import *
from CreateVideo1 import *
#from DIDVideoGenerator import *
from ResponseGenerator import *
from config import *
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP
import code2flow
#import openai
# Import the required module for text 
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
import os

# Language in which you want to convert
language = 'en'
r'''
#code to flowchart
flowchart_path=os.path.join(save_path,f"soha.png")
code2flow.code2flow(test_code,flowchart_path)
'''
# Split the code using parser
sourcelist=[]

for root, dirs, files in os.walk(test_code):
    for file in files:
        if not file.endswith('.py'):
            # Check if the file is not already a .py file
            old_file_path = os.path.join(root, file)
            new_file_path = old_file_path + '.py'
            os.rename(old_file_path, new_file_path)

for root, dirs, files in os.walk(test_code):
    for file in files:
        try:
            file_path = os.path.join(root, file)
                #print(f" Reading {file}...")
            with open(file_path, "r") as f:
                sourcelist.append(f.read())
        except Exception as e:
            #print(f"Error reading {file}: {e}. Moving to next file")
            continue

extracted_elements_list=[]
for source in sourcelist:
     print(source)
     codeparser = code_parser()
     extracted_elements=codeparser.extract_elements(source)
     extracted_elements_list.append(extracted_elements)
     #print(extracted_elements)

# %%
#model init
model_path=r'C:\Users\SESA754073\OneDrive - Schneider Electric\mistral-7b-instruct-v0.1.Q2_K.gguf'
llm = LlamaCPP(model_path=model_path, temperature=0.1, max_new_tokens=512)
service_context_manager = ServiceConfiguration(model_path)
service_context = service_context_manager.get_service_context()
text_node_manager = TextNodeManager()
response_parse_manager = ResponseParser()

video_paths=[]
# Generate explanation and summaries
for extracted_elements in extracted_elements_list:
     n=0
     try:
         generate_carbon_snippets(extracted_elements, save_path)
     except:
         continue
     nodes = text_node_manager.get_nodes(extracted_elements)
     query_handler = QueryHandler(llm,nodes, service_context)
     explaination_response = query_handler.get_response("explaination")
     explaination_summaries = response_parse_manager.parse(explaination_response.response)
     print(explaination_summaries)
     for index, chunk in enumerate(explaination_summaries):
          path=os.path.join(save_path, f"chunk_{index}.mp4")
          myobj = gTTS(text=chunk, lang=language, slow=False)
          myobj.save(path)
          new_path=os.path.join(save_path,f"elements_{n}")
          video_paths.append(new_path)
          # Stitch videos and images together
          audio_paths = [os.path.join(new_path, f"chunk_{i}.mp4") for i in range(len(extracted_elements))]
          image_paths = [os.path.join(new_path, f"image_{i}.png") for i in range(len(extracted_elements))]
          stitch_video(new_path, audio_paths, image_paths)
          n=n+1

final_path=os.path.join(save_path,f"chunk_summaries_full.mp4")
method="compose"
concatenate(video_paths,final_path,method)
