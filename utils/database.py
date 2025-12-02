from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env


# ---------- CONNECTION ----------
def connect_db():
    """Connect to MongoDB and return database object"""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "book_summarization")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    return db


db = connect_db()  # global DB instance


# ---------- USERS ----------
def create_user(name, email, password_hash, role="user"):
    doc = {
        "name": name,
        "email": email.lower(),
        "password_hash": password_hash,
        "role": role,
        "created_at": datetime.utcnow()
    }

    result = db.users.insert_one(doc)
    return str(result.inserted_id)


def get_user_by_email(email):
    return db.users.find_one({"email": email.lower()})


# ---------- BOOKS ----------
def create_book(user_id, title, author=None, chapter=None, file_path=None, raw_text=None, status="uploaded"):
    doc = {
        "user_id": ObjectId(user_id),
        "title": title,
        "author": author,
        "chapter": chapter,
        "file_path": file_path,
        "raw_text": raw_text,
        "uploaded_at": datetime.utcnow(),
        "status": status
    }

    result = db.books.insert_one(doc)
    return str(result.inserted_id)


def update_book_status(book_id, status):
    db.books.update_one({"_id": ObjectId(book_id)}, {"$set": {"status": status}})


# ---------- SUMMARIES ----------
def create_summary(book_id, user_id, summary_text, summary_length, summary_style, chunk_summaries=None, processing_time=None):
    doc = {
        "book_id": ObjectId(book_id),
        "user_id": ObjectId(user_id),
        "summary_text": summary_text,
        "summary_length": summary_length,
        "summary_style": summary_style,
        "chunk_summaries": chunk_summaries or [],
        "processing_time": processing_time,
        "created_at": datetime.utcnow()
    }

    result = db.summaries.insert_one(doc)
    return str(result.inserted_id)


def get_summaries_by_user(user_id):
    return list(db.summaries.find({"user_id": ObjectId(user_id)}).sort("created_at", -1))

