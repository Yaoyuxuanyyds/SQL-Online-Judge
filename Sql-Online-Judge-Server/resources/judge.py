from exts import db
import time, models
from flask_restful import Resource, fields, marshal_with
from common.comm import auth_role, auth_all
from config import *
from flask import request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, TimeoutError, OperationalError
from sqlalchemy.orm import sessionmaker

# 定义返回结果的字段
submit_judge = {
    'submit_sql': fields.String,
    'question_id': fields.Integer
}

class SQLJudge(Resource):
    @auth_all()
    @marshal_with(submit_judge)
    def execute_sql(self, code):
        """
        运行SQL代码，并捕获可能的错误和异常
        :param code: 要执行的SQL代码
        :return: 执行结果，格式为 (error: bool, msg: str)
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://test:4546@localhost/testdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            start_time = time.time()  # 记录开始时间
            
            result = session.execute(text(code))  # 执行SQL代码
            session.commit()  # 提交事务

            if result.returns_rows:  # 如果返回结果
                output = result.fetchall()  # 获取所有结果
            else:
                output = None  # 如果没有返回结果，设置为None

            elapsed_time = time.time() - start_time  # 计算执行时间

            if elapsed_time > 5:  # 判断是否超时
                return (True, "TLE")  # 超时返回TLE

            return (False, str(output))  # 返回执行结果

        except OperationalError as e:  # 捕获操作错误异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        except TimeoutError:  # 捕获超时异常
            session.rollback()  # 回滚事务
            return (True, "TLE")  # 返回超时错误信息
        except SQLAlchemyError as e:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        finally:
            session.close()  # 关闭会话

    def drop_tables(self, tablename):
        """
        删除指定的表，避免数据干扰
        :param tablename: 需要删除的表名（可能有多个表名，以逗号分隔）
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://low_permission_user:password@localhost/testdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            # 关闭外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            # 删除指定表
            session.execute(text(f'DROP TABLE IF EXISTS {tablename};'))
            # 重新打开外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            session.commit()  # 提交事务
        except SQLAlchemyError:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
        finally:
            session.close()  # 关闭会话

    def judge(self, submit_sql, question_id):
        """
        根据question_id从测试用例表读取对应的input_sql和output_sql，执行用户提交的SQL语句并判断结果
        :param submit_sql: 用户提交的SQL语句
        :param question_id: 问题ID
        :return: 测试结果字典，格式为 {测试用例ID: (error: bool, output: int)}
        """
        # 从TestCase表中获取对应question_id的所有测试用例
        test_cases = models.TestCase.query.filter_by(question_id=question_id).all()
        results = {}  # 存储测试结果的字典
        
        for test_case in test_cases:  # 遍历每个测试用例
            test_id = test_case.id  # 获取测试用例ID
            input_sql = test_case.input_sql  # 获取输入SQL
            expected_output = test_case.output  # 获取预期输出
            tablename = test_case.tablename  # 获取表名

            # 清理当前的表，避免表已存在造成干扰
            self.drop_tables(tablename)

            # 执行建表语句，初始化表结构
            error, setup_msg = self.execute_sql(input_sql)
            if error:  # 如果建表语句执行出错
                results[test_id] = (True, 1)  # 返回错误信息
                continue

            # 执行用户提交的SQL
            error, user_output = self.execute_sql(submit_sql)

            if error:  # 如果用户SQL执行出错
                if user_output == "TLE":  # 判断是否超时
                    results[test_id] = (True, 3)
                elif "MemoryError" in user_output:  # 判断是否内存溢出
                    results[test_id] = (True, 4)
                else:  # 其他错误
                    results[test_id] = (True, 1)
            elif user_output != expected_output:  # 判断输出是否正确
                results[test_id] = (True, 2)  # 输出错误
            else:
                results[test_id] = (False, 0)  # 正确通过

        return results  # 返回测试结果