import airsim
import numpy as np
import math
import time

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

# Enable API control
client.enableApiControl(True)
client.armDisarm(True)

# Take off the drone
client.takeoffAsync().join()

# Define wind parameters for Case 1
wind_speed = 10.0  # m/s
wind_direction_deg = 30.0  # degrees
wind_direction_rad = math.radians(wind_direction_deg)
droplet_radius = 0.002  # m (not directly simulated, used for analysis)

# Compute wind velocity components
wind_x = wind_speed * math.cos(wind_direction_rad)
wind_y = wind_speed * math.sin(wind_direction_rad)
wind_z = 0.0  # Assuming horizontal wind

# Set the wind in the AirSim environment
wind = airsim.Vector3r(wind_x, wind_y, wind_z)
client.simSetWind(wind)

# Define flight parameters
drone_speed = 5.0  # m/s
flight_altitude = 20.0  # meters

# Define waypoints
original_waypoints = [
    (30, 0, -flight_altitude),
    (30, 30, -flight_altitude),
    (0, 30, -flight_altitude),
    (0, 0, -flight_altitude),
]

# Fly through waypoints
print("Flying through original waypoints...")
for wp in original_waypoints:
    client.moveToPositionAsync(wp[0], wp[1], wp[2], drone_speed).join()
    time.sleep(2)  # Pause for visualization

# Function to calculate droplet displacement using Stokes' law (for laminar flow)
def calculate_displacement_stokes(V, t, radius, eta, mass):
    return (6 * np.pi * eta * radius * V * t) / mass

# Air properties
eta = 1.81e-5  # Dynamic viscosity of air in pascal-seconds
rho_air = 1.225  # Density of air in kg/m^3
density_fertilizer = 1000  # Assumed as water
t_flight = flight_altitude / drone_speed  # Time of flight

# Calculate droplet displacement
volume = (4 / 3) * math.pi * (droplet_radius ** 3)  # Volume in m^3
mass = density_fertilizer * volume  # Mass in kg

# Wind velocity components
Vx = wind_x
Vy = wind_y

# Calculate displacements
x_displacement = calculate_displacement_stokes(Vx, t_flight, droplet_radius, eta, mass)
y_displacement = calculate_displacement_stokes(Vy, t_flight, droplet_radius, eta, mass)

# Adjust waypoints based on displacement
adjusted_waypoints = [
    (wp[0] - x_displacement, wp[1] - y_displacement, wp[2])
    for wp in original_waypoints
]

print(f"Displacement X: {x_displacement:.2f} m, Displacement Y: {y_displacement:.2f} m")
print("Adjusted waypoints:", adjusted_waypoints)

# Fly through adjusted waypoints
print("Flying through adjusted waypoints...")
for wp in adjusted_waypoints:
    client.moveToPositionAsync(wp[0], wp[1], wp[2], drone_speed).join()
    time.sleep(2)  # Pause for visualization

# Land the drone
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)

print("Simulation complete.")
