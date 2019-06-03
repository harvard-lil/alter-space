# Alterspace

Alterspace is a new kind of reading room: a simple set of controls lets patrons decide on the color and behavior of lights and sounds in the space, adapting conditions for brainstorming, meditation, or quiet study. 


![Photo by Hannah Schoenbaum](photo.png)
Photo by Hannah Schoenbaum


More information about the project is available here: https://alterspace.github.io/
and here: https://lil.law.harvard.edu/projects/alterspace/

This project is a collaboration between Harvard's [Library Innovation Lab](https://lil.law.harvard.edu) and [metaLAB](https://metalab.github.io).

### Before you start, see 
- [List of tools necessary](guides/tools.md)
- [Sound guide](guides/sounds.md)
- [Light guide](guides/lights.md)


### Table of contents:
- [Frameworks used](#frameworks)
- [Project structure](#project-structure)
- [Code installation instructions for OS](guides/install.md)
- [Code installation instructions for raspberry pis](guides/raspberrypi.md)

### Frameworks
This project is built using 
- [vue.js](http://vuejs.org/) on the frontend
- [flask](http://flask.pocoo.org/) on the backend   

### Project structure
- [backend](./backend) contains the server and celery. The main entry point is [app.py](backend/app.py)
- [frontend](./frontend) contains most of our frontend files. These include our [Vue.js app](frontend/main.js) and our [assets](frontend/src/assets).
- styles live in scss format in [assets/css](frontend/src/assets/css)
- [guides](guides) are some guides you might find useful!
- [dist](dist) are the compiled files. Files go there when you [build files](guides/install.md#build-files-before-deploying) with `npm run build` 
