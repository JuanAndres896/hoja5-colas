# -*- coding: cp1252 -*-
'''
Universidad del Valle de Guatemala
Algoritmos y Estructuras de Datos - Seccion 31
Juan Andres Garcia - 15046
Rodrigo Barrios - 15009
Guatemala, agosto 24 de 2016
Hoja de trabajo 5: simulacion de procesamiento de datos
'''
# Se importan librerias simpy y random
import simpy
import math
import random 

# Variables y constantes
global CANTIDAD_MEMORIA

RANDOM_SEED = 127 #semilla inicial para los numeros al azar
CANTIDAD_PROCESOS = 25 #cantidad de procesos que se crearan
CAPACIDAD_PROCESOS = 10
TIEMPO_PROCESOS = 1
TIEMPO_IO = 3 #Tiempo maximo que se tardan las operaciones de I/O
CANTIDAD_INSTRUCCIONES = 10 #cantidad maxima de instrucciones que tendrán los procesos
CANTIDAD_MEMORIA = 100 #espacio de memoria RAM
TIEMPO_TOTAL = 0.0 #Contador de tiempo total que se tardan los procesos
PROMEDIO = 0.0 #contador que calcula el promedio de tiempo de ejecucion
lista = []

def Proceso(env, nombre, unidades, ram, io, mem, ins):
	init = int(env.now)
	print('El proceso %s fue creado durante las %s Unidades' %(nombre,init))
	global TIEMPO_TOTAL, TIEMPO_PROCESOS, CAPACIDAD_PROCESOS

	with ram.get(ins) as req:
		yield req
		initready = int(env.now)
		print('El proceso %s ha pasado al estado listo durante las %s Unidades' %(nombre,initready))


		while(ins >0):
			with unidades.request() as req2:
				yield req2
				initprocesos = int(env.now)
				print('El proceso %s ejecutó 3 instrucciones a las %s Unidades' %(nombre,initprocesos))
				ins -= 3
				ram.put(3)


				if(random.randint(1,2)==1):
					with io.request() as req3:
						yield req3
						initIO = int(env.now)
						print('El proceso %s ha entrado a I/O durante las %s Unidades' % (nombre,initIO))
						tiempoesperaIO = random.randint(1,TIEMPO_IO)
						yield env.timeout(tiempoesperaIO)
						salidaIO = int(env.now)
						TIEMPO_PROCESOS = salidaIO - init
						lista.append(salidaIO)
						print('El proceso %s ha finalizado I/O durante las %s Unidades' % (nombre,salidaIO))

		yield env.timeout(TIEMPO_PROCESOS)
		exitprocesos = int(env.now)
		print('El proceso %s ha terminado de procesar a las %s Unidades' %(nombre,exitprocesos))
		TIEMPO_TOTAL = TIEMPO_TOTAL + exitprocesos - init



def Procesar(env, cantidad, capacidad, unidades,io,ram):
	global CANTIDAD_INSTRUCCIONES, CANTIDAD_MEMORIA
	for i in range(cantidad+1):
		memoria = random.randint(1,CAPACIDAD_PROCESOS)
		instruc = random.randint(1,CANTIDAD_INSTRUCCIONES)
		nuevo_proceso = Proceso(env,str(i),unidades,ram,io,memoria,instruc)
		env.process(nuevo_proceso)
		temptime = random.expovariate(1.0/capacidad)
		yield env.timeout(temptime)
	


env = simpy.Environment()
random.seed(RANDOM_SEED)
procesador = simpy.Resource(env, capacity=1)
ram_TOTAL = simpy.Container(env, capacity=CANTIDAD_MEMORIA, init = CANTIDAD_MEMORIA)
io = simpy.Resource(env, capacity=1)
env.process(Procesar(env,CANTIDAD_PROCESOS,CAPACIDAD_PROCESOS,procesador,io,ram_TOTAL))


env.run()
PROMEDIO = TIEMPO_TOTAL/CANTIDAD_PROCESOS
print('El promedio de tiempo en el que se ejecutan los procesos es de %s' % (PROMEDIO))
