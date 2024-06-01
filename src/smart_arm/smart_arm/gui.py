#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import tkinter as tk
import subprocess
import signal
import os
import time

from objectpose_msgs.msg import ObjectPose
from example_interfaces.msg import Bool



class Gui(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("gui") # MODIFY NAME
        self.caja = 1
        

        #self.subscription = self.create_subscription(ObjectPose, "/box1/ObjectPose", self.sus_callback, 10)

        self.publisher_ = self.create_publisher(Bool, "posicionado",10)
        

        self.crearVentana()
        self.posicionado = False

        #self_publisher_ = self.create_publisher(Bool, "posicionado",10)


        #self.subscription = self.create_subscription(ObjectPose, "/box1/ObjectPose", self.sus_callback, 10)

    def nuevo_objeto(self):

        #objeto = 'ros2 run smart_arm objeto'
        #cinta = 'ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 30}"'
        spawm = f'ros2 run ros2_objectpose SpawnObject.py --package "objectpose_gazebo" --urdf "box_green.urdf" --name "box{self.caja}" --x 0.65 --y -0.02 --z 0.8'
        self.get_logger().info(f"CINTA Y CAJA{self.caja}")
        self.caja += 1

        #self.resultado = subprocess.Popen([objeto], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        #self.resultado = subprocess.Popen([cinta], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        self.resultado = subprocess.Popen([spawm], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        

        time.sleep(4)

        #stop_cinta = 'ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 0}"'
        #self.resultado = subprocess.Popen([stop_cinta], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        self.get_logger().info(f"CINTA PARADA")
        time.sleep(3)

        self.posicionado = True

        #self.publish_posicionado()
        time.sleep(3)
        self.publish_posicionado()
        self.posicionado = False

        self.publish_posicionado()





    def publish_posicionado(self):
        msj = Bool()
        msj.data = self.posicionado
        self.publisher_.publish(msj)

    def sus_callback(self, data):
        self.get_logger().info(f"RECIBE DATOS DE POSICION")
        if self.posicionado:
            agarraX = (data.x)-0.18
            agarraY = data.y
            agarraZ = (data.z)+0.1

            # agarraX = round((data.x)-0.18,2)
            # agarraY = round(data.y,2)
            # agarraZ = round((data.z)+0.1,2)

            xd = f"positionx: {agarraX}, positiony: {agarraY}, positionz: {agarraZ}, yaw: 90, pitch: 45, roll: 90, speed: 1.0"
            agarra = 'ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW ' + xd

            self.get_logger().info(f"Yendo")

            self.resultado = subprocess.Popen([agarra], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)



    def seleccionar_video(self):
        comandoVideo = 'ros2 launch parcial1 parcial1_video.launch.py'
        self.get_logger().info("Ejecutando comando para seleccionar un video")

        self.resultado = subprocess.Popen([comandoVideo], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

       
    def salir(self):
        os.killpg(os.getpgid(self.resultado.pid), signal.SIGINT)
        


    def crearVentana(self):
        ventana = tk.Tk()
        ventana.title("Sistema de Percepción")

        # Texto superior
        etiqueta_superior = tk.Label(ventana, text="Percepción robótica Jhon Edward Gonzalez - Cesar Andres Ramirez")
        etiqueta_superior.pack(pady=10)


        ventana.geometry("600x400")

        canvas = tk.Canvas(ventana, height=400, width=600)
        canvas.pack()

        btn_nuevo_objeto = tk.Button(canvas, text="Nuevo objeto", command=self.nuevo_objeto, height=5, width=20)
        # btn_seleccionar_video = tk.Button(canvas, text="Seleccionar Video", command=self.seleccionar_video, height=5, width=20)
        # btn_salir = tk.Button(canvas, text="Terminar proceso", command=self.salir, height=5, width=20)

        canvas.create_window(150, 150, window=btn_nuevo_objeto)
        # canvas.create_window(450, 150, window=btn_seleccionar_video)
        # canvas.create_window(300, 300, window=btn_salir)

        # Agregar texto en la parte inferior
        #texto = tk.Label(ventana, text="Parcial 1 Percepción robótica Jhon Edward Gonzalez - Juan Sebastian Burbano")
        #texto.pack(side="bottom")

        ventana.mainloop()





    


def main(args=None):
    rclpy.init(args=args)
    node = Gui() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
