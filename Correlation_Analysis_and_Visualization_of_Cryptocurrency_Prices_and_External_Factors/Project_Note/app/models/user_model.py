# app/models/user_model.py

from app.db import get_db

def find_user_by_email(email):
    #이메일 중복 확인
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()

def find_user_by_nickname(nickname):
    #닉네임 중복 확인
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE nickname = %s", (nickname,))
    return cursor.fetchone()

def create_user(email, nickname, password_hash):
    # db에 회원 추가
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (email, nickname, password_hash) VALUES (%s, %s, %s)",
        (email, nickname, password_hash)
    )
    db.commit()

def verify_user(email):
    #로그인 시 비밀번호 검증을 위한 해시 조회
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()