
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
    sender_id = Column(Integer, ForeignKey('sender.id'))
    date_added = Column('date_added', TIMESTAMP)


    def __init__(self, group_name, user, date_added, sender_id):
        self.id = id
        self.group_name = group_name
        self.user = user
        self.sender_id = sender_id
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
    joined_group = relationship("Joined_groups")

    def __init__(self, phone, user, date, sender_name, status):
        self.id = id
        self.phone = phone
        self.user = user
        self.date = date
        self.status = status
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
