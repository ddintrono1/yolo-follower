import argparse
import subprocess

def spawn(x, y, z):
    """Spawns the person model 'my_person' at the given position (x,y)."""
    req = (
        f'sdf_filename: "/root/ros_workspace/person_utils/person.sdf",'
        f'name: "my_person",'
        f'pose: {{ position: {{ x: {x}, y: {y}, z: {z} }} }}'
    )
    subprocess.run([
        "gz", "service", "-s", "/world/default/create",
        "--reqtype", "gz.msgs.EntityFactory",
        "--reptype", "gz.msgs.Boolean",
        "--req", req
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spawn person in Gazebo")
    parser.add_argument("--x", type=float, default=0.0, help="X position")
    parser.add_argument("--y", type=float, default=0.0, help="Y position")
    parser.add_argument("--z", type=float, default=0.0, help="Z position")

    args = parser.parse_args()

    spawn(args.x, args.y, args.z)