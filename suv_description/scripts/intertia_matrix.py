#!/usr/bin/env python
#  -*-  coding: utf-8  -*- 
# 用于urdf惯性矩阵的计算

#矩形
m=0.2
w=0.15
d=0.03
h=0.02

Ixx=(1/12)*m*(h**2+d**2)
Iyy=(1/12)*m*(w**2+d**2)
Izz=(1/12)*m*(w**2+h**2)

print(Ixx)
print(Iyy)
print(Izz)


#圆柱
# r=0.01
# h=0.03
# m=0.5

# Ixx=(1/12)*m*(3*r**2+h**2)
# Iyy=(1/12)*m*(3*r**2+h**2)
# Izz=(1/2)*m*r**2

# print(Ixx)
# print(Iyy)
# print(Izz)
