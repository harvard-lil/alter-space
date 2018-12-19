tested on python 3.5

### Install
```
$ pip install pyenv
$ pyenv install 3.5.4 
$ pyenv virtualenv 3.5.4 alterspace
$ pyenv activate alterspace
```

```
$ cp config/config.example.py config/config.py
$ pip install -r requirements.txt
```

### Run

```
$ fab run
```
or, to run on a different port:
```
$ fab run:8000
```

### Vue/static assets
serve files:
```
$ fab npm
```
Build files:
```
$ fab build
```