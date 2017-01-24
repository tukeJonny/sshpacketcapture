# Installation & Test
```
$ virtualenv --python="your python path" venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ cd src
(venv) $ python main.py --help
(venv) $ python main.py -u root -i 127.0.0.1
```

# Known Bugs
* http_parserがクエリパラメータを正しくとってこれていない模様？（１つしかクエリパラメータを取れない)
