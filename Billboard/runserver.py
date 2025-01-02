import subprocess
import os
import platform

def run_commands_unix():
    # Запуск сервера Django в новом терминале
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'python manage.py runserver; exec bash'])

    # Запуск Celery worker в новом терминале
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'celery -A Billboard worker --loglevel=info; exec bash'])

    # Запуск Celery Beat в новом терминале
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'celery -A Billboard beat --loglevel=info; exec bash'])

def run_commands_windows():
    # Запуск сервера Django в новом терминале
    subprocess.Popen(['start', 'cmd', '/k', 'python manage.py runserver'], shell=True)

    # Запуск Celery worker в новом терминале
    subprocess.Popen(['start', 'cmd', '/k', 'celery -A Billboard worker -l INFO --pool=solo'], shell=True)

    # Запуск Celery Beat в новом терминале
    subprocess.Popen(['start', 'cmd', '/k', 'celery -A Billboard beat --loglevel=info'], shell=True)

def run_commands():
    if platform.system() == 'Windows':
        run_commands_windows()
    else:
        run_commands_unix()

if __name__ == '__main__':
    run_commands()
