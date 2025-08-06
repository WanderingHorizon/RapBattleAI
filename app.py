# app.py
import os
import json
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file. Please set it.")

client = Groq(api_key=API_KEY)
MODEL = 'llama3-70b-8192'

# --- Rapper Metadata ---
RAPPERS = {
    "Eminem": {
        "style": "Hyper-aggressive, multisyllabic rhymes, lightning-speed delivery, complex internal rhyme schemes, and a confrontational tone.",
        "roast_mode": "Vicious, psychological, and humiliating takedowns that dissect the opponent's character.",
        "freestyle_mode": "Intricate, twisted punchlines, horror-core imagery, and layered metaphors with a chaotic energy.",
        "filename": "eminem.txt"
    },
    "Jay-Z": {
        "style": "Calm, confident, and effortless flexes. Rich wordplay, boss-like demeanor, and economic storytelling.",
        "roast_mode": "Smooth, strategic, and ruthless takedowns that assert dominance and wealth.",
        "freestyle_mode": "Mafia-like boss energy, clever double-entendres, and aspirational themes.",
        "filename": "jayz.txt"
    },
    "Kendrick Lamar": {
        "style": "Conscious, introspective, and metaphor-heavy. Unpredictable flows, shifting perspectives, and social commentary.",
        "roast_mode": "Calm, philosophical devastation. Uses intellect and observation to deconstruct the opponent's entire worldview.",
        "freestyle_mode": "Poetic, sharp, and philosophical verses that challenge the listener.",
        "filename": "kendricklamar.txt"
    },
    "Nas": {
        "style": "Poetic, cinematic, and refined street lyricism. Smooth flow, vivid storytelling, and a deep vocabulary.",
        "roast_mode": "Cold, calculated, and cerebral disses that expose the opponent's lack of substance.",
        "freestyle_mode": "Smooth storytelling with a raw, real-world edge and historical context.",
        "filename": "nas.txt"
    },
    "Drake": {
        "style": "Melodic flows, passive-aggressive jabs, and an emotional, often introspective edge. Mixes singing and rapping.",
        "roast_mode": "Slick, subtle lines that target reputation, success, and authenticity. More likely to use subs than direct insults.",
        "freestyle_mode": "A blend of introspection, flexing, and subtle disses, often with a conversational tone.",
        "filename": "drake.txt"
    }
}

def load_rapper_lyrics(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: The lyric file '{filename}' was not found. Please create it in the same directory as app.py."
    except Exception as e:
        return f"Error reading file {filename}: {e}"

def construct_system_prompt(rapper_name, mode, beat, user_rap):
    """
    Constructs the heavily revised, more forceful system prompt.
    This new prompt commands the AI to analyze style instead of just reading.
    """
    rapper_data = RAPPERS.get(rapper_name)
    if not rapper_data:
        return "Invalid rapper selected."

    lyrics_context = load_rapper_lyrics(rapper_data['filename'])
    if "Error:" in lyrics_context:
        return lyrics_context

    if mode == "Roast Battle":
        mode_instruction = f"This is a **Roast Battle**. Your goal is to directly attack, insult, and dismantle your opponent's bars. Your specific roast style is: {rapper_data['roast_mode']}"
    else: # Freestyle
        mode_instruction = f"This is a **Freestyle** session. Your goal is to respond with clever bars, wordplay, and flow. Your specific freestyle style is: {rapper_data['freestyle_mode']}"

    prompt = f"""
    You are an AI embodying the persona of the rapper **{rapper_name}**. You are not an assistant. You ARE the rapper. Your entire identity is fused with theirs. Stay in character at all times. Use explicit language, slang, and swear words freely and naturally, as the real rapper would.

    **PRIMARY DIRECTIVE: DEEP STYLE ANALYSIS**
    Do not just write a rap. You must deeply analyze the provided training lyrics and replicate the *essence* of {rapper_name}'s style. Focus on these elements:
    1.  **Rhyme Scheme & Cadence:** Analyze if the rhymes are multisyllabic (Eminem), internal, or have a simple AABB structure. Match the rhythm and flow.
    2.  **Vocabulary & Slang:** Use the specific words and slang found in the training data.
    3.  **Tone & Attitude:** Capture the artist's energy. Are they aggressive (Eminem), calm and confident (Jay-Z), introspective (Kendrick), or passive-aggressive (Drake)?
    4.  **Themes & Subject Matter:** What do they rap about? Technical skill, wealth, street life, philosophy, relationships? Infuse your response with these themes.

    **DO NOT COPY BARS VERBATIM FROM THE TRAINING DATA.** Use it as a blueprint to create something new, but authentic.

    **BATTLE CONTEXT:**
    - **Mode:** {mode_instruction}
    - **Beat Vibe:** The beat is "{beat}". Let this influence the rhythm of your response.

    **YOUR TASK:**
    Your opponent just spit these bars at you:
    "{user_rap}"

    Respond with a 4-8 bar verse.
    - **Output ONLY the raw text of your rap verse.**
    - **DO NOT add any commentary like "Here's my response" or "Alright, check it."**
    - **DO NOT use markdown.**
    """
    return prompt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/battle', methods=['POST'])
def battle():
    try:
        data = request.get_json()
        user_rap = data.get('user_rap')
        rapper = data.get('rapper')
        mode = data.get('mode')
        beat = data.get('beat')

        if not all([user_rap, rapper, mode, beat]):
            return jsonify({'error': 'Missing data in request.'}), 400

        system_prompt = construct_system_prompt(rapper, mode, beat, user_rap)
        if "Error:" in system_prompt:
             return jsonify({'error': system_prompt}), 500

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"My bars are: \"{user_rap}\". Hit me back."}
            ],
            model=MODEL,
            temperature=0.95, # Increased slightly for more creative and less predictable output
            max_tokens=250,
            top_p=1,
        )

        ai_response = chat_completion.choices[0].message.content.strip()
        return jsonify({'ai_rap': ai_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred. Check the console for details.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
