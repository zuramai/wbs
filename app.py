from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime, time, csv, sys,unicodedata
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import Column, String, TIMESTAMP, Text, Time, Date, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from selenium.common.exceptions import NoSuchElementException
from classes.messages_add import Send

app = Flask(__name__)
login = LoginManager()
login.init_app(app)


app.secret_key = "Flash"
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:''@localhost:3306/wbs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_url = "http://localhost:8081/"
date_now = datetime.datetime.today().strftime('%Y-%m-%d')
time_now = datetime.datetime.now().strftime("%H:%M:%S")

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column('id', primary_key=1)
    name = Column('name', String(50))
    username = Column('username', String(50))
    password = Column('password', String(255))
    email = Column('email', String(255))
    picture = Column('picture', String(255))
    registered_at = Column('registered_at', Date())

    def __init__(self, name, username, password, email, picture, registered_at):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.picture = picture
        self.registered_at = registered_at

class Groups(db.Model):
    __tablename__ = "Groups"
    id = Column("id", primary_key=1)
    group_name = Column('group_name', String(32))
    link = Column('link', String(32))
    date_added = Column('date_added', TIMESTAMP)

    def __init__(self, group_name, link, date_added):
        self.id = id
        self.group_name = group_name
        self.link = link
        self.date_added = date_added

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Contacts_grouping(db.Model):
    __tablename__ = "contacts_grouping"
    id = Column('id', primary_key=1)
    group_name = Column('group_name', String(100))
    phone = Column('phone', String(14))
    user = Column('user', String(100))
    date = Column('date', Date())

    def __init__(self, group_name, phone, user, date):
        self.id = id
        self.group_name = group_name
        self.phone = phone
        self.user = user
        self.date = date

class Joined_groups(db.Model):
    __tablename__ = "joined_groups"
    id = Column("id", primary_key=1)
    group_name = Column('group_name', String(255))
    user = Column('user', String(100))
    date_added = Column('date_added', TIMESTAMP)

    def __init__(self, group_name, user, date_added):
        self.id = id
        self.group_name = group_name
        self.user = user
        self.date_added = date_added

class Contacts(db.Model):
    __tablename__ = "contacts"
    id = Column("id", primary_key=1)
    phone = Column("phone", String(15))
    name = Column("name", String(100))
    date_added = Column("date_added", TIMESTAMP)

    def __init__(self, phone, name, date_added):
        self.id = id
        self.phone = phone
        self.name = name
        self.date_added = date_added


class Sender(db.Model):
    __tablename__ = "sender"
    id = Column('id', primary_key=1)
    phone = Column('phone', String(14))
    user = Column('user', String(100))
    sender_name = Column('sender_name', String(100))
    status = Column('status', String(20))
    date = Column('date', Date())

    def __init__(self, phone, user, date, sender_name):
        self.id = id
        self.phone = phone
        self.user = user
        self.date = date
        self.sender_name = sender_name


class Messages(db.Model):
    __tablename__ = "messages"
    id = Column("id", primary_key=1)
    user = Column('user', String(100))
    sender = Column('sender', String(14))
    receiver = Column('receiver', String(14))
    msg = Column('msg', Text())
    date = Column('date', Date())
    time = Column('time', Time())

    def __init__(self, sender, receiver, msg, date, time):
        self.id = id
        self.sender = sender
        self.user = current_user.username
        self.receiver = receiver
        self.msg = msg
        self.date = date
        self.time = time

def checkElementExist(element_class):
    try:
        webdriver.find_element_by_class_name(element_class)
    except NoSuchElementException:
        return False
    return True

def waitForButtonSend(driver):
    i = 0
    while i == 0:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_35EW6"))
            )
            i = 1
        except:
            i = 0



@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@app.route('/index')
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username, password=password).first()

            if user is None:
                flash("Invalid credentials", 'danger')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('index'))


    else:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('pages/users/login.html')

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        if (fullname is None) or (email is None) or (password is None) or (username is None):
            return redirect(url_for('register'))
            flash("Please complete the form", "danger")

        regs = User(name=fullname,username=username,password=password,email=email,picture='default.png',registered_at=date_now)
        db.session.add(regs)
        db.session.commit()

        flash("Success register! Now you can login", "success")
        return redirect(url_for('login'))
    else:
        return render_template('pages/users/register.html')

@app.route('/logged')
@login_required
def logged():
    return "Hello, "+current_user.email

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/settings')
@login_required
def settings():
    data_user = User.query.filter_by(id=current_user.id)
    return render_template('pages/users/settings.html', data=data_user)


@app.route('/messages')
def messages():
    delete = request.args.get('delete')
    if delete:
        Messages.query.filter_by(id=delete).delete()
        db.session.commit()

        flash('Success delete messages!', 'success')
        return redirect(url_for('messages'))
    message_list = Messages.query.all()
    return render_template('pages/messages/messages.html', messages= message_list)


@app.route('/messages/add', methods=["POST","GET"])
def add_messages():
    if request.method == "GET":
        all_groups = Contacts_grouping.query.filter_by(user=current_user.username).group_by(Contacts_grouping.group_name).all()
        return render_template('pages/messages/add_messages.html', data=all_groups, datas= all_groups)

    elif request.method == 'POST':
        type = request.form["type"]
        target = request.form["target"]
        msg = request.form['msg']
        senderType = request.form['sender']

        if senderType == "chooseSender":
            senders = request.form.getlist("senders")

            for countSender in senders:
                app.logger.info(senders)
        elif senderType == "randomSender":
            numSender = request.form['number_of_senders']
            activeSenderCount = Sender.query.filter_by(status='Active', user=current_user.username).count()

            if int(numSender) > activeSenderCount:
                flash("You only have {} sender active".format(activeSenderCount), 'danger')
                return redirect('messages/add')
        else:
            flash("Internal error.", 'danger')
            return redirect('messages/add')

        driver = webdriver.Chrome()

        if type == "single":
            driver.get('https://web.whatsapp.com/send?phone=' + target + '&text=' + msg)
            time.sleep(10)

            waitForButtonSend(driver)
            send = Send(driver, db, date_now, time_now)
            send.single(target, msg, Messages)

            flash('Message sent!', 'success')
            return redirect(url_for('messages'))

        elif type == "all":
            all_contacts = Contacts.query.all()
            for contacts in all_contacts:
                driver.get('https://web.whatsapp.com/send?phone=' + contacts.phone + '&text=' + msg)
                time.sleep(10)

                waitForButtonSend(driver)

                text = driver.find_element_by_class_name('_2S1VP')
                text.send_keys(msg)

                time.sleep(1)
                element = driver.find_element_by_class_name('_35EW6')
                element.click()

                messages = Messages("081380353611", target, msg, date_now, time_now)
                db.session.add(messages)
                db.session.commit()

                time.sleep(1)
            driver.close()
            flash("Success send messages to all contacts!", "success")
            return redirect("messages/add")
        elif type == "groups":
            joined_group = Joined_groups.query.all()

            driver.get("https://web.whatsapp.com/")
            waitForButtonSend(driver)
            groups_name = []
            for join_group in joined_group:
                groups_name.append(join_group.group_name)

            for group_name in groups_name:
                searchbox = driver.find_element_by_class_name("jN-F5")

                time.sleep(1)

                searchbox.send_keys(group_name)
                searchbox.send_keys(Keys.ENTER)

                text = driver.find_element_by_class_name('_2S1VP')
                text.send_keys(msg)

                time.sleep(1)
                element = driver.find_element_by_class_name('_35EW6')
                element.click()

                time.sleep(1)

            flash("Messages sent!", 'success')
            return redirect('messages')
        elif type == "cgroups":
            selected_groups = request.form.getlist('cgroups')
            for selected in selected_groups:

                contacts = Contacts_grouping.query.filter_by(group_name=selected)
                for number in contacts:
                    driver.get('https://web.whatsapp.com/send?phone={}&text={}'.format(number.phone, msg))

                    # WAIT FOR ELEMENT SEND BUTTON CAN BE CLICKED
                    i = 0
                    while i == 0:
                        try:
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "_35EW6"))
                            )
                            i = 1

                            # CHECK IF THERE IS AN ERROR OR NOT
                            try:
                                popup = driver.find_element_by_css_selector('._1CnF3')
                            except NoSuchElementException:
                                print("No elements found")
                            else:
                                continue
                        except:
                            i = 0

                    time.sleep(1)

                    element = driver.find_element_by_class_name('_35EW6')
                    element.click()

                    messages = Messages("081380353611", target, msg, date_now, time_now)
                    db.session.add(messages)
                    db.session.commit()

                    time.sleep(1)
                return "waiting success"



@app.route('/contacts', methods=["GET","POST"])
def contacts():
    if request.method == "GET":
        delete = request.args.get('delete')
        if delete:
            Contacts.query.filter_by(id=delete).delete()
            db.session.commit()

            flash("Success delete contact", 'success')
            return redirect("contacts")
        else:
            contacts_list = Contacts.query.limit(5)
            return render_template('pages/contacts/contacts.html', contacts=contacts_list)



    else:
        file = request.files['contacts']
        file.save("static/files/csv/"+file.filename)

        csv_url = base_url+"static/files/csv/"+file.filename
        with open("static/files/csv/"+file.filename) as csv_file:
            readcsv = csv.reader(csv_file, delimiter=",")
            name = []
            listNo = []
            for row in readcsv:
                listNo.append(row[1])
                name.append(row[0])

            num = 0
            while num <= len(listNo):
                nomor = listNo[num]
                nama = name[num]
                contact = Contacts(phone=nomor, name=nama, date_added=date_now)
                db.session.add(contact)
                db.session.commit()

                num += 1

            flash("Success import contacts", "success")
            return redirect(url_for('contacts'))

@app.route('/contacts/grouping', methods=['GET','POST'])
def grouping():
    if request.method == 'GET':
        all_groups2 = Contacts_grouping.query.with_entities(Contacts_grouping.id, Contacts_grouping.group_name, func.count(Contacts_grouping.phone).label("count")).group_by(Contacts_grouping.group_name).all()
        return render_template('pages/contacts/grouping/grouping.html', data=all_groups2)
        # app.logger.info(all_groups2)
    else:
        phone = request.form['phone']
        group_name = request.form['name']
        count = request.form['count']
        listPhone = phone.splitlines()

        for line in listPhone:
            newphone = line.replace('0','62', 1)
            C = Contacts_grouping(group_name, newphone, current_user.username, date_now)
            db.session.add(C)
            db.session.commit()
            app.logger.info(newphone)

        return "success"

@app.route('/contacts/grouping/edit/<id>', methods=['GET','POST'])
def update(id):
    if request.method == 'GET':
        all = Contacts_grouping.query.filter_by(id=id)
        for a in all:
            group_name = a.group_name
        list_contacts = Contacts_grouping.query.filter_by(group_name=group_name)
        return render_template('pages/contacts/grouping/update.html', data=all, list_contacts=list_contacts)
    else:
        group_name = request.form['name']
        phone_list = request.form['phone']

        result = [x.strip() for x in phone_list.split(',')]

        for no in result:
            app.logger.info(no)
            check = Contacts_grouping.query.filter_by(phone=no).count()

            if check == 0:
                ins = Contacts_grouping(group_name=group_name, phone=no, user=current_user.username, date=date_now)
                db.session.add(ins)
                db.session.commit()

            else:
                continue



        flash("Success update data!", 'success')
        return redirect(url_for('contacts') + "/grouping")


@app.route('/contacts/add', methods=["POST","GET"])
def add_contacts():
    if request.method == "POST":
        return "POSTED"
    else:
        return render_template('pages/contacts/add_contacts.html')


@app.route('/groups')
def groups():
    grup = Groups.query.all()
    return render_template('pages/groups/groups.html', grup=grup)

@app.route('/groups/joined_groups', methods=['GET', 'POST'])
def Joined():
    if request.method == "GET":
        delete = request.args.get('delete')

        if delete:
            Joined_groups.query.filter_by(id=delete).delete()
            db.session.commit()

            flash('Success delete joined groups', 'success')
            return redirect('groups/joined_groups')
        else:
            joined_groups_all = Joined_groups.query.all()
            return render_template('pages/groups/joined_groups.html', data=joined_groups_all)
    else:
        group_name = request.form['name']

        logged_user = current_user.username
        G = Joined_groups(group_name, logged_user, date_now)

        db.session.add(G)
        db.session.commit()

        flash('Success add joined group!', 'success')
        return redirect(url_for('groups')+'/joined_groups')


@app.route('/groups/joined_groups/import')
def import_groups():
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')

    i=0
    while i == 0:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_2wP_Y"))
            )
            i = 1
        except:
            i = 0
    driver.execute_script("document.getElementById('app').style.height = 'auto';")
    driver.execute_script("document.querySelector('body').style.overflow = 'scroll';")
    driver.execute_script("document.querySelector('html').style.overflow = 'scroll';")

    time.sleep(10)
    list_all = driver.find_elements_by_css_selector("._1wjpf:not(._3NFp9)")
    time.sleep(5)


    list_name = []
    for list in list_all:
        list_name.append(list.text)
        app.logger.info(list.text)

    for list_group in list_name:
        staleElement = False
        while staleElement == False:
            try:
                app.logger.warning(list_group)
                staleElement = True
            except:
                staleElement = False
                return "Please reload to try again"

        searchbox = driver.find_element_by_class_name("jN-F5")

        time.sleep(1)

        searchbox.send_keys(list_group)
        searchbox.send_keys(Keys.ENTER)

        time.sleep(2)

        # Click the burget btn
        burger_btn = driver.find_element_by_css_selector('._1i0-u [title=Menu]')
        burger_btn.click()

        # Check is this a group or not

        try:
            info = driver.find_element_by_css_selector('[title="Group info"]')
            driver.implicitly_wait(10)

            J = Joined_groups(list_group, current_user.username, date_now)
            db.session.add(J)
            db.session.commit()
        except:
            continue








    flash('Success add groups', 'success')
    return redirect(url_for('groups')+'/joined_groups')





@app.route('/groups/add', methods=["POST","GET"])
def add_groups():
    if request.method == "GET":
        return render_template('pages/groups/add_groups.html')
    else:
        if 'manual' in request.form:
            group_name = request.form['name']
            link = request.form['link']

            G = Groups(group_name=group_name, link=link, date_added=date_now)
            db.session.add(G)
            db.session.commit()

            flash("Success add group!", "success")
            return redirect(url_for("groups"))

        elif 'scrape' in request.form:
            keyword = request.form['keyword']

            driver = webdriver.Chrome()
            driver.get(
                "http://ngarang.com/link-grup-wa/daftar-link-grup-wa.php?search={}&searchby=name".format(keyword))
            driver.implicitly_wait(2)
            num = 1
            nextPage = driver.find_elements_by_css_selector("#prev_next > a")

            countNextPage = len(nextPage)

            if countNextPage == 2:
                btnNextPage = driver.find_element_by_css_selector("#prev_next > a:nth-child(2)")
            else:
                btnNextPage = driver.find_element_by_css_selector("#prev_next > a:nth-child(1)")

                if btnNextPage.text == "Halaman berikutnya":
                    btnNextAvailable = True
                else:
                    btnNextAvailable = False

            while btnNextAvailable == True or btnNextAvailable == False:
                titles = driver.find_elements_by_class_name("wa-chat-title-text")
                links = driver.find_elements_by_css_selector(".URLMessage")
                listLinks = []
                listTitle = []

                for link in links:
                    listLinks.append(link.text)

                for title in titles:
                    listTitle.append(title.text)

                list = 0
                while list <= 23:
                    app.logger.info(listTitle[list])
                    G = Groups(group_name=listTitle[list], link=listLinks[list], date_added=date_now)
                    db.session.add(G)
                    db.session.commit()
                    list += 1

                nextPage = driver.find_elements_by_css_selector("#prev_next > a")

                countNextPage = len(nextPage)

                if countNextPage == 2:
                    btnNextPage = driver.find_element_by_css_selector("#prev_next > a:nth-child(2)")
                else:
                    btnNextPage = driver.find_element_by_css_selector("#prev_next > a:nth-child(1)")

                    if btnNextPage.text == "Halaman berikutnya":
                        btnNextAvailable = True
                    else:
                        btnNextAvailable = False

                if btnNextAvailable == False:
                    break
                else:
                    nextPageClicked = False
                    while nextPageClicked == False:
                        try:
                            app.logger.info(btnNextPage.text)
                            btnNextPage.click()
                            nextPageClicked = True
                        except WebDriverException:
                            nextPageClicked = False


            driver.close()
            flash("Success grab all groups with keyword "+keyword, "success")
            return redirect("groups")
        elif 'manual' in request.form:
            return "MANUAL"
        else:
            return "NOTHING"

@app.route('/groups/join', methods=["GET"])
def join_group():
    group_links = Groups.query.all()
    driver = webdriver.Chrome()
    for group_link in group_links:
        driver.get(group_link.link)
        driver.implicitly_wait(5)

        btn = driver.find_element_by_id('action-button')
        btn.click()

        waitingDone = False

        while waitingDone == False:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "PNlAR")))
                waitingDone = True
            except WebDriverException:
                waitingDone = False


        btn_join = driver.find_element_by_class_name("PNlAR")
        btn_join.click()

    flash('Success join all group!', 'success')
    return redirect(url_for('groups'))


@app.route('/sender', methods=['GET','POST'])
def sender():
    if request.method == 'GET':
        if request.args.get('edit'):
            edit = request.args.get('edit')
            all = Sender.query.filter_by(id=edit).all()

            return render_template('pages/sender/edit_sender.html', data=all)
        elif request.args.get('delete'):
            delete = request.args.get('delete')
            Sender.query.filter_by(id=delete).delete()
            db.session.commit()

            flash("Success delete senders", 'success')
            return redirect(url_for('messages'))

        all = Sender.query.filter_by(user=current_user.username).all()
        return render_template('pages/sender/sender.html', data=all)
    else:
        id = request.form['id']
        phone = request.form['phone']
        name = request.form['name'];

        sender = Sender.query.filter_by(id=id).one()
        sender.sender_name = name
        sender.phone = phone
        db.session.commit()

        flash("Success edit data!", 'success')
        return redirect(url_for('sender'))


@app.route('/sender/add', methods=['GET','POST'])
def add_sender():
    if request.method == "GET":
        return render_template('pages/sender/add_sender.html')
    else:

        name = request.form['name']
        phone = request.form['phone']

        S = Sender(phone, current_user.username, date_now, name)
        db.session.add(S)
        db.session.commit()

        flash("Success add sender!",'success')
        return redirect('sender')

if __name__ == "__main__":
    app.run(debug=True, port=8081)
