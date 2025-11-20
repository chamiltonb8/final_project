import pandas as pd
import matplotlib as plt
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}'
r = requests.get(url)
data = r.json()

print(data)

