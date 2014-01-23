from PIL import Image
from KeyManager import *
from Utils import *
from test.test_iterlen import len


'''
Algoritmo LSB simple
'''
#Este metodo recibe la imagen original y el mensaje a ocultar.
#Devuelve la estego-imagen con el mensaje oculto en ella y el tiempo de procesamiento.
def LSB(coverImage, dataToHide):
    
    #Tiempo de calculo
    start = getTimeMillis()
    
    width, height = coverImage.size
    channelR, channelG, channelB = coverImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()

    dataToHide = dataToHide+'\0' 
    #Convertimos en una lista binaria el mensaje a ocultar
    dataBits = stringTobits(dataToHide)

    lenData = len(dataBits)
    
    #Comprobamos si la imagen tiene una magnitud suficiente (resolucion) grande como para
    #contener el mensaje a ocultar. En caso contrario devolvemos False, -1.
    if width*height*3 < lenData:
        return False, -1
        
    
    #La variable nb se usara como contador para saber por que posicion de la lista binaria vamos.
    nb = 0
    #Recorremos la matriz de pixeles de la imagen
    for i in range(width):
        for j in range(height):
            #Por cada pixel recorremos sus 3 canales RGB
            for c in range(3):
                #Para cada canal comprobamos primero si hemos llegado al final del mensaje.
                #En caso negativo convertimos a binario el valor de la componente correspondiente (0-255)
                #para luego sustituir el bit menos significativo del valor por el bit correspondiente del mensaje y
                #por ultimo incrementamos el indice nb.
                
                #Canal rojo
                if(c == 0):
                    if (nb < lenData):
                        pR = intToBinaryList(pixelsR[i,j])  # int -> bit
                        pR[-1]=dataBits[nb]                 # incluimos mensaje
                        pixelsR[i,j] = BinaryListToInt(pR) # bit -> int
                        nb+=1
                        
                #Canal verde
                elif (c == 1):
                    if (nb < lenData):
                        pG = intToBinaryList(pixelsG[i,j])  # int -> bit
                        pG[-1]=dataBits[nb]                 # incluimos mensaje
                        pixelsG[i,j] = BinaryListToInt(pG) # bit -> int
                        nb+=1
                #Canal azul      
                elif (c == 2):
                    if (nb < lenData):
                        pB = intToBinaryList(pixelsB[i,j])  # int -> bit
                        pB[-1]=dataBits[nb]                 # incluimos mensaje
                        pixelsB[i,j] = BinaryListToInt(pB) # bit -> int
                        nb+=1
                        
                        
    #Una vez insertado completamente el mensaje unimos los 3 canales modificados y creamos la estego-imagen.
    stegoImage = Image.merge("RGB",(channelR,channelG,channelB))
    
    finish = getTimeMillis() - start
    
    return stegoImage, finish
    
    
#Dado una estego-imagen con un mensaje oculto, devuelve el mensaje y el tiempo de procesamiento.
def getMessageLSB(stegoImage):

    #Tiempo de calculo
    start = getTimeMillis()

    width, height = stegoImage.size
    channelR, channelG, channelB = stegoImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()
    
    dataBits = []

    #La variable nb se usara como contador para saber por que posicion de la lista binaria vamos.
    nb = 0
    #Recorremos la matriz de pixeles de la imagen
    for i in range(width):
        for j in range(height):
            #Por cada pixel recorremos sus 3 canales RGB
            for c in range(3):
                #Para cada canal convertimos a binario el valor de la componente correspondiente (0-255)
                #para luego extraer el bit menos significativo e introducirlo en la lista binaria que formara
                #el mensaje final. Por ultimo incrementamos el indice nb.
                
                #Canal rojo
                if(c == 0):
                    pR = intToBinaryList(pixelsR[i,j])  # int -> bit
                    dataBits.append(pR[-1])             # sacamos mensaje
                    nb+=1
                #Canal rojo       
                elif (c == 1):
                    pG = intToBinaryList(pixelsG[i,j])  # int -> bit
                    dataBits.append(pG[-1])             # sacamos mensaje
                    nb+=1
                #Canal rojo
                elif (c == 2):
                    pB = intToBinaryList(pixelsB[i,j])  # int -> bit
                    dataBits.append(pB[-1])             # sacamos mensaje
                    nb+=1
    
    finish = getTimeMillis() - start
    
    m = bitsToString(dataBits).split('\0')
    msg = m[0]
    return msg, finish

'''
Algoritmo LSB usando una clave privada y el operador XOR
'''
#Este metodo recibe la imagen original, el mensaje a ocultar y la longitud que tendra la clave privada.
#Devuelve la estego-imagen con el mensaje oculto en ella y la clave privada generada para ocultar el mensaje
#y el tiempo de procesamiento.
def LSBwithKey(coverImage, dataToHide, keySize):
    
    #Tiempo de calculo
    start = getTimeMillis()
    
    width, height = coverImage.size
    channelR, channelG, channelB = coverImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()
    #Generamos la clave
    key = generateRandomKey(keySize)
    #Preparamos la clave convirtiendola en una lista binaria
    keyList = loadKey(key)
    
    #Convertimos en una lista binaria el mensaje a ocultar
    dataBits = stringTobits(dataToHide)

    #La longitud de la lista binaria del mensaje a ocultar se insertara en la primera
    #fila del canal rojo de forma invertida seguida de tantos ceros como bits queden en la fila.
    lengthDataBits = intToBinaryList(len(dataBits))[::-1]
    
    #La variable c se usara como contador para saber por que posicion de la lista binaria vamos.
    c = 0   
    for i in range(width):
        for j in range(height):
            
            pixelR = pixelsR[i,j]
            #En la primera fila del canal rojo almacenamos la longitud del mensaje
            if i==0:
               
                d = 0
                #Si la longitud ha acabado y sigue habiendo bits, se llenan de ceros
                if j<len(lengthDataBits):
                    d = lengthDataBits[j]
                redBits = intToBinaryList(pixelR)
                redBits[-1] = d
                pixelR = BinaryListToInt(redBits)
                pixelsR[i,j] = pixelR  
                continue
            
            #Aplicamos la operacion logica XOR a los bits menos significativos del canal rojo del
            #pixel actual y al bit correspondiente de la clave.      
            r = int(getLSB(bin(pixelR)))  
            k = int(getCircularData(keyList, c))
            xor = bool(r)^bool(k)
            
            #Si la operacion XOR devuelve 1 (o True) introducimos el siguiente bit del mensaje en el bit
            #menos significativo del canal verde.
            if xor:
                #Sacamos el valor de Green en ese pixel
                pixelG = pixelsG[i,j]
                
                #Sacamos el siguiente bit de la informacion a ocultar
                h = dataBits[c]

                #Transformamos el valor de Green en una lista de ceros y unos
                greenBits = intToBinaryList(pixelG)
                
                #Sustituimos el LSB por el bit de la informacion
                greenBits[-1] =h
                
                #Convertimos la lista binaria en un entero
                pixelG = BinaryListToInt(greenBits)
                #Almacenamos el valor modificado de nuevo en el canal Green
                pixelsG[i,j] = pixelG
            
            #Si la operacion XOR devuelve 0 (o False) lo introducimos en el canal azul.
            else:
                #Sacamos el valor de blue en ese pixel
                pixelB = pixelsB[i,j]
                
                #Sacamos el siguiente bit de la informacion a ocultar
                h = dataBits[c]

                #Transformamos el valor de blue en una lista de ceros y unos
                blueBits = intToBinaryList(pixelB)

                #Sustituimos el LSB por el bit de la informacion
                blueBits[-1] =h
                
                #Convertimos la lista binaria en un entero
                pixelB = BinaryListToInt(blueBits)
                #Almacenamos el valor modificado de nuevo en el canal blue
                pixelsB[i,j] = pixelB
                
            
            if c>=len(dataBits)-1:
                #Hemos terminado de meter el mensaje. Paramos
                break
            c += 1
        if c>=len(dataBits)-1:
            break
    
    #Si terminamos de recorrer la matriz de pixeles y aun queda mensaje por ocultar significa que
    #la dimension de la imagen no es lo suficientemente grande como para que, junto con la clave generada,
    #sea capaz de ocultar todo el mensaje. En tal caso devolvemos False, -1.
    if c<len(dataBits)-1:
        return False, None, -1
    
    #Una vez insertado completamente el mensaje unimos los 3 canales modificados y creamos la estego-imagen.
    stegoImage = Image.merge("RGB",(channelR,channelG,channelB))
    
    finish = getTimeMillis() - start
    
    return stegoImage, key, finish 
  
#Dado una estego-imagen con un mensaje oculto y la clave con la que se ha ocultado, devuelve el mensaje y el tiempo de procesamiento..
def getMessagebyLSBwithKey(stegoImage,key):
    
    #Tiempo de calculo
    start = getTimeMillis()

    width, height = stegoImage.size
    channelR, channelG, channelB = stegoImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()
    
    #Preparamos la clave convirtiendola en una lista binaria
    keyList = loadKey(key)
    
    hiddenData = []
    lengthHiddenData = []
    
    #La variable c se usara como contador para saber por que posicion de la lista binaria vamos.
    c = 0   
    for i in range(width):
        for j in range(height):
            
            pixelR = pixelsR[i,j]
            #Localizamos primero el longitud del mensaje
            if i==0:
                redBits = intToBinaryList(pixelR)
                lengthHiddenData += [redBits[-1]]
                #Si estamos al final de la fila paramos y guardamos la longitud del mensaje
                if(j==height-1):
                    #Como esta fila contenia la longitud invertida del mensaje seguida de ceros,
                    #si ahora invertimos todo el numero binario obtendremos la longitud en binario
                    #del mensaje omitiendo los ceros introducidos que no pertenecian a la cifra.
                    lengthHiddenData = BinaryListToInt(lengthHiddenData[::-1])
                continue

            #Aplicamos la operacion logica XOR a los bits menos significativos del canal rojo del
            #pixel actual y al bit correspondiente de la clave. 
            r = int(getLSB(bin(pixelR)))
            k = int(getCircularData(keyList, c))
            xor = bool(r)^bool(k)
            
            #Si la operacion XOR devuelve 1 (o True) significa que el siguiente bit del mensaje esta en
            #el bit menos significativo del canal verde.
            if xor:
                #Sacamos el valor de Green en ese pixel
                pixelG = pixelsG[i,j]
                
                #Transformamos el valor de Green en una lista de ceros y unos
                greenBits = intToBinaryList(pixelG)

                #Sacamos el LSB y lo introducimos en la variable de reconstruccion de la informacion
                hiddenData += [greenBits[-1]]
            
            #Si la operacion XOR devuelve 0 (o False) esta en el canal azul.
            else:
                #Sacamos el valor de blue en ese pixel
                pixelB = pixelsB[i,j]

                #Transformamos el valor de blue en una lista de ceros y unos
                blueBits = intToBinaryList(pixelB)

                #Sustituimos el LSB por el bit de la informacion
                hiddenData += [blueBits[-1]]

            if c>=lengthHiddenData-1:
                break
            c += 1
        if c>=lengthHiddenData-1:
            break
    
    finish = getTimeMillis() - start    
    
    return bitsToString(hiddenData), finish

'''
Algoritmo TwoLSB o 2LSB. Algoritmo basado en LSB usando una clave privada y el operador XOR en el segundo bit menos significativo
'''
#Este metodo recibe la imagen original, el mensaje a ocultar y la longitud que tendra la clave privada.
#Devuelve la estego-imagen con el mensaje oculto en ella y la clave privada generada para ocultar el mensaje y el tiempo de procesamiento.
def TwoLSB(coverImage, dataToHide, keySize):
    
    #Tiempo de calculo
    start = getTimeMillis()
    
    width, height = coverImage.size
    channelR, channelG, channelB = coverImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()
    #Generamos la clave
    key = generateRandomKey(keySize)
    #Preparamos la clave convirtiendola en una lista binaria
    keyList = loadKey(key)
    
    #Convertimos en una lista binaria el mensaje a ocultar
    dataBits = stringTobits(dataToHide)

    #La longitud de la lista binaria del mensaje a ocultar se insertara en la primera
    #fila del canal rojo de forma invertida seguida de tantos ceros como bits queden en la fila.
    lengthDataBits = intToBinaryList(len(dataBits))[::-1]
    
    #La variable v se usara como contador para saber por que posicion de la clave vamos.
    v = 0
    #La variable v se usara como contador para saber por que posicion de la lista binaria vamos.
    c = 0   
    for i in range(width):
        for j in range(height):
            
            
            #En la primera fila del canal rojo almacenamos la longitud del mensaje
            if i==0:
                pixelR = pixelsR[i,j]
                d = 0
                #Si la longitud ha acabado y sigue habiendo bits, se llenan de ceros
                if j<len(lengthDataBits):
                    d = lengthDataBits[j]
                redBits = intToBinaryList(pixelR)
                redBits[-1] = d
                pixelR = BinaryListToInt(redBits)
                pixelsR[i,j] = pixelR  
                continue

            pixelR = pixelsR[i,j]
            pixelG = pixelsG[i,j]
            pixelB = pixelsB[i,j]
            
            #Hallamos los segundos bits menos significativos de cada canal.
            r2 = int(getTwoLSB(bin(pixelR)))
            g2 = int(getTwoLSB(bin(pixelG)))
            b2 = int(getTwoLSB(bin(pixelB)))

            #Canal rojo
            if c>=len(dataBits):
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal rojo y al bit correspondiente
            #de la clave.
            xor = bool(r2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) introducimos el siguiente bit del mensaje en el bit
            #menos significativo del canal rojo.
            if xor:
                
                #Sacamos el siguiente bit de la informacion a ocultar
                h = dataBits[c]

                #Transformamos el valor de Green en una lista de ceros y unos
                redBits = intToBinaryList(pixelR)
                
                #Sustituimos el LSB por el bit de la informacion
                redBits[-1] =h
                
                #Convertimos la lista binaria en un entero
                pixelR = BinaryListToInt(redBits)
                #Almacenamos el valor modificado de nuevo en el canal Green
                pixelsR[i,j] = pixelR
                
                c += 1   
            
            
            #Canal verde
            if c>=len(dataBits):
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal verde y al bit correspondiente
            #de la clave.
            xor = bool(g2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) introducimos el siguiente bit del mensaje en el bit
            #menos significativo del canal verde.
            if xor:
                #Sacamos el siguiente bit de la informacion a ocultar
                h = dataBits[c]

                #Transformamos el valor de Green en una lista de ceros y unos
                greenBits = intToBinaryList(pixelG)
                
                #Sustituimos el LSB por el bit de la informacion
                greenBits[-1] =h
                
                #Convertimos la lista binaria en un entero
                pixelG = BinaryListToInt(greenBits)
                #Almacenamos el valor modificado de nuevo en el canal Green
                pixelsG[i,j] = pixelG
                
                c += 1   
            
            
            #Canal azul
            if c>=len(dataBits):
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal azul y al bit correspondiente
            #de la clave.
            xor = bool(b2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) introducimos el siguiente bit del mensaje en el bit
            #menos significativo del canal azul.
            if xor:
                #Sacamos el siguiente bit de la informacion a ocultar
                h = dataBits[c]

                #Transformamos el valor de Green en una lista de ceros y unos
                blueBits = intToBinaryList(pixelB)
                
                #Sustituimos el LSB por el bit de la informacion
                blueBits[-1] =h
                
                #Convertimos la lista binaria en un entero
                pixelB = BinaryListToInt(blueBits)
                #Almacenamos el valor modificado de nuevo en el canal Green
                pixelsB[i,j] = pixelB
                
                c += 1   
            
        if c>=len(dataBits):
            break
    
    #Si terminamos de recorrer la matriz de pixeles y aun queda mensaje por ocultar significa que
    #la dimension de la imagen no es lo suficientemente grande como para que, junto con la clave generada,
    #sea capaz de ocultar todo el mensaje. En tal caso devolvemos False, -1.
    if c<len(dataBits)-1:
        return False, None, -1
    
    
    #Una vez insertado completamente el mensaje unimos los 3 canales modificados y creamos la estego-imagen.
    stegoImage = Image.merge("RGB",(channelR,channelG,channelB))
    
    finish = getTimeMillis() - start
    
    return stegoImage, key, finish
    
#Dado una estego-imagen con un mensaje oculto y la clave con la que se ha ocultado, devuelve el mensaje y el tiempo de procesamiento.    
def getMessageTwoLSB(stegoImage,key):
    
    #Tiempo de calculo
    start = getTimeMillis()
    
    width, height = stegoImage.size
    channelR, channelG, channelB = stegoImage.split()
    pixelsR = channelR.load()
    pixelsG = channelG.load()
    pixelsB = channelB.load()
    
    #Preparamos la clave convirtiendola en una lista binaria
    keyList = loadKey(key)
    
    hiddenData = []
    lengthHiddenData = []
    
    #La variable v se usara como contador para saber por que posicion de la clave vamos.
    v = 0
    #La variable v se usara como contador para saber por que posicion de la lista binaria vamos.
    c = 0
 
    for i in range(width):
        for j in range(height):
            
            pixelR = pixelsR[i,j]

            #Localizamos primero la longitud del mensaje
            if i==0:
                redBits = intToBinaryList(pixelR)
                lengthHiddenData += [redBits[-1]]
                #Si estamos al final de la fila paramos y guardamos la longitud del mensaje
                if(j==height-1):
                    #Como esta fila contenia la longitud invertida del mensaje seguida de ceros,
                    #si ahora invertimos todo el numero binario obtendremos la longitud en binario
                    #del mensaje omitiendo los ceros introducidos que no pertenecian a la cifra.
                    lengthHiddenData = BinaryListToInt(lengthHiddenData[::-1])

                continue
            
            pixelG = pixelsG[i,j]
            pixelB = pixelsB[i,j]
            
            #Hallamos los segundos bits menos significativos de cada canal.
            r2 = int(getTwoLSB(bin(pixelR)))
            g2 = int(getTwoLSB(bin(pixelG)))
            b2 = int(getTwoLSB(bin(pixelB)))
            
            #Canal rojo
            if c>=lengthHiddenData:
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal rojo y al bit correspondiente
            #de la clave.
            xor = bool(r2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) significa que el siguiente bit del mensaje esta en
            #el bit menos significativo del canal rojo.
            if xor:
                
                #Transformamos el valor de Green en una lista de ceros y unos
                redBits = intToBinaryList(pixelR)

                #Sacamos el LSB y lo introducimos en la variable de reconstruccion de la informacion
                hiddenData += [redBits[-1]]

                c += 1   
                       
            ##Canal verde
            if c>=lengthHiddenData:
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal verde y al bit correspondiente
            #de la clave.
            xor = bool(g2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) significa que el siguiente bit del mensaje esta en
            #el bit menos significativo del canal verde.
            if xor:
                
                #Transformamos el valor de Green en una lista de ceros y unos
                greenBits = intToBinaryList(pixelG)

                #Sacamos el LSB y lo introducimos en la variable de reconstruccion de la informacion
                hiddenData += [greenBits[-1]]

                c += 1   
                       
            ##Canal azul
            if c>=lengthHiddenData:
                break
            k = int(getCircularData(keyList, v))
            v += 1
            #Aplicamos la operacion logica XOR al segundo bit menos significativo del canal azul y al bit correspondiente
            #de la clave.
            xor = bool(b2)^bool(k)
            #Si la operacion XOR devuelve 1 (o True) significa que el siguiente bit del mensaje esta en
            #el bit menos significativo del canal azul.
            if xor:
                   
                #Transformamos el valor de Green en una lista de ceros y unos
                blueBits = intToBinaryList(pixelB)

                #Sacamos el LSB y lo introducimos en la variable de reconstruccion de la informacion
                hiddenData += [blueBits[-1]]

                c += 1   
      
        if c>=lengthHiddenData:
            break
        
    finish = getTimeMillis() - start
        
    return bitsToString(hiddenData), finish
