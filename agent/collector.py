import psutil, requests, os
from dotenv import load_dotenv

load_dotenv()

psutil.cpu_percent()

data = {
    "cpu": psutil.cpu_percent(),
    "ram": psutil.virtual_memory().percent,
    "disk": psutil.disk_usage("/").used/1024**3
}

requests.post(os.getenv("API_URL"), json=data)
