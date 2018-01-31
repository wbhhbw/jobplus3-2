import os
import json
from jobplus.models import User, Company, Job, db
from faker import Factory
from random import randint

# 本地化fake
fake = Factory.create('zh_CN')


def iter_company_user():
    for i in range(63):
        yield User(
            username=fake.lexify(text='??????'),
            email=fake.email(),
            password=fake.bothify(text='???##?'),
            role=20
        )


# 从datas中读取公司数据测试数据
def iter_companies():
    count = 1
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'company_detail.json')) as f:
        companies = json.load(f)
    for company in companies:
        user = User.query.get(count)
        count += 1
        yield Company(
            name=company['company_name'],
            address=fake.address(),
            logo_url=company['logo_url'],
            website=fake.url(),
            slogan=company['companyFeatures'],
            field=company['field'],
            financeStage=company['financeStage'],
            description=fake.text(),
            user=user
        )


def iter_jobs():
    for company in Company.query:
        # 每个公司生成3~10个职位
        for i in range(randint(3, 10)):
            yield Job(
                name=fake.word() + '工程师',
                salary_low=randint(4, 10),
                salary_high=randint(10, 20),
                experience='1-3年',
                location=fake.city(),
                description=fake.paragraph(
                    nb_sentences=3, variable_nb_sentences=True),
                requirements=fake.paragraph(
                    nb_sentences=3, variable_nb_sentences=True),
                company=company
            )


def run():
    for user in iter_company_user():
        db.session.add(user)
   

    for company in iter_companies():
        db.session.add(company)


    for job in iter_jobs():
        db.session.add(job)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

