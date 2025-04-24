from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import find_user_by_email, find_user_by_nickname, create_user, verify_user
from flask import session
from flask_bcrypt import Bcrypt
import re

auth_bp = Blueprint("auth_bp", __name__)
bcrypt = Bcrypt()

# 이메일 정규식 : _@_._
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
# 비밀번호 정규식: 대문자, 소문자, 숫자, 특수기호 각각 1개 이상
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        nickname = request.form["nickname"]
        password = request.form["password"]

        # 이메일 형식 체크
        if not EMAIL_REGEX.match(email):
            flash("올바른 이메일 형식이 아닙니다.", "danger")
            return redirect(url_for("auth_bp.register"))
        
        # 이메일 중복 체크
        if find_user_by_email(email):
            flash("이미 존재하는 이메일입니다.", "danger")
            return redirect(url_for("auth_bp.register"))
        
        # 닉네임 길이 검사
        if len(nickname) < 2 or len(nickname) > 20:
            flash("닉네임은 2자 이상 20자 이하로 입력해주세요.", "danger")
            return redirect(url_for("auth_bp.register"))
        
        # 닉네임 중복 체크
        if find_user_by_nickname(nickname):
            flash("이미 존재하는 닉네임입니다.", "danger")
            return redirect(url_for("auth_bp.register"))

        # 비밀번호 검증
        if not PASSWORD_REGEX.match(password):
            flash("비밀번호는 영문 대/소문자, 숫자, 특수문자를 포함해야 합니다.", "danger")
            return redirect(url_for("auth_bp.register"))

        # 암호화 및 저장
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        create_user(email, nickname, pw_hash)

        flash("회원가입이 완료되었습니다. 로그인해주세요.", "success")
        return redirect(url_for("auth_bp.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = verify_user(email)
        if not user:
            flash("이메일 또는 비밀번호가 일치하지 않습니다.", "danger")
            return redirect(url_for("auth_bp.login"))

        if not bcrypt.check_password_hash(user["password_hash"], password):
            flash("이메일 또는 비밀번호가 일치하지 않습니다.", "danger")
            return redirect(url_for("auth_bp.login"))

        # 로그인 성공
        session["user_id"] = user["id"]
        session["nickname"] = user["nickname"]
        return redirect(url_for("main_bp.index"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()  # 로그인 정보 전체 삭제
    flash("로그아웃 되었습니다.", "success")
    return redirect(url_for("main_bp.index"))