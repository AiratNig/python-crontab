
coverage3 run --source crontab,cronlog setup.py test &> /dev/null
coverage2 run -a --source crontab,cronlog setup.py test &> /dev/null
coverage3 report -m

