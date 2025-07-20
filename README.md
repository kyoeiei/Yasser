# Web-based Chatbot

A simple web-based chatbot built with Flask, ready for chutes.ai API integration.

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory (optional, for API keys):
```
CHUTES_API_KEY=your_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

- Modern web interface with real-time chat functionality
- Ready for chutes.ai API integration
- Responsive design
- Support for both click and Enter key message sending

## Adding chutes.ai Integration

To integrate with chutes.ai API:
1. Add your API key to the `.env` file
2. Modify the `/chat` route in `app.py` to make API calls to chutes.ai
3. Update the response handling as needed

## Project Structure

- `app.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file) 