from datetime import datetime, date

from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")


    # 测试任务func
    def job_func(text):
        print(text)


    # datetime类型（用于精确时间）
    scheduler.add_job(job_func, 'date', run_date=date(2021, 11, 2), args=['测试任务 date'])

    # 在某个时刻运行一次 job_func 方法
    scheduler.add_job(job_func, 'date', run_date=datetime(2021, 11, 1, 11, 40, 0), args=['测试任务 datetime'])

    # 注意：run_date参数可以是date类型、datetime类型或文本类型。
    scheduler.add_job(job_func, 'date', run_date='2021-11-1 11:43:05', args=['测试任务 str'])

    scheduler.start()
