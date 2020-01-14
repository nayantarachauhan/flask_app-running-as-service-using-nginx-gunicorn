######flask_app-running-as-service-using-nginx-gunicorn
#### adda_admin just contains the view of our tables in database(apis are not there)
#### adda_api contains all the apis

The first directory named apps contains my two virtual enviornment named adda-admin and adda_api
adda_api(venv)- contains the main project folder named adda_api,wsgi.py,config.py and requirements.txt as a main thing
adda_admin(venv)- contains the main project folder named adda_admin,wsgi.py,config.py and requirements.txt as a main thing


here we have used gunicorn and nginx to run flask app as a service
for adda_api we created a adda_api.service (daemon) in home/etc/systemd/system/adda_api.service
for adda_admin we created a adda_admin.service (daemon) in home/etc/systemd/system/adda_admin.service

adda_api.service contains the code :

[Unit]
Description=Gunicorn instance to serve adda_api
After=network.target

[Service]
User=root
#WorkingDirectory=/root/home/nayantara/apps/adda_api
#Environment="PATH=/home/nayantara/apps/adda_api/bin"
ExecStart=/home/nayantara/apps/adda_api/bin/gunicorn --workers 2 --bind unix:adda_api.sock --chdir /home/nayantara/apps/adda_api wsgi:app

[Install]
WantedBy=multi-user.target



adda_admin.service contains the code :

[Unit]
Description=Gunicorn instance to serve adda_api
After=network.target

[Service]
User=root
#WorkingDirectory=/root/home/nayantara/apps/adda_admin
#Environment="PATH=/home/nayantara/apps/adda_admin/bin"
ExecStart=/home/nayantara/apps/adda_admin/bin/gunicorn --workers 2 --bind unix:adda_admin.sock --chdir /home/nayantara/apps/adda_admin wsgi:app

[Install]
WantedBy=multi-user.target


(here we are confuguring nginx to listen request for two different flask applications(adda_api and adda_admin))
nginx file configured in default file which is located in home/etc/nginx/sites-available/default
to write inside this ,command - nano default(type this after being in the folder where the default is located)

code inside default file : 

server {
        listen 5001;
        listen [::]:5001;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                #try_files $uri $uri/ =404;
                include proxy_params;
                proxy_pass http://unix:/home/nayantara/apps/adda_api/adda_api.sock;
        }
}

server {
        listen 5002;
        listen [::]:5002;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                #try_files $uri $uri/ =404;
                include proxy_params;
                proxy_pass http://unix:/home/nayantara/apps/adda_admin/adda_admin.sock;
        }
}




#######################important command to keep in mind

1. after configuring the service file always reload the daemon and then restart the service then check the status of service file

systemctl daemon-reload
systemctl restart adda_admin.service 
systemctl status adda_admin.service 


2. for nginx:

service nginx restart
netstat -tulpn | grep LISTEN (it will show you all the port on which it is listening)
service nginx status


IMPORTANT LINKS:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

https://hackersandslackers.com/flask-application-factory/













