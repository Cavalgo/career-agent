from career_agent import chat
import gradio as gr

if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat,
        type="messages",
        title="Agente de carrera de Carlos Vallejo",
        description="Pregúntame sobre la experiencia, habilidades y proyectos de Carlos.",
    ).launch(share=True)

# cd app
# uv run gradio deploy
# python3 main.py

# mkdir my_new_gradio_app
# cd my_new_gradio_app
# uv venv      # creates .venv folder
# source .venv/bin/activate
# uv add gradio openai
