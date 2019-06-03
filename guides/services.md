# Services
This project uses systemctl to manage services. Our services include: 
- running the flask server (your app)
- running the [celery](celery.md) task runner.

### Install
- [ssh into and set up the raspberry pi](../README.md#raspberry-pi-installation-instructions)
- cd into alterspace
```
cd alter-space
```
- run the install script
```
./services/install
```

If something goes wrong, follow the instructions printed in the console.

- Check that the two services are running:
```
sudo systemctl status alterspace-celery.service
sudo systemctl status alterspace.service
```