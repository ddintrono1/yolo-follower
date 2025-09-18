xhost +
docker run -it --rm --ipc host --privileged \
    --gpus all \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.Xauthority:/root/.Xauthority \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=$XAUTHORITY \
    -p 8080:8080 \
    -v ./ros_ws/:/root/ros_workspace \
    --name doom_container \
    ros:doom bash
