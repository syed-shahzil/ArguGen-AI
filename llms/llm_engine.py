import json, os, sys, time

sys.path.append(os.path.join(os.path.dirname(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import  openai_client
from prompts import Oponent_A, Oponent_B, Judge
from config import favour_voice, opposition_voice, judge_voice
from voice_engine import get_aprox_time, generate_voice


debating_statement ="United States is powerful than Iran"


def run_round(round, model, system_prompt, my_argues, opo_argues,statement=debating_statement):
    try:
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
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"Error in run_round: {e}")
        yield f"\n[LLM Generation Error: The debate was interrupted. Exception: {str(e)}]"

def judge_debate(total_rounds, model, opA_argues, opB_argues, statement=debating_statement):
    try:
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
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"Error in judge_debate: {e}")
        yield f"\n[Judgement Error: {str(e)}]"


def debate_func_for_gradio(statement):
    a_accumulated = []
    b_accumulated = []
    
    for i in range(3):
        a_accumulated.append("")
        for chunk in run_round(round=i+1,statement=statement,system_prompt=Oponent_A,model="gpt-4o" ,my_argues=a_accumulated[:-1], opo_argues=b_accumulated):
            a_accumulated[-1] += chunk
            yield list(a_accumulated), list(b_accumulated), "", None, None, None      
        
        audio_A=generate_voice(text=a_accumulated[-1], voice=favour_voice)
        yield list(a_accumulated), list(b_accumulated), "", audio_A, None, None    
        time.sleep(get_aprox_time(text=a_accumulated[-1]))
        
        b_accumulated.append("")
        for chunk in run_round(round=i+1,statement=statement, system_prompt=Oponent_B,model="gpt-4o",my_argues=b_accumulated[:-1], opo_argues=a_accumulated):
            b_accumulated[-1] += chunk
            yield list(a_accumulated), list(b_accumulated), "" , None, None, None    

        audio_B=generate_voice(text=b_accumulated[-1], voice=opposition_voice)
        yield list(a_accumulated), list(b_accumulated), "", None, audio_B, None    
        time.sleep(get_aprox_time(text=b_accumulated[-1]))
    
    j_text = ""
    for chunk in judge_debate(total_rounds=i+1, statement=statement, model="gpt-5.2", opA_argues=a_accumulated, opB_argues=b_accumulated):
        j_text += chunk
        yield list(a_accumulated), list(b_accumulated), f"Judgement: \n {j_text}", None, None, None      
        
    audio_judge = generate_voice(text=j_text, voice=judge_voice)
    yield list(a_accumulated), list(b_accumulated), f"Judgement: \n {j_text}", None, None, audio_judge
    time.sleep(get_aprox_time(text=j_text))
    

if __name__ == "__main__":
    a_accum = []
    b_accum = []
    for i in range(3):
        a_accum.append("")
        for chunk in run_round(round=i+1,system_prompt=Oponent_A,model="gpt-4o" ,my_argues=a_accum[:-1], opo_argues=b_accum):
            a_accum[-1] += chunk
        print(f"Oponant A: Round {i+1}: {a_accum[-1]}")
        
        b_accum.append("")
        for chunk in run_round(round=i+1,system_prompt=Oponent_B,model="gpt-4o",my_argues=b_accum[:-1], opo_argues=a_accum):
            b_accum[-1] += chunk
        print(f"Oponant B: Round {i+1}: {b_accum[-1]}")
        
    j_final = ""
    for chunk in judge_debate(total_rounds=i+1, model="gpt-5.2", opA_argues=a_accum, opB_argues=b_accum):
        j_final += chunk
    print(f"Debate Judgement ={j_final}")
    
    #For Security I only allow 
    __all__=['debate_func_for_gradio']