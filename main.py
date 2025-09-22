from career_agent import chat
import gradio as gr

if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        type="messages",
        title="Agente de carrera de Carlos Vallejo",
        description="Pregúntame sobre la experiencia, habilidades y proyectos de Carlos.",
    ).launch()