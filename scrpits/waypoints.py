import airsim
import time

# Initialize AirSim client
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Take off
client.takeoffAsync().join()

# Define waypoints
waypoints = [
    airsim.Vector3r(30, 0, -30),
    airsim.Vector3r(30, 0, -30),
    airsim.Vector3r(0, 30, -30),
    airsim.Vector3r(0, 0, -30)
]

for i, waypoint in enumerate(waypoints):
    print(f"Moving to waypoint {i + 1}: {waypoint}")
    client.moveToPositionAsync(waypoint.x_val, waypoint.y_val, waypoint.z_val, 5).join()
    print(f"Reached waypoint {i + 1}: {waypoint}")
    time.sleep(1)  # Add a delay between each waypoint

# Land
client.landAsync().join()

# Disarm and disable API control
client.armDisarm(False)
client.enableApiControl(False)

print("Waypoint mission completed!")
