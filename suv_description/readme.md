# 环境准备

安装一些功能包:
```
sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui
sudo apt install ros-$ROS_DISTRO-ros-control
sudo apt install ros-$ROS_DISTRO-ros-controllers
sudo apt install ros-$ROS_DISTRO-gmapping
sudo apt install ros-$ROS_DISTRO-ackermann-msgs
sudo apt install ros-$ROS_DISTRO-navigation
sudo apt install ros-$ROS_DISTRO-teb-local-planner
```
确保自己的python能够import tkinter

# 命令

- 在rviz中观察模型：`roslaunch suv_description view_xacro_rviz.launch`

- gazebo中观察模型: `roslaunch suv_description view_xacro_gazebo.launch`



# 文件介绍

- `/config/keyboard_teleop.yaml: `  键盘控制节点的速度与转向角
- `/launch/controller.launch:`   控制小车关节运动，将ackermann消息转化为twist，发布里程计信息
- `/scripts/intertia_matrix.py:`  计算urdf惯性矩阵时用到
- `/scripts/servo_commands.py:`  订阅ackermann话题并发布到关节
- `/scripts/keyboard_teleop.py:`  键盘控制发布ackermann话题
- `/scripts/ackermann_to_twist.py:`  将ackermann消息转化为twist
- `/scripts/gazebo_odometry.py:`  由gazebo获得odom信息



# 参考

[TIANBOT的博客(阿克曼结构移动机器人的gazebo仿真)](https://blog.csdn.net/tianbot/category_11774891.html)

