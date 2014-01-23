from Algorithms import *

print "===================================================================================================="
print "Tecnicas Esteganograficas en imagenes basadas ocultacion en los bits menos significativos (LSB)"
print "Procesamiento de Imagenes Digitales 2013-2014"
print "E.T.S.I. Informatica. Universidad de Sevilla"
print "\nAutores:\nManuel Jesus Gonzalez Rodriguez\nAngel Cayetano Gomez Gil"
print "====================================================================================================\n\n"

images = []

images.append(Image.open("images/coche_1600_1200.png"))
images.append(Image.open("images/pollito_1024_768.png"))
images.append(Image.open("images/flor_1024_768.png"))
images.append(Image.open("images/pancho_256.png"))
messages = []
messages.append("Sic parvis magna")
messages.append("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

results = []



for img in images:
    for msg in messages:
        localResult = []
        localResult.append(img.size)
        localResult.append(len(stringTobits(msg)))
        print "____________________________________________________________________________________________________"
        print "--LSB simple--\n"
        print "Mensaje a ocultar: "+msg
        print "Ocultando mensaje..."
        stegoIm, duration = LSB(img, msg)
        localResult.append(duration)
        stegoIm.save('images/stegoLSBSimple.png')
        stegoIm = Image.open('images/stegoLSBSimple.png')
        print "Mensaje ocultado. Tiempo de ejecucion: "+str(duration)+"ms."
        print "PSNR entre la imagen original y la estego-imagen generada: "+str(calcPSNR(img, stegoIm))
        print "Comprobacion del mensaje oculto. Extrayendo mensaje..."
        msg1, duration = getMessageLSB(stegoIm)
        localResult.append(duration)
        localResult.append(calcPSNR(img, stegoIm))
        print "Mensaje extraido: "+msg1+". Tiempo requerido: "+str(duration)+"ms."
        results.append(localResult)
        localResult = []
        localResult.append(img.size)
        localResult.append(len(stringTobits(msg)))
        print "____________________________________________________________________________________________________"
        print "--LSB usando una clave privada y el operador XOR--\n"
        print "Mensaje a ocultar: "+msg
        print "Ocultando mensaje..."
        stegoIm,key, duration = LSBwithKey(img, msg, 256)
        localResult.append(duration)
        stegoIm.save('images/stegoLSBKeyXOR.png')
        stegoIm = Image.open('images/stegoLSBKeyXOR.png')
        print "Mensaje ocultado. Tiempo de ejecucion: "+str(duration)+"ms."
        print "Clave generada: "+str(key)
        print "PSNR entre la imagen original y la estego-imagen generada: "+str(calcPSNR(img, stegoIm))
        print "Comprobacion del mensaje oculto. Extrayendo mensaje..."
        msg1, duration = getMessagebyLSBwithKey(stegoIm,key)
        localResult.append(duration)
        localResult.append(calcPSNR(img, stegoIm))
        print "Mensaje extraido: "+msg1+". Tiempo requerido: "+str(duration)+"ms."
        print "____________________________________________________________________________________________________"
        results.append(localResult)
        localResult = []
        localResult.append(img.size)
        localResult.append(len(stringTobits(msg)))
        print "____________________________________________________________________________________________________"
        print "--2LSB--\n"
        print "Mensaje a ocultar: "+msg
        print "Ocultando mensaje..."
        stegoIm,key, duration = TwoLSB(img, msg, 256)
        localResult.append(duration)
        stegoIm.save('images/stego2LSB.png')
        stegoIm = Image.open('images/stego2LSB.png')
        print "Mensaje ocultado. Tiempo de ejecucion: "+str(duration)+"ms."
        print "Clave generada: "+str(key)
        print "PSNR entre la imagen original y la estego-imagen generada: "+str(calcPSNR(img, stegoIm))
        print "Comprobacion del mensaje oculto. Extrayendo mensaje..."
        msg1, duration = getMessageTwoLSB(stegoIm,key)
        localResult.append(duration)
        localResult.append(calcPSNR(img, stegoIm))
        print "Mensaje extraido: "+msg1+". Tiempo requerido: "+str(duration)+"ms."
        print "____________________________________________________________________________________________________"
        results.append(localResult)
        print "Resumen de resultados"
        for res in results:
            print "Dimension de la imagen: "+str(res[0])
            print "Dimension del mensaje: "+str(res[1])
            print "Duracion de la ocultacion: "+str(res[2])
            print "Duracion de la extraccion: "+str(res[3])
            print "PSNR: "+str(res[4])
            print "___________________________\n"