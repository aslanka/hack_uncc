# database connection
import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from __main__ import app



load_dotenv()

# uri = os.getenv("mongodb+srv://ayushlanka106:wCrF79lzDI6vKWcq@cluster0.7by8a1a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
uri = "mongodb+srv://ayushlanka106:wCrF79lzDI6vKWcq@cluster0.7by8a1a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)


db = client['db']