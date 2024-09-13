import airsim
import time

# Initialising the AirSim client
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Take off
client.takeoffAsync().join()

# Define waypoints here it is a sqaure waypoint
waypoints = [
    airsim.Vector3r(30, 0, -30),
    airsim.Vector3r(30, 0, -30),
    airsim.Vector3r(0, 0, -30),
    airsim.Vector3r(0, 0, -30)
]

for i, waypoint in enumerate(waypoints):
    print(f"Moving to waypoint {i + 1}: {waypoint}")
    client.moveToPositionAsync(waypoint.x_val, waypoint.y_val, waypoint.z_val, 5).join()
    print(f"Reached waypoint {i + 1}: {waypoint}")
    time.sleep(5)  # Add a delay between each waypoint of 5 secs

# Land the iris drone
client.landAsync().join()


client.armDisarm(False) #disarm
client.enableApiControl(False) #disable api

print("Waypoint mission completed!")
