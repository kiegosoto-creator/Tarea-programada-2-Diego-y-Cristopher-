#Elaborado por: Cristopher Abel Jara Salazar, y Diego Kim Soto.
#Fecha de elaboracion: 22/5/2026 6:00 PM.
#Ultima modificacion: 24/5/2026 11:00 PM.
#Version: 0.0.0

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
