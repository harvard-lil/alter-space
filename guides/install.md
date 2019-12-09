# Installation instructions

This project was tested on python 3.5
See [package.json](frontend/package.json) for JS requirements
and [requirements.txt](requirements.txt) for python requirements


### Install
```
pip install pyenv
pyenv install 3.5.4 
pyenv virtualenv 3.5.4 alterspace
pyenv activate alterspace
```

#### Install python dependencies
```
cp config/config.example.py config/config.py
pip install -r requirements.txt
```

#### Install JS dependencies
I have noticed that there are problems with newer versions of node.
To get around this, I ran `brew install nvm` (a node package manager)
and then `nvm install 8.11.1` 
In another bash window:
```
cd frontend
npm install
```


### In the first bash window, run flask server

```
cd ..
fab run
```
or, to run on a different port:
```
fab run:8000
```

### Tasks
We use Celery to handle all of our light-related tasks, since some tasks might take longer than others and we don't want that to clobber anything else we might want to be doing.
Therefore, we need to start the Celery service in a different terminal session: 
```
fab celery
```

In development, we need to serve both the flask app and vue frontend.  

### Vue/Static assets
To serve files:
```
cd frontend
npm run serve
```
This command runs a live reload server at from http://127.0.0.1:8080/

### Build files before deploying
Remember to build files before adding them to the source code:
```
$ cd frontend
$ npm run build
```

All built front-end files will be in [alter-space/dist](dist) folder.

Now you should be able to visit http://127.0.0.1:5000/ and see everything working as intended.

Note: some static assets live in the /public folder. On build, these get copied over to the /dist folder
instead of compiled using the webpack configuration.


### Working with SVGs
We use the lovely [vue-svgicon](https://github.com/MMF-FE/vue-svgicon#use-generated-icon) for dealing with svgs in Vue.
To use, place all svg assets into frontend/svg-icons.
Run the following command to compile (assets will be placed in frontend/src/components/icons):
```
$ cd ./frontend
$ npm run generate-icons
```

In your Vue component's script tag, import your icon

```python
  import './icons/your-icon';
```

In your vue component's template, place the svg
```html
<svgicon icon="your-icon" width="60" height="60" :original="true" class="btn-default" stroke="0"></svgicon>
```