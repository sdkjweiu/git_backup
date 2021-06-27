from flask import Flask, render_template, abort, url_for, session, flash, session
from flask.signals import Namespace
from werkzeug.utils import redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import Required

home = Flask(__name__)
Bootstrap = Bootstrap(home)

class HOMEForm(FlaskForm):      #FlaskForm 상속
    ID_Text = StringField('아이디', validators=[Required()]) #validators=[Required()] -> 필드에 데이터가 있는지 검증
    PW_Text = PasswordField('비밀번호', validators=[Required()])
    man_woman = RadioField('성별', choices=[('남'), ('여')])
    submit = SubmitField('확인')

home.config['SECRET_KEY'] = 'Test SECRET KEY'

@home.route('/', methods = ['GET', 'POST'])
def index():
    form=HOMEForm()
    if form.validate_on_submit():
        
        session['name'] = form.ID_Text.data
        form.ID_Text.data=''
        return redirect(url_for('user'))
    return render_template ('index.html', form=form)

@home.route('/user/<name>')
def user(name):
    return render_template ('user.html', name=session.get('name'))

@home.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    home.run(debug=True)