import argparse
# Fixed import - use langchain_community instead of langchain.vectorstores
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# Voice integration imports
from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import platform

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def get_tts_engine():
    """Get configured TTS engine with English voice support"""
    engine = pyttsx3.init()
    
    # Voice selection - prioritize English voices
    voices = engine.getProperty('voices')
    if voices:
        for voice in voices:
            voice_name = voice.name.lower()
            voice_id = voice.id.lower()
            
            # Prioritize English voices first
            if ('english' in voice_name or 'zira' in voice_name or 'david' in voice_name or 
                'mark' in voice_name or 'hazel' in voice_name or 'en-us' in voice_id or 
                'en_us' in voice_id):
                engine.setProperty('voice', voice.id)
                print(f"Using English voice: {voice.name}")
                break
        else:
            # If no specific English voice found, use the first available
            if voices:
                engine.setProperty('voice', voices[0].id)
                print(f"Using default voice: {voices[0].name}")
    
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine



def speak_response(text):
    """Speak the LLM response"""
    try:
        print(f"🔊 Speaking response...")
        engine = get_tts_engine()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        print("✅ Finished speaking")
    except Exception as e:
        print(f"TTS Error: {e}")

def get_voice_input():
    """Get single voice input"""
    print("🎤 Please speak your question...")
    
    recorder = AudioToTextRecorder(
        model="medium",
        language="en",  # Change to "en" for English
        enable_realtime_transcription=False,
        post_speech_silence_duration=1.2,
        min_length_of_recording=0.5,
        sample_rate=16000,
        use_microphone=True,
        spinner=False,
    )
    
    # Get the speech input
    text = recorder.text()
    
    # Cleanup
    try:
        recorder.shutdown()
    except:
        pass
    
    return text.strip() if text else ""

def query_rag(query_text: str):
    """Query the RAG system"""
    print(f"🤖 Processing: {query_text}")
    
    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Search the DB
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Query Ollama
    print("🧠 Thinking...")
    model = Ollama(model="llama3.2")
    response_text = model.invoke(prompt)
    
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    
    # Print response
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    
    return response_text

def main():
    """Main function with voice input option"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", action="store_true", help="Use voice input")
    parser.add_argument("query_text", nargs="?", type=str, help="The query text")
    
    args = parser.parse_args()
    
    if args.voice:
        # Voice input mode
        print("🎤 Voice RAG System - Single Query Mode")
        voice_query = get_voice_input()
        
        if voice_query:
            print(f"👂 You asked: {voice_query}")
            response = query_rag(voice_query)
            speak_response(response)
        else:
            print("❌ No speech detected")
            
    elif args.query_text:
        # Text input mode with spoken output
        response = query_rag(args.query_text)
        speak_response(response)
    else:
        print("Usage:")
        print("  python query_data.py --voice              # Voice input mode")
        print("  python query_data.py 'your question'      # Text input with spoken output")

if __name__ == "__main__":
    main()
