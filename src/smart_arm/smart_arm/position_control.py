import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from moveit_msgs.srv import GetPositionIK
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import RobotTrajectory
from moveit_msgs.srv import GetMotionPlan
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from rclpy.action import ActionClient

class MoveIt2ArmController(Node):
    def __init__(self):
        super().__init__('moveit2_arm_controller')
        
        # Create Action Client for MoveGroup
        self.move_group_client = ActionClient(self, MoveGroup, 'move_group')
        self.get_logger().info("MoveGroup Action Client created")

        # Define the target pose
        self.target_pose = PoseStamped()
        self.target_pose.header.frame_id = 'world'
        self.target_pose.pose.position.x = 0.4
        self.target_pose.pose.position.y = 0.2
        self.target_pose.pose.position.z = 0.4
        self.target_pose.pose.orientation.w = 1.0

        # Set the target pose and execute the motion
        self.plan_and_execute()

    def plan_and_execute(self):
        goal = MoveGroup.Goal()
        goal.request.group_name = 'irb120_arm'
        goal.request.pose_goal = self.target_pose

        self.get_logger().info("Sending goal to MoveGroup")
        self.move_group_client.wait_for_server()
        self.move_group_client.send_goal_async(goal)

        self.get_logger().info("Goal sent")

def main(args=None):
    rclpy.init(args=args)
    moveit2_arm_controller = MoveIt2ArmController()
    rclpy.spin(moveit2_arm_controller)
    moveit2_arm_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
