#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from message_filters import Subscriber, ApproximateTimeSynchronizer
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from vectornav_msgs.msg import ImuGroup
from vectornav_msgs.msg import InsGroup
from vectornav_msgs.msg import AttitudeGroup
import matplotlib.pyplot as plt
from nav_msgs.msg import Odometry


class OdomPlotNode(Node):
    def __init__(self):
        super().__init__('odom_plot_node')

        self.odom_sub = self.create_subscription(Odometry, '/odometry/filtered', self.odom_callback, 10)

        self.x_data = []
        self.y_data = []
        
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x_data, self.y_data, '-b', label='Odometry')
        
        self.ax.set_xlabel("X position (m)")
        self.ax.set_ylabel("Y position (m)")
        self.ax.legend()
        self.ax.grid(True)

        self.ax.axis('equal')

    def odom_callback(self, odom_msg):
        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y

        self.x_data.append(x)
        self.y_data.append(y)

        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)

        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        


def main(args=None):
    rclpy.init()
    odom_plot_node = OdomPlotNode()
    rclpy.spin(odom_plot_node)
    odom_plot_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()