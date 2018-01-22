from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    """所有model的一个基类，默认添加了时间戳
    """

    # 表示不要把这个类当作 Model 类，不映射到数据库
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 该表为求职者与职位的关联表，用于实现用户收藏职位功能，由SQLAlchemy自动接管
user_job = db.Table('user_job',
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
    # 用户收藏职位
    collect_jobs = db.relationship('Job', secondary='user_job')
    upload_resume_ulr = db.Column(db.String(64))
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
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.String(32))
    location = db.Column(db.String(32))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    #公司与职位是一对多的关系，uselist设置为False
    company = db.relationship('Company', uselist=False)

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
    field = db.Column(db.String(32))
    financeStage = db.Column(db.String(32))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    # 一对一关系，双向都设置uselist为False
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company:{}>'.format(self.name)


class Dilivery(Base):
    """求职者与职位关联表
    """
    __tablename__ = 'delivery'

    # 企业回应状态
    # 已投递
    STATUS_POSTED = 1
    # 被查看
    STATUS_CHECKED = 2
    # 被拒绝
    STATUS_REJECT = 3
    # 被接收，等待面试通知
    STATUS_ACCEPT = 5

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey(
        'job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_POSTED)
    # 企业回应
    response = db.Column(db.String(256))