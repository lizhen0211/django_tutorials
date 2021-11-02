import os
import time

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

if __name__ == '__main__':
    # 测试任务func
    def job_func():
        os.system('python ../manage.py task_command')


    '''
        Starting the scheduler is done by simply calling start() on the scheduler. 
        For schedulers other than BlockingScheduler, 
        this call will return immediately and you can continue the initialization process of your application,
        possibly adding jobs to the scheduler.
        For BlockingScheduler, you will only want to call start() after you’re done with any initialization steps.
    '''
    # https://www.cnblogs.com/quijote/p/4385774.html 参数说明
    jobstores = {
        # 'mongo': MongoDBJobStore(),
        # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    '''
        coalesce：当由于某种原因导致某个job积攒了好几次没有实际运行（比如说系统挂了5分钟后恢复，有一个任务是每分钟跑一次的，
        按道理说这5分钟内本来是“计划”运行5次的，但实际没有执行），如果coalesce为True，下次这个job被submit给executor时，只会执行1次，
        也就是最后这次，如果为False，那么会执行5次（不一定，因为还有其他条件，看后面misfire_grace_time的解释）
        
        max_instance: 就是说同一个job同一时间最多有几个实例再跑，比如一个耗时10分钟的job，被指定每分钟运行1次，
        如果我们max_instance值为5，那么在第6~10分钟上，新的运行实例不会被执行，因为已经有5个实例在跑了
        
        misfire_grace_time：设想和上述coalesce类似的场景，如果一个job本来14:00有一次执行，但是由于某种原因没有被调度上，
        现在14:01了，这个14:00的运行实例被提交时，会检查它预订运行的时间和当下时间的差值（这里是1分钟），大于我们设置的30秒限制，
        那么这个运行实例不会被执行。
    '''
    job_defaults = {
        'coalesce': False,
        'max_instances': 5
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    scheduler.add_job(job_func, 'interval', minutes=1)
    # scheduler.add_job(job_func, 'interval', minutes=1, args=['config'])

    scheduler.start()

    # BackgroundScheduler 运行在Backgroud，但是并不会阻止主程序自己终止，而主程序终止后，BackgroundScheduler 也会终止。
    try:
        while True:
            time.sleep(50)
    except (KeyboardInterrupt, SystemExit):
        pass
