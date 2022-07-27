[TOC]

# 参考：

> 文章仅为个人搭建urdf模型时的笔记，可能重点不突出，有的地方也不详细

请配合[TIANBOT的博客(阿克曼结构移动机器人的gazebo仿真)](https://blog.csdn.net/tianbot/category_11774891.html)一起阅读，能极大加快构建仿真环境的效率

# 一、urdf模型

## 1.urdf 模型搭建

### 1.1 link标签

[wiki](http://wiki.ros.org/urdf/XML/link)：查看哪些标签是必须的

```xml
<link name="my_link">
	<!--惯性相关-->
    <inertial> 
        <!--位置-->
   		<origin xyz="0 0 0.5" rpy="0 0 0"/>
        <!--重量 kg-->
        <mass value="1"/>
		<!--惯性矩阵相关-->
        <inertia ixx="100"  ixy="0"  ixz="0" iyy="100" iyz="0" izz="100" />
	</inertial>

    <!--可视化相关-->
	<visual>
 		<origin xyz="0 0 0" rpy="0 0 0" />
 		<!--几何形状 m-->
        <geometry>
			<box size="1 1 1" />
		</geometry>
		<!--材质-->
        <material name="Cyan">
 			<color rgba="0 1.0 1.0 1.0"/>
		</material>
	</visual>

    <!--碰撞相关-->
	<collision>
		<origin  xyz="0 0 0" rpy="0 0 0"/>
		<geometry>
  			<cylinder radius="1" length="0.5"/>
 		</geometry>
	</collision>
</link>
```

![选区_001](/home/speike/图片/选区_001.png)

### 1.2 joint相关

[wiki](http://wiki.ros.org/urdf/XML/joint)：查看哪些标签是必须的

![选区_002](/home/speike/图片/选区_002.png)

```xml
<!--名称及活动方式-->
<joint name="my_joint" type="floating">
	<origin xyz="0 0 1" rpy="0 0 3.1416"/>
	<parent link="link1"/>
	<child link="link2"/>

	<calibration rising="0.0"/>
	<dynamics damping="0.0" friction="0.0"/>
	<limit effort="30" velocity="1.0" lower="-2.2" upper="0.7" />
	<safety_controller k_velocity="10" k_position="15" soft_lower_limit="-2.0" soft_upper_limit="0.5" />
</joint>
```

1. **type：**
   - revolute-有上下限的旋转活动
   - continuous-没有上下限的连续旋转
   - prismatic-有上下限的滑动
   - fixed-固定
   - floating-没有约束，可在六个自由度运动，三平移三旋转
   - plannar-允许在垂直于轴的某个平面内移动或转动

### 1.3 偏移关系讲解

```xml
<?xml version="1.0"?>  
<robot name="arckmann_car">

<link name="base_link">
    <!--可视化相关-->
	<visual>
 		<!--几何形状 m-->
        <geometry>
			<box size="5 3 1" />
		</geometry>
        <origin xyz="0 0 0" rpy="0 0 0" />			<!--不偏移-->
		<!--材质-->
        <material name="Cyan">
 			<color rgba="0 1.0 1.0 1.0"/>
		</material>
	</visual>
</link>

<joint name="camera_to_baselink" type="continuous">
    <parent link="base_link"/>
    <child link="camera"/>
    <origin xyz="-1 0 0" rpy="0 0 0"/>				<!--x偏移-1-->
    <axis xyz="0 0 1"/>
</joint>

<link name="camera">
	<visual>
        <geometry>
			<box size="1 1 1" />
		</geometry>
        <origin xyz="0 0 2" rpy="0 0 0" />			<!--z偏移2-->
        <material name="Red">
 			<color rgba="1 0 0 0.5"/>
		</material>
	</visual>
</link>

</robot>  

```

![选区_003](/home/speike/图片/选区_003.png)

如图，base_link不偏移，camera在自身坐标系下向上偏移2，joint标签只是表明了base_link和camera的偏移关系。

## 2. xacro描述机器人

[xacro wiki](http://wiki.ros.org/xacro)

[参考博客](https://blog.csdn.net/baoli8425/article/details/117338338?spm=1001.2101.3001.6650.6&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6-117338338-blog-80398681.pc_relevant_aa&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6-117338338-blog-80398681.pc_relevant_aa&utm_relevant_index=10)

[wiki翻译](https://blog.csdn.net/chishuideyu/article/details/53695392?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165768003816782246475369%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165768003816782246475369&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-53695392-null-null.142^v32^new_blog_fixed_pos,185^v2^control&utm_term=xacro&spm=1018.2226.3001.4187)

- 使用xacro时根标签必须包含 ` <robot name="XXX" xmlns:xacro="http://ros.org/wiki/xacro">  `
- 属性定义：`<xacro:property name="XXXX" value="YYYY">`
- 属性调用：`${XXXX}`
- 属性块定义与调用：

```xml
<xacro:property name="front_left_origin">
  <origin xyz="0.3 0 0" rpy="0 0 0" />
</xacro:property>

<pr2_wheel name="front_left_wheel">
  <xacro:insert_block name="front_left_origin" />
</pr2_wheel>
```

- 数学公式计算：${a+b/c}
- 条件判断的使用

```xml
<xacro:if value="<expression>">  <!-- value="${变量=='值'}" -->
  <... some xml code here ...>
</xacro:if>
<xacro:unless value="<expression>">
  <... some xml code here ...>
</xacro:unless>
```

- 函数定义与调用

```xml
<!--函数声明，传入参数-->
<xacro:macro name="XXXX" params="YY ZZ"> 
${YY}	<!--形参-->
</xacro:macro>

<!--函数调用-->
<xacro:XXXX YY="?"  ZZ="?" />
```

- 头文件包含：` <xacro:include filename="$(find hhbot_description)/urdf/hhbot_body.urdf.xacro" />`

## 3. rviz中加载urdf

```xml
<launch>
  <arg name="model" />
  <param name="robot_description" textfile="$(find suv1)/urdf/suv.urdf" />
  <node name="joint_state_publisher_gui" pkg="joint_state_publisher_gui" type="joint_state_publisher_gui" />
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find suv1)/urdf.rviz" />
</launch>
```



## 4. solidworks阿克曼模型创建

不要用solidworks直接导出的urdf文件去配置，最好是先用简单形状把模型搭好跑通之后去修改link中的vision标签

# 二、Gazebo

## 1. 创造gazebo贴图模型

[Gazebo仿真环境搭建 7:00](https://www.bilibili.com/video/BV1s541197SW?spm_id_from=333.337.search-card.all.click&vd_source=73e7d8f820757a29675895180024f22a)

## 1.为link添加gazebo标签

[gazebo官方网页](https://classic.gazebosim.org/tutorials?tut=ros_urdf&cat=connect_ros)

![[]](/home/speike/图片/截图/截图 2022-07-15 19-05-57.png)

- 添加颜色

[Gazebo material颜色列表](https://blog.csdn.net/qq_42226250/article/details/110881207?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165788126816781685360871%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165788126816781685360871&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-110881207-null-null.142^v32^pc_rank_34,185^v2^control&utm_term=gazebo%20material&spm=1018.2226.3001.4187)

```xml
    <gazebo reference="base_link">
        <material>Gazebo/GreenTransparent</material>
    </gazebo>
```

- 添加摩擦力

## 3. 配置gazebo传感器和执行器

## 4. gazebo加载urdf模型

- 若出现模型翻转或与初始位置不对的情况，如下，将paused改为true，观察初始加载时模型的状态，有可能嵌到了地下

```xml
  <!-- 运行gazebo仿真环境 -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="debug" value="false" />
    <arg name="gui" value="true" />
    <arg name="paused" value="true" />
    <arg name="use_sim_time" value="true" />
    <arg name="headless" value="false" />
  </include>
```

