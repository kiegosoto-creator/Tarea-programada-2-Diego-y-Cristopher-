#Elaborado por: Cristopher Abel Jara Salazar, y Diego Kim Soto.
#Fecha de elaboracion: 22/5/2026 6:00 PM.
#Ultima modificacion: 24/5/2026 11:00 PM.
#Version: 0.0.0

#Pruebas requeridas para el progreso y uso de la interface grafica.
#CLase 1 Ventana
from tkinter import*

raiz=Tk()

raiz.title('Ventana de prueba.')

#raiz.resizable(False,False)# (Ancho, Altura)

#raiz.iconbitmap("python2.ico")#Da error porque no se encuentra en el file.

#raiz.geometry("650x350")# Tamanno

raiz.config(bg="green")
#Clase 2 Frame

miFrame=Frame()
miFrame.pack(fill="both",expand="True")#Lo une y coloca en raiz.
# Difreciones top botom left right, and n->Nort s e o...fill x y axis/both
miFrame.config(bg="red")#Nota, desactiva el tamanno de la raiz.
miFrame.config(width="650",height="350")#Nota: Desactiva el lock en camio de tamanno
miFrame.config(bd=20)
miFrame.config(relief="sunken")#groove, 

miFrame.config(cursor="pirate")# Cambiar cursor. hand2

raiz.mainloop()# Ultima linea en orden.(Regla)

#Nota: Cambiar el nombre de una copia al mismo
#      nombre pero con w al final hace que se active
#      sin que aparesca la consola.

#Definicion de funciones.

def menuPrincipal():
  while True:
    print('\nMenu Principal de...')
    print('\n1.Insertar donador.')
    print('2.Generar donadores')
    print('3.Actualizar datos del donador.')
    print('4.Eliminnar donador.')
    print('5.Insertar lugar de donacion segun provincia.')
    print('6.Reportes.')
    print('7.Salir')
    opcion=input('\n:_')
    if opcion=='7':
      print('\nSaliendo del programa...')
      break
    elif opcion=='6':
      print('')
    elif opcion=='5':
      print('')
    elif opcion=='4':
      print('')
    elif opcion=='3':
      print('')
    elif opcion=='2':
      print('')
    elif opcion=='1':
      print('')
    else:
      print('\nOpcion no valida.')
      input('\nIngrese (ENTER), para continuar.')

#Funcion principal.
