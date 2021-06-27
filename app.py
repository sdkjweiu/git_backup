from flask import Flask, render_template, abort, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import pymysql


app = Flask(__name__)
Bootstrap = Bootstrap(app)


class NameForm(FlaskForm):      #FlaskForm 상속
    name = StringField('What is your name?', validators=[Required()]) #validators=[Required()] -> 필드에 데이터가 있는지 검증
    submit = SubmitField('Submit')

app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST']) #wtf.quick_form 메소드가 post 방식 / 화면출력은 Get, submit 버튼은 post
def main():
    form=NameForm()
    if form.validate_on_submit():
        conn = pymysql.connect(host='192.168.182.128', port=3306, user='mysqlID', passwd='mysqlPW', database='flasky')
        cur = conn.cursor()
        cur.execute('select username from user where username="%s"' %(form.name.data))
        user = cur.fetchone()  #fetchone() 결과값 보여줌=리턴
        if user is None:
            cur.execute('insert into user (username) value ("%s")' %(form.name.data))
            conn.commit()       #DML에서는 커밋을 해야함, 저장
            session['known'] = False
            
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known', False))

@app.route('/name/<test>')
def name(test):
    return '<h1>NAME!</h1> : ' + test

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', test=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

