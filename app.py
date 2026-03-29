import gradio as gr
from llms.llm_engine import debate_func_for_gradio

with gr.Blocks(theme=gr.themes.Monochrome(), css="style.css") as demo:
    gr.HTML("""
    <div class="header-banner">
        <h1 style="display:flex; justify-content:center; align-items:center; gap: 10px;">🧠 ArguGen_AI</h1>
        <h3>AI Debate in Realtime</h3>
        <p>Enter a statement and watch two AI models eloquently debate each other.</p>
    </div>
    """)

    with gr.Row():
        input_box = gr.Textbox(
            label="Debate Topic",
            placeholder="e.g., AI will replace Humans",
            lines=1,
            elem_id="topic-input"
        )

    submit_btn = gr.Button("Start Debate 🚀", variant="primary")

    gr.HTML("<h2 class='arena-title'>🥊 The Debate Arena</h2>")

    with gr.Row():
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div style='color: #60a5fa; border-bottom: 2px solid #3b82f6; padding-bottom: 5px; margin-bottom: 15px; font-weight: bold;'>🔵 In Favor (Opponent A)</div>")
            left_output = gr.HTML()
            
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div style='color: #f87171; border-bottom: 2px solid #ef4444; padding-bottom: 5px; margin-bottom: 15px; font-weight: bold; text-align: right;'>🔴 In Opposition (Opponent B)</div>")
            right_output = gr.HTML()

    judge_output = gr.HTML()

    submit_btn.click(
        fn=debate_func_for_gradio,
        inputs=input_box,
        outputs=[left_output, right_output, judge_output]
    )

if __name__ == "__main__":
    demo.launch()