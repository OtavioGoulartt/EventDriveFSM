#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from rclpy.qos import qos_profile_sensor_data
import numpy as np
import math

class YawNoiseNode(Node):
    def __init__(self):
        super().__init__('simulated_yaw_noise_node')

        self.pub_imu = self.create_publisher(Imu, 'imu', qos_profile_sensor_data)
        self.sub_imu = self.create_subscription(Imu, 'fsds/imu', self.imu_callback, qos_profile_sensor_data)

        self.declare_parameter('noise_std_dev_deg', 0.5)

    def imu_callback(self, imu_msg):
        std_dev_deg = self.get_parameter('noise_std_dev_deg').value
        std_dev_rad = math.radians(std_dev_deg)
        
        noisy_imu = Imu()
        noisy_imu.header = imu_msg.header
        
        noisy_imu.angular_velocity = imu_msg.angular_velocity
        noisy_imu.linear_acceleration = imu_msg.linear_acceleration

        noisy_imu.angular_velocity_covariance = imu_msg.angular_velocity_covariance
        noisy_imu.linear_acceleration_covariance = imu_msg.linear_acceleration_covariance
        
        new_orientation_cov = list(imu_msg.orientation_covariance)
        new_orientation_cov[8] += (std_dev_rad ** 2)
        noisy_imu.orientation_covariance = new_orientation_cov

        q = imu_msg.orientation
        roll, pitch, yaw = self.euler_from_quaternion(q.x, q.y, q.z, q.w)
        
        yaw_noise_rad = np.random.normal(0.0, std_dev_rad)
        noisy_yaw = yaw + yaw_noise_rad

        qx, qy, qz, qw = self.quaternion_from_euler(roll, pitch, noisy_yaw)
        
        noisy_imu.orientation.x = qx
        noisy_imu.orientation.y = qy
        noisy_imu.orientation.z = qz
        noisy_imu.orientation.w = qw

        self.pub_imu.publish(noisy_imu)

    def euler_from_quaternion(self, x, y, z, w):
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)
        return roll, pitch, yaw

    def quaternion_from_euler(self, roll, pitch, yaw):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return qx, qy, qz, qw

def main(args=None):
    rclpy.init(args=args)
    node = YawNoiseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()  