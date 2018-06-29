Customized animation of satellite images over the internet
===========================================================

This usage of this project is to develop an efficient mechanism to view an animation of time series of satellite photos as per user's requirement. User can choose the start and end time / date and the required interval and is able to visualize its animation over the internet with different speeds.

INSTALLATION:
-------------------

Server side requires Linux( Ubuntu) and postgresql database server. Postgresql server can be on same computer or on another computer. Ubuntu is assumed for these install instructions.
Project is developed in python and uses python's 'virtualenv' module for installation.

1. Checkout the project code https://bitbucket.org/AkshataJ96/sih2018 in a folder (we use name sih2018 as foldername)
2. Change into source directory and run shell script(prepare.sh) to install the required modules.
cd sih2018/source
./prepare.sh

SETUP:
------
 
Assuming the virtual environment is activated and all installations are complete,

1. This project requires the user to update the new images in directory named as images in source directory.
cd sih2018/source/server/webapp/GrazerISR4
mkdir images
	
2. Run the following command to watch the "images" directory continously for new images. Ideally you should put this command as 'service' or run it from 'cron job'
python3 manage.py getImage

3. From a different shell prompt, Run Django migration command to create the DB tables and create an admin user.
python3 manage.py migrate
python3 manage.py createsuperuser
	
4. Start the django server. Following command is for running django server in 'development' mode. In production it advisable to install the django in Gunicorn or some other WSGI compliant server

python3 manage.py runserver
   Enter the credentials at http://localhost:8000/GrazerFeed/Login and proceed to choose the options and view the animation.

5. To create more users,
	Enter the Django admin with your user credentials at http://localhost:8000/admin/
	
