from flask import Flask
from flask import render_template
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask import abort
from pprint import pprint
from flask_sqlalchemy import *  

app = Flask(__name__)
app.secret_key = "Flash"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/wbs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
    

class Groups(db.Model):
    group_name = db.Column(db.String(100))
    link = db.Column(db.Text())

    def __repr__(self):
        return "<Title: {}>".format(self.group_name)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/',  methods=['POST'])
def chat():
    target = request.form['no']
    msg = request.form['msg']
    browser = webdriver.Firefox()
    browser.get('https://web.whatsapp.com/send?phone=' + target + '&text=' + msg)

    time.sleep(10)
    # wait = browser.WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'_35EW6'))

    text = browser.find_element_by_class_name('_2S1VP')
    text.send_keys(msg)

    time.sleep(1)
    element = browser.find_element_by_class_name('_35EW6')
    element.click()

    flash('Sukses kirim pesan!', "success")
    return render_template("index.html")


@app.route('/messages')
def messages():
    return render_template('pages/messages/messages.html')


@app.route('/messages/add')
def add_messages():
    return render_template('pages/messages/add_messages.html')


@app.route('/contacts')
def contacts():
    return render_template('pages/contacts/contacts.html')


@app.route('/contacts/add', methods=["POST","GET"])
def add_contacts():
    if request.method == "POST":
        return "POSTED"
    else:
        return render_template('pages/contacts/add_contacts.html')
        

@app.route('/groups')
def groups():
    return render_template('pages/groups/groups.html')


@app.route('/groups/add', methods=["POST","GET"])
def add_groups():
    if request.method == "GET":
        return render_template('pages/groups/add_groups.html')
    else:
        book = Groups(group_name=request.form.get("group_name"), link="test")
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('groups'))


@app.route('/settings')
def settings():
    return render_template('pages/settings/settings.html')


@app.route('/logout')
def logout():
    return render_template('pages/logout.html')
    

if __name__ == "__main__":
    app.run(debug=True, port=8081)
