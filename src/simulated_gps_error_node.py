#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import numpy as np
import time



class GpsErrorNode(Node):
    def __init__(self):
        super().__init__('simulated_gps_error_node')

        self.pub_gps = self.create_publisher(NavSatFix, 'gps/fix', 10)
        self.sub_gps = self.create_subscription(NavSatFix, '/fsds/gps', self.error_callback, 10)

        self.declare_parameter('gaussian_noise', True)
        self.declare_parameter('accumulated_drift', False)
        
        self.gaussian_noise = self.get_parameter('gaussian_noise').value
        self.accumulated_drift = self.get_parameter('accumulated_drift').value

        self.lat_drift = 0
        self.lon_drift = 0


    def error_callback(self, gps_msg):
        noisy_gps = NavSatFix()
        noisy_gps.header = gps_msg.header
        #noisy_gps.child_frame_id = gps_msg.child_frame_id

        noisy_gps.latitude = gps_msg.latitude
        noisy_gps.longitude = gps_msg.longitude
        noisy_gps.altitude = gps_msg.altitude

        noisy_gps.position_covariance = gps_msg.position_covariance
        noisy_gps.position_covariance_type = gps_msg.position_covariance_type

        if self.accumulated_drift:
            noisy_gps = self.apply_drift(gps_msg, noisy_gps)

        if self.gaussian_noise:
            noisy_gps = self.apply_gaussian_noise(gps_msg, noisy_gps)

        self.pub_gps.publish(noisy_gps)


    def apply_drift(self, gps, drifted_gps):
        self.lat_drift += np.random.normal(0, 0.01)
        self.lon_drift += np.random.normal(0, 0.01)

        drifted_gps.latitude = gps.latitude + self.lat_drift
        drifted_gps.longitude = gps.longitude + self.lon_drift

        return drifted_gps


    def apply_gaussian_noise(self, gps, noisy_gps):
        lat_noise = np.random.normal(0, 0.00001)
        lon_noise = np.random.normal(0, 0.00001)

        noisy_gps.latitude = gps.latitude + lat_noise
        noisy_gps.longitude = gps.longitude + lon_noise
        
        return noisy_gps
    

def main(args=None):
    rclpy.init(args=args)
    node = GpsErrorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()