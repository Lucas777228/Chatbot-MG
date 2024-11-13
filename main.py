import streamlit as st #importar la libreria
from groq import Groq #? NUEVA IMPORTACIÓN

#configuración de la ventana de la web
st.set_page_config(page_title = "Chat de IA", page_icon= "💻")

#Titulo de la pagina
st.title("Aplicación con Streamlit")

#Ingreso de dato del usuario
nombre = st.text_input("¿Cuál es tu nombre?")

#Creamos boton con funcionalidad
if st.button("Saludar") :
    st.write(f"¡Hola {nombre}! Gracias por venir a Talento Tech")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conecta a la API, crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #obteniendo la clave de nuestro archivo
    return Groq(api_key = clave_secreta) #crea al usuario

#cliente = usuario de groq | modelo es la Ia seleccionada | mensaje del usuario
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

 #-> Simula un historial de mensajes
def inicializar_estado():
    #Si "mensajes" no esta en st,session_state
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
    #El metodo apped() agrega un elemento a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : 
            st.markdown(mensaje["content"])
#Contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #agrupamos los mensajes en el area del chat
    with contenedorDelChat : mostrar_historial()

def configurar_pagina():
    st.title("chat de IA") #Titulo
    st.sidebar.title("Configuración") #Menu lateral
    elegirModelo = st.sidebar.selectbox(
        "Elegí un modulo", #titulo
        MODELO, #Opciones del menu
        index = 2 #valorDefecto
    )
    return elegirModelo

def generar_respuestas(chat_completo):
    respuesta_completa = "" #texto vacio
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa    

def main(): #función principal
    #invocación de funciones
    modelo = configurar_pagina() #Llamamos a la función
    clienteUsuario = crear_usuario_groq()
    inicializar_estado() #llama a la función historial
    area_chat() # creanos el sector para ver los mensajes
    mensaje = st.chat_input("Escribí un mensaje...")

    #verificar si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "🧙‍♂️") #visualizamos el msg del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

#indicamos que nuetra función principal es main()
if __name__ == "__main__":
    main()