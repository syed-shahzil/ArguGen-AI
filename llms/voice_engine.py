from config import openai_client

def get_aprox_time(text):
    words= len(text.split())
    return words/2.5

def generate_voice(text, voice):
    try:
        response= openai_client.audio.speech.create(
            input=text[:4096], # Safety limit for OpenAI TTS
            model="gpt-4o-mini-tts",
            voice=voice
        )
        return response.read()
    except Exception as e:
        print(f"Voice Error: {e}")
        return None
