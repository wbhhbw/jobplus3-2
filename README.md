# jobplus3-2
LouPlus Team 2 https://www.shiyanlou.com/louplus/python

* [wbhhbw](https://github.com/wbhhbw)

## 数据库设计

* 职位与求职者是多对多的关系，一个求职者可以申请多个职位，每个职位又能供多个求职者申请，此处为了避免过多的冗余信息，需要设计第三张表，求职表`registrations`。包含两个字段，求职者和职位，分别对应求职者的id和职位的id
* 企业用户与企业表是一对一关系  `uselist`采用`False`参数，用户表中的company_id与企业表的id字段关联，用户表中的company_id字段默认为0（即为非企业用户）
