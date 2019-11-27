import tkinter as tk
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

conversaciones = [
    "hola como estas",
    "Como estas",
    "Que andas haciendo",
    "Bien y tu",
    "Hola amigo mio"
]

respuestas = [
    "Estoy super bien",
    "y tu que tal andas amigo",
    "yo soy un boot",
    "deja tu mensaje por ahora",
    "puedo leer tu mensaje"
]
chatbot = ChatBot('LimbertBoot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
logic_adapters=[
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'Lo siento, No conozco esa palabra.',
    },
    {
        'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        'input_text': 'Help me!',
        'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org',
        'maximum_similarity_threshold': 0.90
    }
])

trainer = ListTrainer(chatbot)

#Clase de la interfaz grafica GUI
class interface:
    #Constructor recibe un objeto de tipo ventana
    def __init__(self, ventana):
        #self es un parametro obligatorio tipo puntero
        self.ventana = ventana
        #le damos un tamaño a la ventana
        ventana.geometry('1200x600')
        #Configuramos el color de fondo de la ventana
        ventana.configure(bg='black')
        ventana.columnconfigure(1, weight=1)
        #Ponemos un titulo a la ventana
        ventana.title("Entrenando a tu boot")
        self.components_trainer(ventana)
        self.components_chat(ventana)
        self.components_list_trainer(ventana)
        self.conty = 0
        self.contb = 1

        trainer.train(respuestas)
    #Metodo encargado de crear los componentes de la GUI
    #como parametro recibe la pantalla donde se pondran los componentes
    def components_trainer(self, ventana):
        self.frame1 = tk.Frame(ventana, bg="white", height=1200, width=400 )
        self.frame1.grid(row=0, column=1, sticky="e,w,s,n")
        self.frame1.grid_propagate(False)
        #cremos una variable que contentra el objeto de tipo Label
        #como parametro recibe la ventana donde se posicionara y el texto
        self.lblSaludo = tk.Label(self.frame1, text="ENTRENANDO A TU BOOT", height="3", bg="white")
        #enpaquetamos el objeto label
        self.lblSaludo.grid(row=0, column=1)

        self.lblPregunta = tk.Label(self.frame1, text="Pregunta :")
        # enpaquetamos el objeto label
        self.lblPregunta.grid(row=2, column=0, pady=15)
        self.txtPregunta = tk.Entry(self.frame1, textvariable=tk.IntVar, width="50", relief="sunken", bd=3)
        self.txtPregunta.grid(row=2, column=1, pady=15, padx=10)

        self.lblRespuesta = tk.Label(self.frame1, text="Respuesta :")
        # enpaquetamos el objeto label
        self.lblRespuesta.grid(row=3, column=0, pady=15)
        self.txtRespuesta = tk.Entry(self.frame1, textvariable=tk.IntVar, width="50", relief="sunken", bd=3)
        self.txtRespuesta.grid(row=3, column=1, pady=15, padx=10)

        self.btnSaludo = tk.Button(self.frame1, text="Entrenar", fg="white", bg="lime", width="20", command=self.add_json)
        self.btnSaludo.grid(row=4, column=1, pady=15)

    def components_chat(self, ventana):
        self.frame2 = tk.Frame(ventana, bg="green", height=1200, width=400)
        self.frame2.grid(row=0, column=2, sticky="e,w,s,n")
        self.frame2.grid_propagate(False)

        self.panelChat = tk.Frame(self.frame2, height=500, width=370)
        self.panelChat.grid(row=0, column=0, pady=15, padx=15)
        self.panelChat.grid_propagate(False)

        self.panelSend = tk.Frame(self.frame2, height=50, width=370)
        self.panelSend.grid(row=1, column=0, pady=15, padx=15)
        self.panelSend.grid_propagate(False)

        self.txtMensaje = tk.Entry(self.panelSend, textvariable=tk.IntVar, width="43", relief="sunken", bd=3)
        self.txtMensaje.grid(row=12, column=0, pady=10, padx=5)

        self.btnEnviar = tk.Button(self.panelSend, text="Enviar", fg="white", bg="lime", width="10", command=self.send_message)
        self.btnEnviar.grid(row=12, column=1, pady=10, padx=5)

    def components_list_trainer(self, ventana):
        self.frame3 = tk.Frame(ventana, bg="white", height=1200, width=400)
        self.frame3.grid(row=0, column=3, sticky="e,w,s,n")
        self.frame3.grid_propagate(False)
        self.lblPreguntas = tk.Label(self.frame3, text="Preguntas")
        self.lblPreguntas.grid(row=0, column=0)
        self.lblRespuestas = tk.Label(self.frame3, text="Respuestas")
        self.lblRespuestas.grid(row=0, column=1)
        self.lstPreguntas = tk.Listbox(self.frame3, height=100, width=35)
        self.lstPreguntas.grid(row=1, column=0)
        self.lstPreguntas.insert(0, *conversaciones)
        self.lstRespuestas = tk.Listbox(self.frame3, height=100, width=35)
        self.lstRespuestas.grid(row=1, column=1)
        self.lstRespuestas.insert(0, *respuestas)

    def send_message(self):
        self.lblmy = tk.Label(self.panelChat, text=self.txtMensaje.get())
        self.lblmy.grid(row=self.conty, column=0)
        trainer.train(respuestas)
        print(respuestas)
        response = chatbot.get_response(self.txtMensaje.get())
        self.lblbot = tk.Label(self.panelChat, text=response)
        self.lblbot.grid(row=self.contb, column=1)
        self.txtMensaje.delete(0, last='end')
        self.conty = self.conty + 2
        self.contb = self.contb + 2

    def add_json(self):
        conversaciones.append(self.txtPregunta.get())
        respuestas.append(self.txtRespuesta.get())
        self.lstPreguntas.delete(0, self.lstPreguntas.size())
        self.lstPreguntas.insert(0, *conversaciones)
        self.lstRespuestas.delete(0, self.lstRespuestas.size())
        self.lstRespuestas.insert(0, *respuestas)
        self.txtPregunta.delete(0, last='end')
        self.txtRespuesta.delete(0, last='end')

    def trains(self, mensaje):
        #Obtenemos el string de lo que se escribio en el campo de texto
        #self.lblSaludo.configure({'text': self.txtNombreT})

        return "fewfe"

root = tk.Tk()
miVentana = interface(root)
root.mainloop()





