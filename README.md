# yolo-follower



## FILESYSTEM:

* **docker\_ws** folder: contains all the necessary docker files and scripts to build docker images.
* **ros\_ws** folder: this folder will contain all the project packages. It is mapped inside the docker container using volumes strategy.
* **chown\_me.sh**: bash script to change the owner of files from root to user.
* **run.sh**: bash script to run our container with all the capabilities and volumes that we need.
* **exec.sh**: bash script to open a shell to an already running container.



## HOW TO RUN THE PROJECT:

* First of all, build the docker image by moving in the docker\_ws folder and launching the '**./build\_doom.sh**' script
* After the image building is completed, launch the docker engine by running docker desktop application
* Create the container using '**./run.sh**' in the doom\_ws folder
* Build the packages by running '**colcon build**' bash command in the ros\_ws folder
* Source the environment with '**source install/setup.bash**'
* Run the command '**export TURTLEBOT3\_MODEL=waffle**' to specify to the nodes which kind of robot to be used
* Launch the simulation using '**ros2 launch doom\_nodes doom\_project.launch.py**'
* After the launch is complete, enter the same container from another terminal using '**./exec.sh**' in the doom\_ws folder and source using '**source install/setup.bash**'
* Use this second container to control the person model that the robot will follow. In particular, use the command '**python3 person\_utils/person\_spawn.py --x <> --y <>**' to spawn the model. Then the command '**python3 person\_utils/person\_move.py --x <> --y <>**' can be used to move the person model around, allowing to check the robot dynamic target-following behaviour.
* An example path, designed to keep the person within the robot's camera field of view, can be executed using the following sequence of commands:



&nbsp;	- python3 person\_utils/person\_spawn.py --x 0.5 --y -0.4

&nbsp;	- python3 person\_utils/person\_move.py --x 0.5 --y 0.0

&nbsp;	- python3 person\_utils/person\_move.py --x 1.2 --y 0.5	

&nbsp;	- python3 person\_utils/person\_move.py --x 0.5 --y 1.5

&nbsp;	- python3 person\_utils/person\_move.py --x 0.0 --y 2.0

 	- python3 person\_utils/person\_move.py --x -1.0 --y 2.0

 	- python3 person\_utils/person\_move.py --x -1.8 --y 1.5

 	- python3 person\_utils/person\_move.py --x -1.5 --y 0.0

&nbsp;	





