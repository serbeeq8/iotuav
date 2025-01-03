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

# Define wind parameters for Case 5
wind_speed = 15.0  # m/s
wind_direction_deg = 70.0  # degrees
wind_direction_rad = math.radians(wind_direction_deg)
droplet_radius = 0.002  # m

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

# Fly through original waypoints
print("Flying through original waypoints...")
for wp in original_waypoints:
    client.moveToPositionAsync(wp[0], wp[1], wp[2], drone_speed).join()
    time.sleep(2)  # Pause for visualization

# Function to calculate Reynolds number
def reynolds_number(wind_speed, droplet_radius, rho_air, eta):
    return (2 * droplet_radius * wind_speed * rho_air) / eta

# Function to calculate drag coefficient
def drag_coefficient(reynolds):
    if reynolds < 0.5:
        return 24 / reynolds
    elif reynolds < 1000:
        return 24 / reynolds**0.6
    elif 2000 <= reynolds < 4000:  # Transitional flow
        return 24 * (1 / reynolds + 0.15 * reynolds**0.687)
    else:  # Turbulent flow
        return 0.44

# Function to calculate displacement using drag
def calculate_displacement_with_drag(wind_speed, wind_direction, droplet_radius, fall_time, density_fertilizer, rho_air, eta):
    reynolds = reynolds_number(wind_speed, droplet_radius, rho_air, eta)
    C_d = drag_coefficient(reynolds)
    A = math.pi * droplet_radius**2
    v_x = wind_speed
    x_displacement = 0
    dt = 0.001  # Small time step for precision
    droplet_mass = (4 / 3) * math.pi * droplet_radius**3 * density_fertilizer

    for _ in range(int(fall_time / dt)):
        F_d = 0.5 * rho_air * v_x**2 * C_d * A
        v_x -= (F_d / droplet_mass) * dt
        x_displacement += v_x * dt

    wind_direction_rad = math.radians(wind_direction)
    x_displacement_adjusted = x_displacement * math.cos(wind_direction_rad)
    y_displacement_adjusted = x_displacement * math.sin(wind_direction_rad)

    return x_displacement_adjusted, y_displacement_adjusted

# Air properties
eta = 1.81e-5  # Dynamic viscosity of air in pascal-seconds
rho_air = 1.225  # Density of air in kg/m^3
density_fertilizer = 1000  # Assumed as water
t_flight = flight_altitude / drone_speed  # Time of flight

# Calculate droplet displacement
x_displacement, y_displacement = calculate_displacement_with_drag(
    wind_speed, wind_direction_deg, droplet_radius, t_flight, density_fertilizer, rho_air, eta
)

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
