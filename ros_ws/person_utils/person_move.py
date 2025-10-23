import argparse
import subprocess
import time
import re

def move(x, y, z, steps, rate):
    """Moves the person model 'my_person' from the current position to the specified one (x,y,z)."""
    x_start, y_start, z_start = get_person_position()

    dx = (x - x_start) / steps
    dy = (y - y_start) / steps
    dz = (z - z_start) / steps


    for i in range(steps):
        req = f'name: "my_person", position: {{x: {x_start + dx*(i+1)}, y: {y_start + dy*(i+1)}, z: {z_start + dz*(i+1)}}}'
        subprocess.run([
            "gz", "service", "-s", "/world/default/set_pose",
            "--reqtype", "gz.msgs.Pose",
            "--reptype", "gz.msgs.Boolean",
            "--req", req
        ])
        time.sleep(1.0 / rate)

def get_person_position():
    """Gets the person model 'my_person' current position"""
    result = subprocess.run(
        ["gz", "model", "-m", "my_person", "--pose"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    
    # Search for the pose using regex
    xyz_match = re.search(r"XYZ.*:\s*\[([^\]]+)\]", output)

    x, y, z = [float(val) for val in xyz_match.group(1).split()]
    
    return x, y, z


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move person in Gazebo")
    parser.add_argument("--x", type=float, default=0.0, help="X target")
    parser.add_argument("--y", type=float, default=0.0, help="Y target")
    parser.add_argument("--z", type=float, default=0.0, help="Z target")
    parser.add_argument("--steps", type=int, default=10, help="Number of steps")
    parser.add_argument("--rate", type=float, default=1.0, help="Hz rate")

    args = parser.parse_args()

    move(args.x, args.y, args.z, args.steps, args.rate)
