# iotuav
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
using `venv`:
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
