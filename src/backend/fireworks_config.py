import os
from fireworks.client import Fireworks

# Fetch the Firework API key from environment variables
FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')

# Initialize the Fireworks client
fireworks_client = Fireworks(api_key=FIREWORKS_API_KEY)