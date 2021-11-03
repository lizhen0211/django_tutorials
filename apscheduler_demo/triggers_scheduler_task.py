from datetime import datetime, date
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")


    # 测试任务func
    def job_func(text):
        print(text + " 当前时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


    def job_block_func(text):
        print(text + " 当前时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        sleep(2 * 60)


    # datetime类型（用于精确时间）
    # scheduler.add_job(job_func, 'date', run_date=date(2021, 11, 2), args=['测试任务 date'])

    # 在某个时刻运行一次 job_func 方法
    # scheduler.add_job(job_func, 'date', run_date=datetime(2021, 11, 1, 11, 40, 0), args=['测试任务 datetime'])

    # 注意：run_date参数可以是date类型、datetime类型或文本类型。
    # scheduler.add_job(job_func, 'date', run_date='2021-11-1 11:43:05', args=['测试任务 str'])

    # 每2小时触发
    # scheduler.add_job(job_func, 'interval', minutes=2, args=['interval 1'])

    # 在 2019-04-15 17:00:00 ~ 2019-12-31 24:00:00 之间, 每隔两分钟执行一次 job_func 方法
    # scheduler.add_job(job_func, 'interval', minutes=2, args=['interval 2'], start_date='2021-11-01 00:00:00',
    #                   end_date='2021-11-05 23:59:59')

    # jitter振动参数，给每次触发添加一个随机浮动秒数，一般适用于多服务器，避免同时运行造成服务拥堵。
    # scheduler.add_job(job_func, 'interval', minutes=2, jitter=20, args=['interval jitter'])

    scheduler.add_job(job_block_func, 'interval', minutes=1, args=['interval jitter'])

    # scheduler.add_job(job_block_func, 'interval', seconds=1, args=['interval jitter'])

    # =======================================================================================================

    # 在每年 1-3、7-9 月份中的每个星期一、二中的 00:00, 01:00, 02:00 和 03:00 执行 job_func 任务
    # scheduler.add_job(job_func, 'cron', month='1-3,7-9', day='1,2', hour='0-3', args=['测试任务 cron'])

    # scheduler.add_job(job_func, 'cron', minute='0-59', args=['测试任务 cron'])

    scheduler.add_job(job_func, 'cron', day_of_week='1-5', hour=15, minute=32, end_date='2022-12-31',
                      args=['测试任务 cron'])

    # @scheduler.scheduled_job('cron', id='my_job_id', day='last sun')
    # def some_decorated_task():
    #     print("I am printed at 00:00:00 on the last Sunday of every month!")

    # =======================================================================================================
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
