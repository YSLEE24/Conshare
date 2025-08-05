# auth_view.py

from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)

# 로그인 폼(GET)
@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template("login-register.html")

# 로그인 처리(POST)
@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('이메일 또는 비밀번호가 올바르지 않습니다.')
        return redirect(url_for('auth.login'))

    login_user(user)  # Flask-Login 사용
    return redirect(url_for('main.index'))  # 여기서 메인으로 리디렉션!

@auth_bp.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    address = request.form.get('address')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash('이미 존재하는 아이디 또는 이메일입니다.')
        return redirect(url_for('auth.login'))

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        name=name,
        address=address,
        role='both'
    )
    db.session.add(new_user)
    db.session.commit()

    flash('회원가입이 완료되었습니다. 로그인해주세요.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))