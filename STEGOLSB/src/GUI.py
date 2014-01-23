from Tkinter import *
from ttk import *
from PIL import Image, ImageTk
from Algorithms import *
import tkFileDialog

master = Tk()
master.title("Tecnicas basadas LSB - Estegoimagenes")

tutotex = []
tutotex.append("\tLSB es una tecnica que modifica el bit menos significativo con cada bit del mensaje a cifrar")
tutotex.append("\tLSBXOR es una tecnica que  modifica el bit menos significativo del canal verde o azul con cada bit del mensaje a cifrar segun la operacion xor entre el canal rojo con la clave generada")
tutotex.append("\t2LSB es una tecnica que modifica el bit menos significativo de cada canal de color con cada bit del mensaje a cifrar segun la operacion xor entre el segundo bit menos significativo con la clave generada")


widthImage,height_Image = 420,360

global imageFileGlobal
imageFileGlobal = StringVar()
imageFileGlobal.set("images/no-image.png")
global imagenGlobal
imagenGlobal = Image.open(imageFileGlobal.get())

print "INIT"


mensage = StringVar()
mensage.set("Aqui saldra tu texto desencriptado")
info = StringVar()
info.set("PSNR:")
time = StringVar()
time.set("Tiempo: -")
txt = StringVar()
txt.set(imageFileGlobal.get())

notebook = Notebook(master)
notebook.pack(fill='both', expand='no')
key = StringVar()
key.set("No Key")

def getInfo():
    print "imageFileGlobal.get(): "+txt.get()
    
def loadKeyfromUser(wid):
    k=wid.get()
    key.set(k)
    
def copyKey(wid):
    wid.set(key.get())
    
def encript(texto_a_encriptar,algorithm):
    imagenGlobal = Image.open(imageFileGlobal.get())
    print "PATH: "+imageFileGlobal.get()
    t = 0
    print("Encriptando ...")
    stegoIm = ""
    if(algorithm == 0):
        stegoIm,t =LSB(imagenGlobal, texto_a_encriptar)
        
    elif algorithm == 1:
        stegoIm,k,t=LSBwithKey(imagenGlobal, texto_a_encriptar, 256)
        key.set(str(k))
        print "KEY:"+key.get()
        
    else:
        stegoIm,k,t=TwoLSB(imagenGlobal, texto_a_encriptar, 256)
        key.set(str(k))
        print "KEY:"+key.get()
       
    time.set("Tiempo: "+str(t))
    print("Listo")
    print("PATH: ",imageFileGlobal.get())
    paths = imageFileGlobal.get().split('.')
    print("Grabando imagen",paths[0]+"-STEGO."+paths[1])
    stegoIm.save(paths[0]+"-STEGO."+paths[1])
    print "Calculando vericidad"
    psnr = calcPSNR(imagenGlobal, stegoIm)
    print ("PSNR",psnr)
    info.set("PSNR: "+str(psnr))
    print("Listo")
    
def guardarMensaje(msg):
    path = imageFileGlobal.get().split('.')
    file = open(path[0]+"_msg.txt",'w') 
    file.write(str(msg)) 
    file.close() 
    
def desencript(algorithm):
    imagenGlobal = Image.open(imageFileGlobal.get())
    t=0
    print("Desencriptando ...")
    data = ""
    if(algorithm == 0):
        data,t = getMessageLSB(imagenGlobal)
        
    elif algorithm == 1:
        data,t = getMessagebyLSBwithKey(imagenGlobal, long(key.get()))
        
    else:
        data,t = getMessageTwoLSB(imagenGlobal, long(key.get()))
        
    time.set("Tiempo: "+str(t))
    print("Listo")
    print("El mensaje es:",data)
    
    guardarMensaje(data)
    
    mensage.set(data)
        
def loadImage(frame,algorithm):
    
    print "Cargando nueva imagen ... Pestana: "+str(algorithm)
    # Con la imagen que haya cargado el usuario ...
    newPath = tkFileDialog.askopenfilename(parent = master, filetypes = [('PNG', '*.png')], multiple = 1 )
    imageFileGlobal .set(newPath)
    print imageFileGlobal.get()
    txt.set(imageFileGlobal.get())
    im=Image.open(imageFileGlobal.get())
    imagenGlobal = im
    #Redimensionamos la imagen
    im=im.resize((widthImage, height_Image), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    print "Cargada!"
    frame.configure(image=img)
    frame.image = img
    
    
def loadSubWindow(frame,algorithm=None):
    
    commandContainer = Label(frame)
    commandContainer.pack(side='left')
    
    imageLoadContainer = Label(commandContainer)
    imageLoadContainer.pack(side='top')
    
    encriptContainer = Label(commandContainer)
    encriptContainer.pack()
    
    textMensageContainer = Label(frame)
    textMensageContainer.pack(side='bottom')
    
    
    widthImage,height_Image = 420,360
    
    #Canvas para cargar al imagen
    im = imagenGlobal
    im=im.resize((widthImage, height_Image), Image.ANTIALIAS)
    
    imgLoaded = ImageTk.PhotoImage(im)
    
    imagePreview = Label(frame, image=imgLoaded)
    imagePreview.image = imgLoaded
    imagePreview.pack(side='right', fill='both', expand='no')
    
#AQUI IBA

    loadFile = Button(imageLoadContainer, text="Load Image", command = lambda: loadImage(imagePreview,algorithm))
    loadFile.pack(side='top')
    
    
    
    #tuto = Label(encriptContainer,text=tutotex[algorithm], width=34)
    #tuto.pack(side='bottom')
    
    
    textInfoField = Label(encriptContainer,textvariable = txt, width=34)
    textInfoField.pack(side='bottom')
        
    textField = Entry(encriptContainer,width=34)
    textField.pack(side='bottom')
    
    keyInfoField = Label(encriptContainer,text="Introduce el mensaje:", width=34)
    keyInfoField.pack(side='bottom')        
        
    if algorithm>0:
        acceptKey = Button(encriptContainer, text="Cargar key", command = lambda: loadKeyfromUser(textKeyField))
        acceptKey.pack(side='bottom')
        
        keyInfoField = Label(encriptContainer,textvariable = key, width=34)
        keyInfoField.pack(side='bottom')
        
        textKeyField = Entry(encriptContainer,textvariable= key,width=34)
        textKeyField.pack(side='bottom')
        
        
        

    

    
    
    
    print "PATH: "+imageFileGlobal.get()
    encriptcButton = Button(encriptContainer, text="Encripta!", command = lambda: encript(textField.get(),algorithm))
    encriptcButton.pack(side='left')
    
    desencriptcButton = Button(encriptContainer, text="Desencripta!", command = lambda: desencript(algorithm))
    desencriptcButton.pack(side='right')
    
    
    
    
    mensageLabel = Label(textMensageContainer,textvariable=mensage, justify=CENTER)
    mensageLabel.pack(side='left')
    
    infoLabel = Label(textMensageContainer,textvariable=info, justify=CENTER)
    infoLabel.pack(side='right')
    
    #botonInfo = Button(encriptContainer, text="Info path", command = getInfo)
    #botonInfo.pack(side='top')
    

#Cargar la GUI del LSB
frameLSB = Frame(notebook)
loadSubWindow(frameLSB,algorithm=0)


#Cargar la GUI del modo LSB-XOR
frameLSBXOR = Frame(notebook)
loadSubWindow(frameLSBXOR,algorithm=1)

#Cargar la GUI del modo 2LSB
frame2LSB = Frame(notebook)
loadSubWindow(frame2LSB,algorithm=2)

#Cargar la GUI del tutorial
frameTuto = Frame(notebook)
tutotitleLabel = Label(frameTuto, text ="Imagenes Esteganograficas - Tutorial")
tutotitleLabel.pack()

tutoLabel = Label(frameTuto,text="")
tutoLabel.pack()

text1="Cada pestana corresponde a un modelo esteganografico analizado en la documentacion.\rPara mas informacion, visita el portal Opera de la Universidad de Sevilla o ponte en contacto con nosotros."
tutoLabel1 = Label(frameTuto,text=text1)
tutoLabel1.pack()


text1 = "\r\tLSB es una tecnica que modifica el bit menos significativo con cada bit del mensaje a cifrar\r\tLSBXOR es una tecnica que  modifica el bit menos significativo del canal verde o azul con\r\tcada bit del mensaje a cifrar segun la operacion xor entre el canal rojo con la clave generada\r\t2LSB es una tecnica que modifica el bit menos significativo de cada canal de color con cada\r\tbit del mensaje a cifrar segun la operacion xor entre el segundo bit menos significativo con\r\tla clave generada"

tutoLabel1 = Label(frameTuto,text=text1)
tutoLabel1.pack()


text1 = "\r\rPASO 1:  Carga la imagen. \r\tSi quieres encriptar un mensaje, pasa al PASO 2. \r\tPor el contrario si quieres desencriptar un mensaje, pasa al PASO 3. \r\rPASO 2:  Escribe en el cuadro de texto el mensaje y dale a encriptar\r\rPASO 3:  Si necesita clave, haz primero el paso 3.1, si no continua.\r\tDale al boton desencriptar\r\rPASO 3.1:  Introducir la clave y pulsar en 'Cargar clave', \r\tLa clave es proporcionada al generar la estegoimagen."

tutoLabel1 = Label(frameTuto,text=text1)
tutoLabel1.pack()


text="Angel Cayetano Gomez Gil & Manuel Jesus Rodriguez Gonzalez\rTrabajo PID : Tecnicas Esteganograficas\rCurso 2013 - 2014"

pieLabel = Label(master,text=text)
pieLabel.pack(side='left')

timeLabel= Label(master,textvariable=time)
timeLabel.pack(side='right')





notebook.add(frameTuto, text='Tutorial')
notebook.add(frameLSB, text='LSB')
notebook.add(frameLSBXOR, text='LSB-XOR')
notebook.add(frame2LSB, text='2LSB')


master.geometry('640x480')
master.mainloop()
