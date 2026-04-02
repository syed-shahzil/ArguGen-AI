import json
import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import time 
from llm_config import openrouter_client, openai_client
from prompts import Oponent_A, Oponent_B, Judge
from llm_config import favour_voice, opposition_voice, judge_voice
debating_statement ="United States is powerful than Iran"

opA_argues = dict()
opB_argues = dict()


def run_round(round, model, system_prompt, my_argues, opo_argues,statement=debating_statement):
    
    response = openai_client.chat.completions.create(
    model=model,  
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": json.dumps({
                "round": round,
                "debate_statement": statement,
                "Your_recent_argues": my_argues,
                "oponant_recent_argues":opo_argues
            })}],
            stream=True
            )
    my_argues[f"argue_{round}"]= " "
    full_response=" "
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response+= chunk.choices[0].delta.content
            my_argues[f"argue_{round}"]= full_response
   
            yield full_response

def judge_debate(total_rounds, model, statement=debating_statement):
    response = openai_client.chat.completions.create(
    model=model,  
    messages=[
        {
            "role": "system",
            "content": Judge
        },
        {
            "role": "user",
            "content": json.dumps({
                "total_rounds": total_rounds,
                "debate_statement": statement,
                "oponant_A_argues": opA_argues,
                "oponant_B_argues":opB_argues
            })}],
            stream=True
            )
    full_response=" "
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response+= chunk.choices[0].delta.content
            yield full_response

def get_aprox_time(text):
    words= len(text.split())
    return words/2.5

def generate_voice(text, voice):
    response= openai_client.audio.speech.create(
        input=text,
        model="gpt-4o-mini-tts",
        voice=voice
    )
    return response.read()

def debate_func_for_gradio(statement):
    opA_argues.clear()
    opB_argues.clear()
    
    for i in range(3):
        for chunk in run_round(round=i+1,statement=statement,system_prompt=Oponent_A,model="gpt-4o" ,my_argues=opA_argues, opo_argues=opB_argues):
            yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), "", None, None, None      
        
        audio_A=generate_voice(text=opA_argues[f'argue_{i+1}'], voice=favour_voice)
        yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), "", audio_A, None, None    
        time.sleep(get_aprox_time(text=opA_argues[f'argue_{i+1}']))
        
        for chunk in run_round(round=i+1,statement=statement, system_prompt=Oponent_B,model="gpt-4o",my_argues=opB_argues, opo_argues=opA_argues):
            yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), "" , None, None, None    

        audio_B=generate_voice(text=opB_argues[f'argue_{i+1}'], voice=opposition_voice)
        yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), "", None, audio_B, None    
        time.sleep(get_aprox_time(text=opB_argues[f'argue_{i+1}']))
    
    j_text = ""
    for chunk in judge_debate(i+1,statement=statement , model="gpt-5.2"):
        j_text = chunk
        yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), f"Judgement: \n {chunk}", None, None, None      
        
    audio_judge = generate_voice(text=j_text, voice=judge_voice)
    yield "\n\n".join(opA_argues.values()), "\n\n".join(opB_argues.values()), f"Judgement: \n {j_text}", None, None, audio_judge
    time.sleep(get_aprox_time(text=j_text))
    

    
if __name__ == "__main__":
    for i in range(3):
        r1_final = ""
        for chunk in run_round(round=i+1,system_prompt=Oponent_A,model="gpt-4o" ,my_argues=opA_argues, opo_argues=opB_argues):
            r1_final = chunk
        print(f"Oponant A: Round {i+1}: {r1_final}")
        
        r2_final = ""
        for chunk in run_round(round=i+1,system_prompt=Oponent_B,model="gpt-4o",my_argues=opB_argues, opo_argues=opA_argues):
            r2_final = chunk
        print(f"Oponant B: Round {i+1}: {r2_final}")
        
    
    j_final = ""
    for chunk in judge_debate(i+1, model="gpt-5.2"):
        j_final = chunk
    print(f"Debate Judgement ={j_final}")
    
    #For Security I only allow 
    __all__=['debate_func_for_gradio']