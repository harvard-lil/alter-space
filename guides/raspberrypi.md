# Raspberry PI Installation Instructions
- ssh into your pi: https://www.raspberrypi.org/documentation/remote-access/ssh/ (archived at https://perma.cc/RP4P-CYSR)
- set up raspberry pi wifi: https://raspberrypihq.com/how-to-connect-your-raspberry-pi-to-wifi/ (archived at https://perma.cc/W9XE-XFT7)
- set up git:
```
sudo apt install git
git clone https://github.com/harvard-lil/alter-space
cd alter-space
cp config/config.example.py config/config.py
pip3 install -r requirements.txt
```

- install redis
```
sudo apt install redis-server
```

- make sure redis is running
```
ps aux | grep redis
```
you should see something like:
```
$ redis      574  0.2  0.3  29692  3232 ?        Ssl  21:19   0:04 /usr/bin/redis-server 127.0.0.1:6379
```
- In your Raspberry Pi environment, you will be using the [built version](../dist/)of the frontend app. Therefore, you need to make sure that your [.env.production](frontend/.env.production) keys are correct.
Specifically, set `VUE_APP_SOUND_LOCAL_URL` to your Pi's IP address, 
make sure .env.production or .env.development point to the right IP and port.

- Follow instructions to set up [systemctl services](./services.md). This will allow the app to run on boot.
