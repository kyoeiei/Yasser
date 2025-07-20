from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Get the Chutes.ai API key from environment variables
CHUTES_API_KEY = os.getenv('CHUTES_API_KEY')
CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"

# Default system prompt for the chatbot
DEFAULT_SYSTEM_PROMPT = """[system note: You are a helpful assistant name "Yasser" with purpose of to check the grammar of the text provided by the user and YOU WILL NOT GIVE THEM DIRECT ANSWER unless being asked by the user. you can communicate with the user. You will be given a text and you will need to check the grammar of the text and return the text with the grammar errors SUGGESTIONS. You will give the user of what they could maybe change into but do not give them the word/sentence that can change (example:  "Consider using a more precise phrase. Hint:") . YOU WILL NOT GIVE DIRECT CORRECT ANSWER BUT GIVE THE USER A HINT INSTEAD AND YOUR PURPOSE IS TO HELP USER THINK BUT YOU CAN ALSO GIVE THE USER HINTS WHEN THEY ASK FOR SPECIFIC WORDS IN THE ESSAY AND ONLY GIVE THE USER HINTS ONLY HINTS IF YOU ARE GIVING THE USER HINTS DO NOT GIVE THE REAL ANSWERS BUT GIVE THE USER HINTS TO THE REAL ANSWER INSTEAD.When highlighting incorrect words, you should put them in bold using double asterisks (e.g., incorrect_word). You will give out words in the text that are not correct and not giving direct answer and give hint instead, with the hint sentence are being bold text. The system will have the knowledge of writing and will able to help the user with the vocabulary and grammar. You will rate user responses with the standard of CEFR exam and will tell the user what level of english they are at in the term of CEFR exam. You will give the user the rating and explain the rating and how you arrived at it.You will be honest with the rating with the user responds and tell them how they actually are at the term of CEFR exam. You will give the user how close they were to the correct answer. You will give the user what level of english they are at.]."""
app = Flask(__name__)

def call_chutes_api(message, system_prompt=None):
    """
    Make a call to the Chutes.ai chat completions API using DeepSeek-V3-0324
    """
    if not CHUTES_API_KEY:
        return "Error: Chutes.ai API key not found. Please set it in your .env file."

    headers = {
        "Authorization": f"Bearer {CHUTES_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        messages = []
        # Add system prompt if provided, otherwise use default
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        elif DEFAULT_SYSTEM_PROMPT:
            messages.append({"role": "system", "content": DEFAULT_SYSTEM_PROMPT})
        # Add user message
        messages.append({"role": "user", "content": message})

        payload = {
            "model": "deepseek-ai/DeepSeek-V3-0324",
            "messages": messages,
            "stream": False,
            "max_tokens": 0,
            "temperature": 0.7
        }

        print("Sending request with payload:", payload)  # Debug print
        response = requests.post(
            CHUTES_API_URL,
            headers=headers,
            json=payload
        )
        print("Response status:", response.status_code)  # Debug print
        print("Response content:", response.text)  # Debug print

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('choices') and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            return "No response content from API"
        else:
            error_message = f"Error: API returned status code {response.status_code}"
            try:
                error_detail = response.json()
                error_message += f"\nDetails: {error_detail}"
            except:
                pass
            print("Error response:", error_message)  # Debug print
            return error_message

    except requests.exceptions.RequestException as e:
        return f"Error connecting to Chutes.ai API: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    system_prompt = data.get('systemPrompt', '')  # Get system prompt if provided

    # Call the Chutes.ai API with both message and system prompt
    response = call_chutes_api(user_message, system_prompt if system_prompt else None)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)




