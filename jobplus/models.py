from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    """所有model的一个基类，默认添加了时间戳
    """

    # 表示不要把这个类当作 Model 类，不映射到数据库
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 该表为求职者与职位的关联表，由SQLAlchemy自动接管
registrations = db.Table('registrations',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('job_id', db.Integer, db.ForeignKey('job.id')))


class User(Base):
    __tablename__ = 'user'

    # 用数值表示角色，方便判断是否有权限，比如说有个操作要角色为员工
    # 及以上的用户才可以做，那么只要判断 user.role >= ROLE_STAFF
    # 就可以了，数值之间设置了 10 的间隔是为了方便以后加入其它角色
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True,
                         index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)

    # 默认情况下，sqlalchemy 会以字段名来定义列名，但这里是 _password, 所以明确指定数据库表列名为 password
    _password = db.Column('password', db.String(256), nullable=False)
    fullname = db.Column(db.String(32), unique=True,
                         index=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'company.id', ondelete='CASCADE'), default=0)
    company = db.relationship('Company', uselist=False)
    phone_num = db.Column(db.String(32), unique=True,
                          index=True, nullable=False)

    # 多对多的关系可以在任何一张表中定义，此处定义在user表中，backref处理关系另一侧
    jobs = db.relationship('job', secondary=registrations, backref=db.backref('user', lazy='dynamic'),
                           lazy='dynamic')
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        """这样设置user.password就会自动为password生成哈希值存入_password字段"""
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """判断用户输入的密码和存储的hash密码是否相等"""
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    salary = db.Column(db.String(32))
    experience = db.Column(db.String(32))
    location = db.Column(db.String(32))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True,
                     index=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    logo_url = db.Column(db.String(256))
    website = db.Column(db.String(256))
    slogan = db.Column(db.String(256))
    description = db.Column(db.Text)
    user = db.relationship('User', uselist=False)

    def __repr__(self):
        return '<Company:{}>'.format(self.name)

