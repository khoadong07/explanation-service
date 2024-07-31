# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
LOG_PATH = os.getenv('LOG_PATH', './logs/app.log')
FIREWORKS_URL = os.getenv('FIREWORKS_URL', 'https://api.fireworks.ai/inference/v1/chat/completions')
FIREWORKS_TOKEN = os.getenv('FIREWORKS_TOKEN', '')
FIREWORKS_API_MAX_TOKEN = int(os.getenv('FIREWORKS_API_MAX_TOKEN', '2048'))
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.6'))
FIREWORKS_MODEL = os.getenv('FIREWORKS_MODEL', 'accounts/fireworks/models/llama-v3-8b-instruct')
REDIS = os.getenv('REDIS', '')
