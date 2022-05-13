from flask import render_template, request, flash, redirect, url_for
from ...forms import LoginForm, RegisterForm
from .import bp as auth
from ...models import User
from flask_login import current_user, logout_user, login_user, login_required



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        # look up email address that is trying to log in
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash(f'Welcome to MovieWorld!', 'success')
            return redirect(url_for('main.index'))
        flash(f'Incorrect Email and Password', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template('login.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash(f'You have logged out','warning')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            # Create an empty User
            new_user_object = User()
            # build user with the form data
            new_user_object.from_dict(new_user_data)
            # save user to the database
            new_user_object.save()
        except:
            flash("There was an an unexpected error creating your account. Please try again later.", "danger")
            return render_template('register.html.j2', form=form)

        flash('You have successfully registered!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html.j2', form=form)    
