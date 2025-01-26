# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.latest_message = None

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.latest_message = msg
        
    def get_latest_message(self):
        return self.latest_message

def main(args=None):
    rclpy.init(args=args)
    subscriber_node = MinimalSubscriber()

    try:
        while rclpy.ok():
            rclpy.spin_once(subscriber_node, timeout_sec=0.1)
            latest_msg = subscriber_node.get_latest_message()
            if latest_msg:
                # Process the latest message as needed
                print(f'Latest message in main: "{latest_msg.data}"')
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
