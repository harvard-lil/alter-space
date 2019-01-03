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

Install frontend
```
$ fab npm_install 
```

### Run

```
$ fab run
```
or, to run on a different port:
```
$ fab run:8000
```
In development, we need to serve both the flask app and vue frontend.  

### Vue/Static assets
To serve files:
```
$ fab npm 
```
This command cds into the /frontend dir and runs `npm run build`, which causes the javascript to be loaded live from http://127.0.0.1:8080/ and recompiled on save.


Remember to build files before adding them to the source code:
```
$ fab build
```
Some static assets live in the /public folder. On build, these get copied over to the /dist folder
instead of compiled using the webpack configuration.

