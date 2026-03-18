#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64


class FrequencyMonitorNode(Node):
    def __init__(self):
        super().__init__('ekf_sim_node')
        self.msg_type = Odometry
        self.msg_topic = '/fsds/testing_only/odom'

        self.subscription = self.create_subscription(self.msg_type, self.msg_topic, self.freq_callback, 10)
        self.frequency_pub = self.create_publisher(Float64, 'frequency_pub', 10)

        self.last_time = None

    def freq_callback(self, msg):
        self.frequency = Float64()
        stamp_sec = msg.header.stamp.sec
        stamp_nsec = msg.header.stamp.nanosec

        new_time = stamp_sec + stamp_nsec / 1e9

        if self.last_time is None:
            self.last_time = new_time
            return
        
        delta_time = new_time - self.last_time
        self.last_time = new_time
        
        if delta_time == 0:
            return
        
        self.frequency.data = 1.0 / delta_time

        self.frequency_pub.publish(self.frequency)


def main(args=None):
    rclpy.init(args=args)
    frequency_monitor_node = FrequencyMonitorNode()
    rclpy.spin(frequency_monitor_node)
    frequency_monitor_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()