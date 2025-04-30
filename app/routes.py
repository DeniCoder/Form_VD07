from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from .models import User, db
from .forms import RegisterForm, LoginForm, ProfileForm

def register_routes(app):
    bp = Blueprint('main', __name__)

    @bp.route('/')
    def index():
        return redirect(url_for('main.login'))

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Пользователь с таким email уже существует.', 'danger')
                return render_template('register.html', form=form)

            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('main.login'))
        return render_template('register.html', form=form)

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                session['user_id'] = user.id
                flash('Вы вошли в систему', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Неверный email или пароль', 'danger')
        return render_template('login.html', form=form)

    @bp.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('main.login'))

        user = User.query.get(session['user_id'])
        form = ProfileForm(obj=user)

        if form.validate_on_submit():
            user.name = form.name.data
            user.email = form.email.data
            if form.password.data:
                user.set_password(form.password.data)
            db.session.commit()
            flash('Профиль обновлён', 'success')
            return redirect(url_for('main.profile'))

        return render_template('profile.html', form=form)

    @bp.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('Вы вышли из системы', 'info')
        return redirect(url_for('main.login'))

    app.register_blueprint(bp)