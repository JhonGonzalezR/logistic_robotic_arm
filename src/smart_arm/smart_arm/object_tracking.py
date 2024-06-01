#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import subprocess
import signal
import os
from objectpose_msgs.msg import ObjectPose
from example_interfaces.msg import Bool
import time
from example_interfaces.msg import String


class ObjectTracker(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("Object_tracker") # MODIFY NAME

        self.subscription_3 = self.create_subscription(String, "verde_color", self.color_callback, 10)

        self.subscription_1 = self.create_subscription(ObjectPose, "/box1/ObjectPose", self.sus_callback, 10)
        self.subscription_2 = self.create_subscription(Bool, "posicionado", self.poscallback, 10)

        self.posicionado = False

    def poscallback(self,data):
        self.posicionado = data.data

    def color_callback(self, data):
        self.color = data.data


    def sus_callback(self, data):
        if self.posicionado:

            self.get_logger().info(f"ENTROOOOOO")
            
            agarraX = round((data.x)-0.18,2)
            agarraY = round(data.y,2)
            agarraZ = round((data.z)+0.1,2)

            # agarraX = round((data.x)-0.18,2)
            # agarraY = round(data.y,2)
            # agarraZ = round((data.z)+0.1,2)

            # ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW "{positionx: 0.00, positiony: 0.00, positionz: 0.00, yaw: 0.00, pitch: 0.00, roll: 0.00, speed: 1.0}"
            xd = f"positionx: {agarraX}, positiony: {agarraY}, positionz: {agarraZ}, yaw: 90, pitch: 45, roll: 90, speed: 1.0"
            agarra = 'ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW ' + '"{' + xd + '}"'

            print(agarra)

            self.get_logger().info(f"Yendo")

            self.resultado = subprocess.Popen([agarra], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

            self.get_logger().info(f"FUEEE")
            time.sleep(5)
            # ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: 0.00, movez: 0.00, speed: 1.0}"
            self.get_logger().info(f"baja")
           
            bajar = 'ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: 0.00, movez: -0.09, speed: 1.0}"'

            self.resultado = subprocess.Popen([bajar], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
            time.sleep(5)

            self.get_logger().info(f"gripper")
            gripper = 'ros2 action send_goal -f /MoveG ros2_data/action/MoveG "{goal: 0.01}"'

            self.resultado = subprocess.Popen([gripper], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

            time.sleep(5)
            self.get_logger().info(f"agarrar")
            coger = 'ros2 action send_goal -f /Attacher ros2_grasping/action/Attacher "{object: "box1", endeffector: "EE_egp64"}"'
            self.resultado = subprocess.Popen([coger], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

            time.sleep(5)
            self.get_logger().info(f"subir")
            subir = 'ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: 0.00, movez: 0.20, speed: 1.0}"'
            self.resultado = subprocess.Popen([subir], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

            ############
            if self.color == 'verde':
                time.sleep(5)
                self.get_logger().info(f"subir mas")
                subirrojo = 'ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: 0.00, movez: 0.10, speed: 1.0}"'
                self.resultado = subprocess.Popen([subirrojo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)


                time.sleep(5)
                self.get_logger().info(f"izquierda")
                izquierda = 'ros2 action send_goal -f /MoveR ros2_data/action/MoveR "{joint: "joint1", value: 90.00, speed: 1.0}"'
                self.resultado = subprocess.Popen([izquierda], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

                time.sleep(5)
                self.get_logger().info(f"frente")
                frenterojo = 'ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: 0.50, movez: 0.00, speed: 1.0}"'
                self.resultado = subprocess.Popen([frenterojo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

                time.sleep(5)
                self.get_logger().info(f"gripper")
                gripperrojo = 'ros2 action send_goal -f /MoveG ros2_data/action/MoveG "{goal: -0.01}"'
                self.resultado = subprocess.Popen([gripperrojo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

                time.sleep(5)
                soltarrojo ='ros2 topic pub --rate 999999999 /ros2_Detach std_msgs/msg/String "{data: "True"}"'
                self.resultado = subprocess.Popen([soltarrojo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

                time.sleep(5)
                self.get_logger().info(f"atras")
                atrasrojo = 'ros2 action send_goal -f /MoveL ros2_data/action/MoveL "{movex: 0.00, movey: -0.10, movez: 0.00, speed: 1.0}"'
                self.resultado = subprocess.Popen([atrasrojo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)






            ###########




            time.sleep(2)
            self.get_logger().info(f"girar")
            girar = 'ros2 action send_goal -f /MoveR ros2_data/action/MoveR "{joint: "joint1", value: 90.0, speed: 1.0}"'
            self.resultado = subprocess.Popen([girar], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)


            # ### Pensar en que reciba la información del color y con respecto a esto baje en el eje z



            self.posicionado = False



def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracker() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
