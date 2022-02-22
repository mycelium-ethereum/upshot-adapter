from dotenv import load_dotenv
load_dotenv();

import os
from client.Webhook import webhook
from client.Upshot import Upshot

upshot = Upshot(os.getenv("UPSHOT_API_KEY"))
