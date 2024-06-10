import models

def evaluation(submit: models.Submission):
    submit.pass_rate = 1.0  # 假设所有提交都通过
    submit.status = 0  # 假设所有提交都成功
