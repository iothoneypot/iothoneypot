# sp2015fypgroup63iothoneypot
IoT HTTP Webcam Honeypot

ABOUT
-----

This is the Python web application honeypot made by the FYP Group 63.

General approach:

- 3 way integration between the webserver, nginx, the python script framework, and the motion ip camera module
- Using nginx, the team set up a webpage that looks like an authentic ip camera control panel page.
- The script logs any actions done on the webpage and to the protocol. It also captures any file uploads made to the server in a non-executable, non-readable folder.
- The motion ip camera module is used to show real-time footage from the connected camera, to provide additional bait.
- Nginx runs on port 80, to simulate a normal webserver. It uses iframe to livestream the motion ip camera footage, which runs on port 888. When a attacker/user tries to authenticate themselves to gain access to the camera controls, they will be redirected to port 8000, which is where the python script runs.

INSTALL
-------

Installation instructions can be found in the README.txt that's also in the repository.