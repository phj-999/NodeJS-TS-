from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(15) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱地址', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):  # 相当于django的__str__
        return f"<{self.name} {self.__class__.__name__}>"

class Course(db.Model):
    """课程模型"""
    """
        CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '课程', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )

    """
    __tablename__ = "tb_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    price = db.Column(db.Numeric(8, 2), comment="价格")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Teacher(db.Model):
    """老师模型"""
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT,
        name VARCHAR(255) COMMENT '姓名',
        `option` ENUM('讲师','助教','班主任'),
        PRIMARY KEY (id),
        UNIQUE (name)
    )
    """
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"


@app.route("/data")
def data():
    """按主键获取一条"""
    # student = Student.query.get(1)
    # if student:
    #     print(student.name)
    #
    # student = Student.query.get(100)
    # if student:
    #     print(student.name)

    """获取查询结果的所有数据"""
    # # 如果不设置条件，则默认查询全表
    # student_list = Student.query.all()
    # print(student_list)
    #
    # # 设置过滤条件查询全部结果
    # # 如果查不到数据，返回空列表
    # student_list = Student.query.filter(Student.sex==False).all()
    # print(student_list)
    #
    # # all()的返回值是一个python列表，可以直接使用切片，与django的QuerySet完全不是一回事。
    # student_list = Student.query.all()[1:]
    # print(student_list)


    """统计查询结果的数量"""
    # # 如果不设置过滤条件，则默认统计全表记录的数量
    # total = Student.query.count()
    # print(total)
    #
    # # 设置条件，作为返回满足条件的记录数量
    # total = Student.query.filter(Student.age>16).count()
    # print(total)

    """获取查询结果的第一个结果"""
    student = Student.query.first()
    print(student, student.name)

    student = Student.query.filter(Student.sex==True).first()
    print(student, student.name)

    """获取查询结果的最后一个结果"""
    student = Student.query.filter(Student.sex==True)[-1]
    print(student, student.name)

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
        # 如果数据库中已经声明了有数据表，则不会继续生成
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
