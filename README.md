# yolo-follower



## Description

* **docker\_ws** folder: contains all the necessary docker files and scripts to build docker images.
* **ros\_ws** folder: this folder will contain all the packages that we'll create. It is mapped inside our container with docker volumes. 
* **chown\_me.sh**: bash script to change the owner of files from root to user (just in case docker root user messes around with our files :) ).
* **run.sh**: bash script to run our container with all the capabilities and volumes that we need.
* **exec.sh**: bash script to open a shell to an already running container.



After building the image and the packages and sourcing the environment, the simulation can be run using the launch file, through the command: **ros2 launch doom\_nodes doom**





