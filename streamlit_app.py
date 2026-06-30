import streamlit as st
import random
import time

# 1. CONFIGURACIÓN VISUAL (Diseño Oscuro/Gamer Oficial de Astra AI)
st.set_page_config(page_title="Astra AI - Estación de Estudio Absoluta", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    h1 { color: #f59e0b !important; font-family: 'Poppins', sans-serif; font-weight: 800; }
    .stButton>button { 
        background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); 
        color: white !important; 
        border: none; 
        border-radius: 12px; 
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(234, 88, 12, 0.4); }
    .sidebar .sidebar-content { background-color: #070a12 !important; }
    .chat-bubble-user { background-color: #1e1b4b; border: 1px solid #4338ca; padding: 15px; border-radius: 15px 15px 0px 15px; margin-bottom: 10px; }
    .chat-bubble-astra { background-color: #111827; border: 1px solid #1f2937; padding: 15px; border-radius: 15px 15px 15px 0px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE VARIABLES GLOBALES
if "messages" not in st.session_state:
    st.session_state.messages = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
if "modo" not in st.session_state:
    st.session_state.modo = "🧠 Método Aristotélico (Pistas)"
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = ""

# Banco de preguntas interno para que funcione al tiro gratis sin APIs
BANCO_PREGUNTAS = {
    "Matemáticas": [
        {"p": "¿Cómo resolverías la ecuación 2x + 5 = 15? ¿Qué pasarías haciendo primero con ese 5?", "r": "restar"},
        {"p": "Si tenemos un triángulo rectángulo y sus catetos miden 3 y 4, ¿cómo encontramos la hipotenusa usando Pitágoras?", "r": "raiz"},
        {"p": "Si una torta se divide en 8 partes y te comes 3, ¿qué fracción de la torta te queda?", "r": "5/8"}
    ],
    "Física": [
        {"p": "Un auto frena bruscamente y los pasajeros se van hacia adelante. ¿Qué ley de Newton explica esto por la resistencia al cambio de movimiento?", "r": "inercia"},
        {"p": "Si dejas caer una pelota de tenis y una piedra gigante al mismo tiempo en el vacío, ¿cuál llega primero al suelo?", "r": "iguales"},
        {"p": "La fórmula de la fuerza es Masa multiplicada por...", "r": "aceleracion"}
    ],
    "Química": [
        {"p": "¿Cuál es el componente o elemento químico más abundante en el universo entero?", "r": "hidrogeno"},
        {"p": "Si mezclamos agua con sal, ¿cuál de los dos actúa como el soluto en esta solución?", "r": "sal"},
        {"p": "El pH del agua pura es 7. Si le agregamos jugo de limón, ¿el pH sube o baja?", "r": "baja"}
    ],
    "Inglés": [
        {"p": "¿Cómo se dice correctamente en inglés: 'Yo tengo quince años'? Cuidado con el verbo.", "r": "i am"},
        {"p": "¿Cuál es el pasado del verbo irregular 'GO'?", "r": "went"},
        {"p": "Traduce la palabra 'Unforgettable' al español.", "r": "inolvidable"}
    ]
}

# 3. BARRA LATERAL (Panel de Control)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 35px;'>🪐 ASTRA AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Edición Absoluta Multimodal</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown(f"### 🏆 Nivel Actual: **{st.session_state.nivel}**")
    st.progress(st.session_state.xp / 100)
    st.markdown(f"🌟 **{st.session_state.xp} / 100 XP** para el siguiente rango.")
    st.write("---")
    
    st.markdown("### 📚 Configuración de Estudio")
    materia = st.selectbox("Selecciona tu asignatura:", ["Matemáticas", "Física", "Química", "Inglés"])
    modo_seleccionado = st.radio("Herramientas Astra:", [
        "🧠 Método Aristotélico (Pistas)",
        "🗣️ AI Oral Exam (Modo Quiz)",
        "📇 Generador de Flashcards y Resumen"
    ])
    
    if modo_seleccionado != st.session_state.modo:
        st.session_state.modo = modo_seleccionado
        st.session_state.messages = []
        st.session_state.pregunta_actual = ""
        st.rerun()

    st.write("---")
    if st.button("🧹 Reiniciar Pizarra"):
        st.session_state.messages = []
        st.session_state.xp = 0
        st.session_state.nivel = 1
        st.session_state.pregunta_actual = ""
        st.rerun()

# 4. INTERFAZ PRINCIPAL DE CHAT
st.write(f"### ⚡ Canal activo: `{st.session_state.modo}` en `{materia}`")

if len(st.session_state.messages) == 0:
    if st.session_state.modo == "🧠 Método Aristotélico (Pistas)":
        bienvenida = f"¡Wena! Soy tu tutor de Astra AI. Ponme cualquier ejercicio o duda de **{materia}** que tengas. ¿Qué problema resolvemos?"
    elif st.session_state.modo == "🗣️ AI Oral Exam (Modo Quiz)":
        pregunta = random.choice(BANCO_PREGUNTAS[materia])
        st.session_state.pregunta_actual = pregunta
        bienvenida = f"🚀 ¡Iniciamos el Examen Oral de **{materia}**! Prepárate:\n\n**{pregunta['p']}**"
    else:
        bienvenida = f"📇 ¡Selector de Materiales activado! Escribe el tema de **{materia}** para armarte tarjetas de memoria y un resumen pro."
    
    st.session_state.messages.append({"role": "astra", "content": bienvenida})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>🧔 Tú:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-astra'><b>🤖 Astra:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# 5. LOGICA INTERACTIVA DE RESPUESTAS
if user_input := st.chat_input("Escribe tu duda o respuesta aquí..."):
    st.markdown(f"<div class='chat-bubble-user'><b>🧔 Tú:</b><br>{user_input}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Astra analizando..."):
        time.sleep(1)
        
        if st.session_state.modo == "🧠 Método Aristotélico (Pistas)":
            respuesta_astra = f"¡Buena pregunta! Respecto a lo que planteas sobre **{materia}**, tu enfoque va bien encaminado. Pero para no arruinarte el aprendizaje, analicemos este detalle: ¿qué pasa si aplicas el concepto base primero? Cuéntame qué crees que se debería hacer en ese primer paso."
        
        elif st.session_state.modo == "🗣️ AI Oral Exam (Modo Quiz)":
            solucion_correcta = st.session_state.pregunta_actual["r"]
            
            if solucion_correcta in user_input.lower():
                st.session_state.xp += 35
                if st.session_state.xp >= 100:
                    st.session_state.xp = 0
                    st.session_state.nivel += 1
                    st.toast("🎉 ¡SUBISTE DE NIVEL CAMPEÓN!", icon="🔥")
                
                nueva_pregunta = random.choice(BANCO_PREGUNTAS[materia])
                st.session_state.pregunta_actual = nueva_pregunta
                respuesta_astra = f"¡Excelente! Le achuntaste medio a medio. Te ganaste **+35 XP**. 🏆\n\nPasemos al siguiente desafío de **{materia}**:\n\n**{nueva_pregunta['p']}**"
            else:
                respuesta_astra = f"Buen intento, pero no va por ahí el concepto exacto. Te doy una pista: se relaciona directamente con lo que empieza con la letra '{solucion_correcta[0]}'. ¡Piénsala bien!"
        
        else:
            respuesta_astra = f"✨ ¡Material de repaso completado para **{materia}**!\n\n### 📇 Flashcards:\n1. **Pregunta:** ¿Cuál es la regla principal? \n   *Respuesta:* Estudiar por partes.\n2. **Pregunta:** ¿Qué error común se comete? \n   *Respuesta:* Memorizar todo sin entender.\n\n### 📜 Resumen Pro:\n• El núcleo de {user_input} se basa en dominar las bases.\n• Repasa las guías anteriores para asegurar el 7.0."

        st.markdown(f"<div class='chat-bubble-astra'><b>🤖 Astra:</b><br>{respuesta_astra}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "astra", "content": respuesta_astra})
        st.rerun()
        