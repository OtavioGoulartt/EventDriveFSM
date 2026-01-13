# Utils

---

This repository contains all files and folders not designed for a proper function or simply not organized yet. They are here for probable future use.

# ROS Interfaces

> [!WARNING]
> The interfaces which are presented here are not organized and therefore are not related. This implies for the user to add the description to a new package or folder added in this repository.

## Topics (Example)

- self.track_sub = Subscriber(self,TrackStamped,"track")
- self.pointcloud_pub = Publisher(self,PointCloud2,"pointcloud")

> Topics and messages used in Utils package.

---

| Module | Direction | Topic         | Message Type              | Notes             |
| ------ | --------- | ------------- | ------------------------- | ----------------- |
| Utils  | Sub       | `/track`      | `nav_msgs/TrackStamped`   | Track input       |
| Utils  | Pub       | `/pointcloud` | `sensor_msgs/PointCloud2` | Pointcloud output |

# Dependencies

Core dependencies (minimum):

- ROS 2 Humble (or newer)
- `rclcpp` / `rclpy`
- `nav_msgs`, `sensor_msgs`, `fs_msgs`
- `ament_cmake`
- `colcon` (build system)

# Folders descriptions

## Camera Utils

This **folder** is designed for storing **camera-related codes**. Now, there are two Python files developed also for calculations involving camera errors.

## Pointcloud RGB Launcher

This **launcher** is designed for launching the pointcloud

## Rosbag Converter

This **"package"** is designed for converting **track** rosbags to **CSV** files.
