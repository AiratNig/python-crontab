
coverage3 run --source crontab,crontabs,cronlog setup.py test &> /dev/null
coverage2 run -a --source crontab,crontabs,cronlog setup.py test &> /dev/null
coverage3 report -m

