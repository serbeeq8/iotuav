# Wind-Compensated Drone Navigation for Precision Weed Spraying

Welcome to the **Wind-Compensated Drone Navigation** project! This repository showcases a fascinating blend of physics, programming, and drone technology to achieve accurate and efficient weed spraying, even in challenging windy conditions.

## Overview

Imagine a drone flying over a field, tasked with spraying weeds. On a calm day, this might seem straightforward. But what happens when the wind starts blowing? The drone can easily drift off course, leading to inefficient spraying and missed targets. That's where our project comes in.

We have developed a solution that allows a drone to compensate for wind, maintaining its intended path and ensuring precise weed spraying. By leveraging fundamental physics principles, real-time adjustments, and simulation tools, we can guide the drone accurately to its targets, no matter the wind conditions.

## Main Aim

The primary goal of this project is to create a robust algorithm that enables drones to navigate accurately in windy environments. Our approach involves:

1. **Understanding Wind Dynamics**: Analyzing wind speed and direction to determine its impact on the drone's flight path.
2. **Applying Physics Principles**: Utilizing Newton's Laws of Motion and Stokes' Law to calculate the wind-induced forces acting on the drone.
3. **Real-Time Path Adjustment**: Continuously adjusting the drone's target coordinates to counteract wind drift.
4. **Simulation and Visualization**: Using Turtle graphics in the AirSim simulation to visualize the drone's path and its corrections in real-time.

## How It Works

1. **Wind Analysis**: We start by measuring the wind speed and direction. This helps us break down the wind into its horizontal components.
2. **Force Calculation**: Using Stokes' Law, we calculate the drag force the drone experiences as it flies through the wind.
3. **Path Adjustment**: We adjust the drone's flight path in real-time to counteract the wind's push, ensuring it reaches the intended target.
4. **Visualization**: We employ Turtle graphics to plot the original weed positions, the adjusted target points, and the drone's actual path, providing a clear visual representation of the drone's navigation.

## Project Highlights

- **Real-Time Adjustments**: Our algorithm continuously monitors and adjusts the drone's path, making it highly responsive to changing wind conditions.
- **Physics-Based Approach**: By grounding our solution in well-established physics principles, we ensure accuracy and reliability.
- **Engaging Visualization**: The use of Turtle graphics in the AirSim simulation offers an intuitive and engaging way to see the drone's path corrections in action.

## Conclusion

This project not only demonstrates the practical application of physics in drone navigation but also highlights the potential for drones to perform precise agricultural tasks, even in less-than-ideal conditions. We hope you find this project as exciting and informative as we do!

Feel free to explore the code, try out the simulation, and contribute to further enhancements. Together, we can make drone technology smarter and more resilient!

---

Thank you for checking out our project! If you have any questions or suggestions, please don't hesitate to reach out. Happy flying! 🌿🚁

---

**Note**: This project is intended for educational and research purposes. Always ensure to comply with local regulations and safety guidelines when operating drones.

---

# Project Setup and Execution Guide

This document provides a step-by-step guide to setting up and running the project. Follow these instructions to ensure a smooth workflow from initializing the environment to executing the wind compensation script.

## Prerequisites

- Visual Studio (VS)
- Windows Subsystem for Linux 2 (WSL2) with Ubuntu 22.04
- PX4 SITL
- AirSim
- ROS2 Humble
- Unreal Engine 4 (UE4)

## Steps

### 1. Open Visual Studio and Project File

1. **Launch Visual Studio.**
2. **Navigate to the project file named `myprojectfile2.sln`:**
    - Go to `File -> Open -> Project/Solution`.
    - Locate and select `myprojectfile2.sln`.
3. **Start the project** to open UE4.

### 2. Navigate to the iort Folder and Activate the Environment

1. **Open File Explorer** and navigate to `This PC`.
2. **Open the pinned `iort` folder** in the recent bar.
3. **Activate the Python environment** by opening a terminal in this folder and running:
    ```bash
    source path/to/your/venv/bin/activate
    ```

### 3. Open PX4 SITL

1. **Open File Explorer** and navigate to `This PC`.
2. **Open the pinned `PX4 SITL` folder** in the recent bar.
3. **Start WSL2** by opening a WSL terminal.

### 4. Start WSL2 and Make PX4 SITL

1. **Navigate to the PX4 directory** in the WSL terminal:
    ```bash
    cd /path/to/PX4-Autopilot
    ```
2. **Make the PX4 SITL**:
    ```bash
    make px4_sitl_default none
    ```

### 5. Run the Wind Compensation Script

1. **In the WSL terminal, navigate to the wind compensation script in the `iort` folder**:
    ```bash
    cd /mnt/c/path/to/iort
    ```
2. **Run the script**:
    ```bash
    python case3_correction.py
    ```
    Alternatively, **use the up arrow key** in the terminal to quickly access the recently ran script command and press `Enter` to execute it.

### 6. Monitor and Control

1. Use the keyboard arrow keys to navigate the drone in the simulation.
2. Monitor the output in the terminal for status updates or errors.
3. Verify the drone’s movement and wind compensation through the plotted path and logged positions.

### 7. Shutdown

1. Shut down the PX4 SITL:
    ```bash
    ctrl + C
    ```
2. Exit the UE4 simulation.

By following these steps, you will be able to set up and execute the project effectively. Address any issues that arise during each step promptly to ensure a smooth operation.