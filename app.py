import gradio as gr
from llms.llm_engine import debate_func_for_gradio

def format_debate_func(statement):
    for a_text, b_text, j_text, a_aud, b_aud, j_aud in debate_func_for_gradio(statement):
        def format_blocks(text, side="favor"):
            rounds = text.split("\n\n")
            html = ""
            for i, r in enumerate(rounds):
                if r.strip():
                    html += f"<div class='round-card {side}-card'><div class='round-card-title {side}-title'>Round {i+1}</div><div class='round-card-content {side}-content'>{r}</div></div>"
            return html
        
        a_html = format_blocks(a_text, "favor")
        b_html = format_blocks(b_text, "opposition")
        
        j_html = ""
        if j_text and j_text.strip():
            clean_j = j_text.replace("Judgement: \n", "").replace("Judgement:\n", "").strip()
            j_html = f"<div class='judge-card'><div class='judge-title'>⚖️ The Verdict</div><div class='judge-content'>{clean_j}</div></div>"
            
        yield a_html, b_html, j_html, a_aud, b_aud, j_aud

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
            left_audio = gr.Audio(autoplay=True)
        
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div style='color: #f87171; border-bottom: 2px solid #ef4444; padding-bottom: 5px; margin-bottom: 15px; font-weight: bold; text-align: right;'>🔴 In Opposition (Opponent B)</div>")
            right_output = gr.HTML()
            right_audio = gr.Audio(autoplay=True)

    judge_output = gr.HTML()
    judge_audio = gr.Audio(autoplay=True)

    submit_btn.click(
        fn=format_debate_func,
        inputs=input_box,
        outputs=[left_output, right_output, judge_output, left_audio, right_audio, judge_audio]
    )

if __name__ == "__main__":
    demo.launch()