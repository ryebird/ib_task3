#!/bin/bash

mkdir -p /home/linuxuser/linux_practice
chown -R linuxuser:linuxuser /home/linuxuser

cp /app/linux_tasks /home/linuxuser/tasks
chown linuxuser:linuxuser /home/linuxuser/tasks

echo "echo 'Добро пожаловать в тренировочный Linux-терминал!'" >> /home/linuxuser/.bashrc
echo "echo ''" >> /home/linuxuser/.bashrc
echo "echo 'Вам предстоит выполнить несколько базовых заданий по работе с Linux.'" >> /home/linuxuser/.bashrc
echo "echo 'В каждом шаге будет подсказка, какую команду нужно использовать.'" >> /home/linuxuser/.bashrc
echo "echo ''" >> /home/linuxuser/.bashrc
echo "echo 'Чтобы начать выполнение заданий, введите команду:'" >> /home/linuxuser/.bashrc
echo "echo ''" >> /home/linuxuser/.bashrc
echo "echo '   ./tasks'" >> /home/linuxuser/.bashrc

export HOME=/home/linuxuser
export USER=linuxuser
export PS1='[linuxuser@training]$ '
cd /home/linuxuser
exec ttyd -p 7681 -i 0.0.0.0 --writable bash
