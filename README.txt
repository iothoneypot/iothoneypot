For the Raspbian image provided.

1) Change the ip addresses in index.html, and settings under /var/www/html and /root/mmal respectively.

2) Settings and http.py should be in the same location.

3) Run the http.py under folder /root/mmal with the argument 800 for running it on port 800 by typing "./http.py 800".

4) Stop the nginx service by typing "fuser -k 80/tcp" when booted. (Due to some error setting up nginx)

5) Run the nginx service again by typing "service nginx start".

6) After connecting the pi camera to the pi, run "./motion -n -c motion-mmalcam.conf" under /root/mmal.

7) The honeypot should be up by now.