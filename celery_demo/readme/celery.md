#For a complete listing of the command-line options available, use the help command:
celery --help

# Starting the worker
celery -A django_tutorials worker -l INFO

# 启动
celery -A django_tutorials worker -c 5 -l info
# In the background 后台启动
celery multi start w1 -A django_tutorials -l INFO
# 重启
celery  multi restart w1 -A django_tutorials -l INFO
# 停止
celery multi stop w1 -A django_tutorials -l INFO

# The stop command is asynchronous so it won’t wait for the worker to shutdown.
# You’ll probably want to use the stopwait command instead,
# which ensures that all currently executing tasks are completed before exiting:
celery multi stopwait w1 -A proj -l INFO

# 启动flower
celery -A django_tutorials flower  --address=127.0.0.1 --port=5673
