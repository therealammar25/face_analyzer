from mangum import Mangum
from main import app  # Yeh aapka main.py se import karo (same folder level se)

handler = Mangum(app, lifespan="off")  # Serverless handler for Vercel/AWS Lambda