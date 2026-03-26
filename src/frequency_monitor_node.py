#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64


class FrequencyMonitorNode(Node):
    def __init__(self):
        super().__init__('frequency_monitor_node')
        self.msg_type = Odometry
        self.msg_topic = '/fsds/testing_only/odom'

        self.subscription = self.create_subscription(self.msg_type, self.msg_topic, self.freq_callback, 10)
        self.stamp_frequency_pub = self.create_publisher(Float64, 'stamp_frequency_pub', 10)
        self.time_frequency_pub = self.create_publisher(Float64, 'time_frequency_pub', 10)

        self.last_stamp = None
        self.last_time = None

    def freq_callback(self, msg):
        stamp_frequency = Float64()
        time_frequency = Float64()

        stamp_sec = msg.header.stamp.sec
        stamp_nsec = msg.header.stamp.nanosec
        new_stamp = stamp_sec + stamp_nsec / 1e9

        self.current_time = self.get_clock().now().to_msg()
        new_time = self.current_time.sec + self.current_time.nanosec * 1e-9

        if self.last_stamp is None:
            self.last_stamp = new_stamp
            self.last_time = new_time
            return
        
        delta_stamp = new_stamp - self.last_stamp
        if delta_stamp > 0:
            stamp_frequency.data = 1.0 / delta_stamp
            self.stamp_frequency_pub.publish(stamp_frequency)
        
        delta_time = new_time - self.last_time
        if delta_time > 0:
            time_frequency.data = 1.0 / delta_time
            self.time_frequency_pub.publish(time_frequency)

        self.last_stamp = new_stamp
        self.last_time = new_time


def main(args=None):
    rclpy.init(args=args)
    frequency_monitor_node = FrequencyMonitorNode()
    rclpy.spin(frequency_monitor_node)
    frequency_monitor_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()