import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Define constants
eta = 1.81e-5  # Dynamic viscosity of air in pascal-seconds
g = 9.81  # Acceleration due to gravity in m/s^2
drone_speed = 5  # Drone speed in m/s
height = 20  # Height from which the drone is flying in meters
t_flight = height / drone_speed  # Flight time
rho_air = 1.225  # Density of air in kg/m^3
density_fertilizer = 1000  # Uniform density for the fertilizer solution in kg/m^3 (assumed as water)

# Wind cases (laminar and turbulent)
cases = [
    {'Case': 1, 'Wind Speed': 10.0, 'Wind Direction': 30, 'Droplet Radius': 0.002},
    {'Case': 2, 'Wind Speed': 12.0, 'Wind Direction': 40, 'Droplet Radius': 0.002},
    {'Case': 3, 'Wind Speed': 13.0, 'Wind Direction': 50, 'Droplet Radius': 0.002},
    {'Case': 4, 'Wind Speed': 14.0, 'Wind Direction': 60, 'Droplet Radius': 0.002},
    {'Case': 5, 'Wind Speed': 15.0, 'Wind Direction': 70, 'Droplet Radius': 0.002},
    {'Case': 6, 'Wind Speed': 20.0, 'Wind Direction': 80, 'Droplet Radius': 0.003},
]

# Original waypoints
original_waypoints = np.array([
    [30, 0, -20],
    [30, 30, -20],
    [0, 30, -20],
    [0, 0, -20]
])

def calculate_displacement_stokes(V, t, radius, eta, mass):
    """Calculate displacement using Stokes' law (for laminar flow)."""
    return (6 * np.pi * eta * radius * V * t) / mass

def determine_flow_type(wind_speed, droplet_radius, rho_air, eta):
    """Determine flow type based on Reynolds number."""
    Re = (rho_air * wind_speed * droplet_radius) / eta
    if Re < 2000:
        return 'Laminar', Re
    elif 2000 <= Re < 4000:
        return 'Transitional', Re
    else:
        return 'Turbulent', Re

def reynolds_number(wind_speed, droplet_radius):
    return (2 * droplet_radius * wind_speed * rho_air) / eta

def drag_coefficient(reynolds):
    if reynolds < 0.5:
        return 24 / reynolds
    elif reynolds < 1000:
        return 24 / reynolds**0.6
    else:
        return 0.44

def calculate_displacement_with_drag(wind_speed, wind_direction, droplet_radius, fall_time, density_fertilizer):
    """Calculate displacement for turbulent flow."""
    reynolds = reynolds_number(wind_speed, droplet_radius)
    C_d = drag_coefficient(reynolds)
    A = math.pi * droplet_radius**2
    v_x = wind_speed
    x_displacement = 0
    dt = 0.0001  # Smaller time step to avoid overflow
    droplet_mass = (4/3) * math.pi * droplet_radius**3 * density_fertilizer

    for _ in range(int(fall_time / dt)):
        F_d = 0.5 * rho_air * v_x**2 * C_d * A
        v_x -= (F_d / droplet_mass) * dt
        x_displacement += v_x * dt

    wind_direction_rad = math.radians(wind_direction)
    x_displacement_adjusted = x_displacement * math.cos(wind_direction_rad)
    y_displacement_adjusted = x_displacement * math.sin(wind_direction_rad)

    return x_displacement_adjusted, y_displacement_adjusted

def calculate_average_displacement(wind_speed, wind_direction, droplet_radius, fall_time, density_fertilizer, eta, mass):
    """Calculate the average displacement for Transitional flow."""
    # Displacement using Stokes' law (Laminar)
    Vx = wind_speed * np.cos(np.radians(wind_direction))
    Vy = wind_speed * np.sin(np.radians(wind_direction))
    x_displacement_stokes = calculate_displacement_stokes(Vx, fall_time, droplet_radius, eta, mass)
    y_displacement_stokes = calculate_displacement_stokes(Vy, fall_time, droplet_radius, eta, mass)

    # Displacement using Drag force (Turbulent)
    reynolds = reynolds_number(wind_speed, droplet_radius)
    C_d = drag_coefficient(reynolds)
    A = math.pi * droplet_radius**2
    v_x = wind_speed
    x_displacement_drag = 0
    y_displacement_drag = 0
    dt = 0.0001  # Smaller time step to avoid overflow
    droplet_mass = (4/3) * math.pi * droplet_radius**3 * density_fertilizer

    for _ in range(int(fall_time / dt)):
        F_d = 0.5 * rho_air * v_x**2 * C_d * A
        v_x -= (F_d / droplet_mass) * dt
        x_displacement_drag += v_x * dt
        y_displacement_drag += v_x * dt  # Assuming same drag effect on Y direction

    # Average displacement
    x_displacement_avg = (x_displacement_stokes + x_displacement_drag) / 2
    y_displacement_avg = (y_displacement_stokes + y_displacement_drag) / 2

    return x_displacement_avg, y_displacement_avg

results = []

for case in cases:
    wind_speed = case['Wind Speed']
    wind_direction_deg = case['Wind Direction']
    droplet_radius = case['Droplet Radius']

    flow_type, reynolds_number_value = determine_flow_type(wind_speed, droplet_radius, rho_air, eta)
    reynolds_number_rounded = round(reynolds_number_value, 2)

    volume = (4/3) * np.pi * (droplet_radius**3)  # Volume of the droplet in cubic meters
    mass = density_fertilizer * volume  # Mass of the droplet in kg
    A = np.pi * droplet_radius**2  # Cross-sectional area of the droplet

    wind_direction_rad = np.radians(wind_direction_deg)
    Vx = wind_speed * np.cos(wind_direction_rad)
    Vy = wind_speed * np.sin(wind_direction_rad)

    if flow_type == 'Laminar':
        x_displacement = calculate_displacement_stokes(Vx, t_flight, droplet_radius, eta, mass)
        y_displacement = calculate_displacement_stokes(Vy, t_flight, droplet_radius, eta, mass)
    elif flow_type == 'Turbulent':
        x_displacement, y_displacement = calculate_displacement_with_drag(wind_speed, wind_direction_deg, droplet_radius, t_flight, density_fertilizer)
    else:  # Transitional flow (2000 < Re < 4000)
        x_displacement, y_displacement = calculate_average_displacement(wind_speed, wind_direction_deg, droplet_radius, t_flight, density_fertilizer, eta, mass)

    adjusted_waypoints = [(x - x_displacement, y - y_displacement, z) for x, y, z in original_waypoints]
    adjusted_waypoints_rounded = [(round(x, 2), round(y, 2), round(z, 2)) for x, y, z in adjusted_waypoints]

    results.append({
        'Case': case['Case'],
        'Wind Speed (m/s)': wind_speed,
        'Wind Direction (degrees)': round(wind_direction_deg, 2),
        'Droplet Radius (m)': droplet_radius,
        'Reynolds Number': reynolds_number_rounded,
        'Flow Type': flow_type,
        'Original Waypoint': original_waypoints.tolist(),
        'Adjusted Waypoint': adjusted_waypoints_rounded
    })

    original_x, original_y, _ = zip(*original_waypoints)
    adjusted_x, adjusted_y, _ = zip(*adjusted_waypoints_rounded)

    plt.figure(figsize=(6, 6))
    plt.plot(list(original_x) + [original_x[0]], list(original_y) + [original_y[0]], 'bo-', label='Original Path')
    plt.plot(list(adjusted_x) + [adjusted_x[0]], list(adjusted_y) + [adjusted_y[0]], 'ro-', label='Adjusted Path')
    plt.xlabel('X Coordinate (m)')
    plt.ylabel('Y Coordinate (m)')
    plt.title(f'Original vs. Adjusted Path for Case {case["Case"]}')
    plt.legend()
    plt.grid(True)
    plt.show()

results_df = pd.DataFrame(results)
results_df = results_df[['Case', 'Wind Speed (m/s)', 'Wind Direction (degrees)', 'Droplet Radius (m)', 'Reynolds Number', 'Flow Type', 'Original Waypoint', 'Adjusted Waypoint']]
print(results_df)
# Create a DataFrame with the results
results_df = pd.DataFrame(results)
results_df = results_df[['Case', 'Wind Speed (m/s)', 'Wind Direction (degrees)', 'Droplet Radius (m)', 'Reynolds Number', 'Flow Type', 'Original Waypoint', 'Adjusted Waypoint']]

# Set pandas options to display the full content of the waypoint columns
pd.set_option('display.max_colwidth', None)

# Print the full results table
print(results_df)