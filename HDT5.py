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

RANDOM_SEED = 127
CANTIDAD_PROCESOS = 25
CAPACIDAD_PROCESOS = 10
TIEMPO_PROCESOS = 1
TIEMPO_IO = 2
CANTIDAD_INSTRUCCIONES = 3 
CANTIDAD_MEMORIA = 100
TIEMPO_TOTAL = 0.0
PROMEDIO = 0.0
lista = []

def Proceso(env, nombre, unidades, ram, io, mem, ins):
	init = env.now
	print('El proceso %s fue creado durante las %s Unidades' %(nombre,init))
	global TIEMPO_TOTAL, TIEMPO_PROCESOS, CAPACIDAD_PROCESOS

	with ram.get(mem) as req:
		yield req
		initready = env.now
		print('El proceso %s ha pasado al estado listo durante las %s Unidades' %(nombre,initready))

		while(ins >0):
			with unidades.request() as req2:
				yield req2
				initprocesos = env.now
				print('El proceso %s se ha empezado a procesar a las %s Unidades' %(nombre,initprocesos))

				yield env.timeout(TIEMPO_PROCESOS)
				exitprocesos = env.now
				print('El proceso %s ha terminado de procesar a las %s Unidades' %(nombre,exitprocesos))

				if(ins < CAPACIDAD_PROCESOS):
					terminadoProceso = env.now
					print('El proceso %s ha finalizado durante las %s Unidades' %(nombre,terminadoProceso))
					terminadoProceso = env.now
					tiempoTerminado = terminadoProceso - init
					lista.append(tiempoTerminado)
					TIEMPO_TOTAL = TIEMPO_TOTAL + tiempoTerminado
					ram.put(mem)
					ins = 0
				else:
					ins -= CAPACIDAD_PROCESOS
					if(random.randint(1,2)==1):
						with io.request() as req3:
							yield req3
							initIO = env.now
							print('El proceso %s ha entrado a I/O durante las %s Unidades' % (nombre,initIO))
							tiempoesperaIO = random.randint(1,tiempoIO)
							yield env.timeout(tiempoesperaIO)
							salidaIO = env.now
							TIEMPO_PROCESOS = salidaIO - init
							lista.append(tiempoTerminado)
							TIEMPO_TOTAL = TIEMPO_TOTAL + tiempoTerminado
							print('El proceso %s ha finalizado I/O durante las %s Unidades' % (nombre,salidaIO))



def Procesar(env, cantidad, capacidad, unidades,io,ram):
	global CANTIDAD_INSTRUCCIONES, CANTIDAD_MEMORIA
	for i in range(cantidad):
		memoria = random.randint(1,CANTIDAD_MEMORIA)
		instruc = random.randint(1,CANTIDAD_INSTRUCCIONES)
		nuevo_proceso = Proceso(env,('%s' % i),unidades,ram,io,memoria,instruc)
		env.process(nuevo_proceso)
		temptime = random.expovariate(1.0/capacidad)

env = simpy.Environment()
random.seed(RANDOM_SEED)
procesador = simpy.Resource(env, capacity=2)
ram_TOTAL = simpy.Container(env, capacity=CANTIDAD_MEMORIA, init = CANTIDAD_MEMORIA)
io = simpy.Resource(env, capacity=2)
env.process(Procesar(env, CANTIDAD_PROCESOS,CAPACIDAD_PROCESOS,procesador,io,ram_TOTAL))

env.run()