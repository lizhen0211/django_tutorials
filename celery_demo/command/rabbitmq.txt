#查看服务状态
systemctl status rabbitmq-server
#停止服务
systemctl stop rabbitmq-server
#启动服务
systemctl start rabbitmq-server
#开机禁止启动
systemctl disable rabbitmq-server
#开机启动
systemctl enable rabbitmq-server
#rabbitmq 控制台访问地址
http://localhost:15672/#/

# https://www.rabbitmq.com/access-control.html
# Adding a User
rabbitmqctl add_user "rabbit"

#
rabbitmqctl set_user_tags rabbit administrator

#https://www.rabbitmq.com/vhosts.html
rabbitmqctl add_vhost /celery_sample

#https://www.rabbitmq.com/access-control.html
rabbitmqctl set_permissions -p /celery_sample 'rabbit' '.*' '.*' '.*'

#
sudo rabbitmqctl add_vhost /django_tutorials
sudo rabbitmqctl set_permissions -p /django_tutorials rabbit '.*' '.*' '.*'
sudo rabbitmqctl set_policy -p /django_tutorials ha-all "^" '{"ha-mode":"all"}'