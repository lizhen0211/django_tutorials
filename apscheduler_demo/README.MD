##参考文档
 http://www.chenxm.cc/article/829.html
##介绍：
APScheduler的全称是Advanced Python Scheduler。它是一个轻量级的 Python 定时任务调度框架。APScheduler 支持三种调度任务：固定时间间隔，固定时间点（日期），Linux 下的 Crontab 命令。同时，它还支持异步执行、后台执行调度任务。
##安装:
pip install apscheduler
##基本概念
###1. APScheduler四大组件：
1、触发器 triggers ：用于设定触发任务的条件
2、任务储存器 job stores：用于存放任务，把任务存放在内存或数据库中
3、执行器 executors： 用于执行任务，可以设定执行模式为单线程或线程池
4、调度器 schedulers： 把上方三个组件作为参数，通过创建调度器实例来运行

1.1 触发器 triggers
触发器包含调度逻辑。每个任务都有自己的触发器，用于确定何时应该运行作业。除了初始配置之外，触发器完全是无状态的。

1.2 任务储存器 job stores
默认情况下，任务存放在内存中。也可以配置存放在不同类型的数据库中。如果任务存放在数据库中，那么任务的存取有一个序列化和反序列化的过程，
同时修改和搜索任务的功能也是由任务储存器实现。

**注意：一个任务储存器不要共享给多个调度器，否则会导致状态混乱**

1.3 执行器 executors
任务会被执行器放入线程池或进程池去执行，执行完毕后，执行器会通知调度器。

1.4 调度器 schedulers
一个调度器由上方三个组件构成，一般来说，一个程序只要有一个调度器就可以了。
开发者也不必直接操作任务储存器、执行器以及触发器，因为调度器提供了统一的接口，通过调度器就可以操作组件，比如任务的增删改查。

##2. 调度器组件详解

根据开发需求选择相应的组件，下面是不同的调度器组件：

1、BlockingScheduler 阻塞式调度器：适用于只跑调度器的程序。
2、BackgroundScheduler 后台调度器：适用于非阻塞的情况，调度器会在后台独立运行。
3、AsyncIOScheduler AsyncIO调度器，适用于应用使用AsnycIO的情况。
4、GeventScheduler Gevent调度器，适用于应用通过Gevent的情况。
5、TornadoScheduler Tornado调度器，适用于构建Tornado应用。
6、TwistedScheduler Twisted调度器，适用于构建Twisted应用。
7、QtScheduler Qt调度器，适用于构建Qt应用。

##2.1 任务储存器的选择

要看任务是否需要持久化。如果你运行的任务是无状态的，选择默认任务储存器MemoryJobStore就可以应付。
但是，如果你需要在程序关闭或重启时，保存任务的状态，那么就要选择持久化的任务储存器。
如果，作者推荐使用SQLAlchemyJobStore并搭配PostgreSQL作为后台数据库。这个方案可以提供强大的数据整合与保护功能。

##2.2 执行器的选择

同样要看你的实际需求。默认的ThreadPoolExecutor线程池执行器方案可以满足大部分需求。
如果，你的程序是计算密集型的，那么最好用ProcessPoolExecutor进程池执行器方案来充分利用多核算力。
也可以将ProcessPoolExecutor作为第二执行器，混合使用两种不同的执行器。
配置一个任务，就要设置一个任务触发器。触发器可以设定任务运行的周期、次数和时间。

##3. APScheduler有三种内置的触发器：
1、date 日期：触发任务运行的具体日期
2、interval 间隔：触发任务运行的时间间隔
3、cron 周期：触发任务运行的周期
4、calendarinterval：当您想要在一天中的特定时间以日历为基础的间隔运行任务时使用

一个任务也可以设定多种触发器，比如，可以设定同时满足所有触发器条件而触发，或者满足一项即触发。

##3.0 触发器代码示例
3.1 date 是最基本的一种调度，作业任务只会执行一次。它表示特定的时间点触发。它的参数如下：
参数	说明
run_date(datetime or str)	任务运行的日期或者时间
timezone(datetime.tzinfo or str)	指定时区
```
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

def my_job(text):
    print(text)

# 在2019年4月15日执行
scheduler.add_job(my_job, 'date', run_date=date(2019, 4, 15), args=['测试任务'])

scheduler.start()

###########################################################################################
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

def my_job(text):
    print(text)
    
# datetime类型（用于精确时间）
scheduler.add_job(my_job, 'date', run_date=datetime(2019, 4, 15, 17, 30, 5), args=['测试任务'])

scheduler.start()
```

注意：run_date参数可以是date类型、datetime类型或文本类型。
```
scheduler.add_job(my_job, 'date', run_date='2009-11-06 16:30:05', args=['测试任务'])
```

##3.2 interval 周期触发任务
固定时间间隔触发。interval 间隔调度，参数如下：

参数	说明
weeks(int)	间隔几周
days(int)	间隔几天
hours(int)	间隔几小时
minutes(int)	间隔几分钟
seconds(int)	间隔多少秒
start_date(datetime or str)	开始日期
end_date(datetime or str)	结束日期
timezone(datetime.tzinfo or   str)	时区
```
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def job_func():
     print("当前时间：", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

scheduler = BlockingScheduler()

# 每2小时触发
scheduler.add_job(job_func, 'interval', hours=2)

# 在 2019-04-15 17:00:00 ~ 2019-12-31 24:00:00 之间, 每隔两分钟执行一次 job_func 方法
scheduler .add_job(job_func, 'interval', minutes=2, start_date='2019-04-15 17:00:00' , end_date='2019-12-31 24:00:00')

scheduler.start()
```
jitter振动参数，给每次触发添加一个随机浮动秒数，一般适用于多服务器，避免同时运行造成服务拥堵。

每小时（上下浮动120秒区间内）运行`job_function`
```
scheduler.add_job(job_func, 'interval', hours=1, jitter=120)
```

##3.3 cron 触发器
在特定时间周期性地触发，和Linux crontab格式兼容。它是功能最强大的触发器。

cron 参数：



参数	说明
year(int or str)	年，4位数字
month(int or str)	月（范围1-12）
day(int or str)	日（范围1-31）
week(int or str)	周（范围1-53）
day_of_week(int or str)	周内第几天或者星期几（范围0-6或者mon,tue,wed,thu,fri,stat,sun）
hour(int or str)	时（0-23）
minute(int or str)	分（0-59）
second(int or str)	秒（0-59）
start_date(datetime or str)	最早开始日期（含）
end_date(datetime or str)	最晚结束日期（含）
timezone(datetime.tzinfo or   str)	指定时区

注意：month和day_of_week参数分别接受的是英语缩写jan– dec 和 mon – sun

使用 scheduled_job() 装饰器添加任务：
```
@scheduler.scheduled_job('cron', id='my_job_id', day='last sun')
def some_decorated_task():
    print("I am printed at 00:00:00 on the last Sunday of every month!")
```









 