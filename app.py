import os
import gradio as gr
from llms.llm_engine import debate_func_for_gradio

def format_debate_func(statement):
    for a_accumulated, b_accumulated, j_text, a_aud, b_aud, j_aud in debate_func_for_gradio(statement):
        # Prepare plain text for each side, joined by double newlines for separation
        a_text = "\n\n".join([v.strip() for v in a_accumulated if v.strip()])
        b_text = "\n\n".join([v.strip() for v in b_accumulated if v.strip()])
        j_text_clean = ""
        if j_text and j_text.strip():
            j_text_clean = j_text.replace("Judgement: \n", "").replace("Judgement:\n", "").strip()
        yield (
            a_text,
            b_text,
            j_text_clean,
            a_aud if a_aud is not None else gr.skip(),
            b_aud if b_aud is not None else gr.skip(),
            j_aud if j_aud is not None else gr.skip()
        )


css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    custom_css = f.read()


with gr.Blocks(theme=gr.themes.Monochrome(), css=custom_css) as demo:
    gr.HTML("""
    <div class="header-banner">
        <div class="header-icon">🧠</div>
        <h1>ArguGen<span class="highlight">_AI</span></h1>
        <h3>AI-Powered Real-Time Debate Arena</h3>
        <p>Enter a statement and watch two AI models engage in an eloquent real-time debate.</p>
    </div>
    """)

    with gr.Row():
        input_box = gr.Textbox(
            label="💬 Debate Topic",
            placeholder="e.g., AI will replace Humans",
            lines=1,
            elem_id="topic-input"
        )

    submit_btn = gr.Button("⚡ Start Debate", variant="primary", elem_id="start-btn")

    gr.HTML("""
    <div class="arena-title-wrapper">
        <div class="arena-divider"></div>
        <h2 class="arena-title">🥊 The Debate Arena</h2>
        <div class="arena-divider"></div>
    </div>
    """)

    with gr.Row(elem_classes="debate-arena"):
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header favor-col-header'><span class='col-dot green-dot'></span> In Favor <span class='column-tag'>(Opponent A)</span></div>")
            left_output = gr.HTML(elem_id="favor-output")
            left_audio = gr.Audio(autoplay=True)

        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header opposition-col-header'><span class='col-dot red-dot'></span> In Opposition <span class='column-tag'>(Opponent B)</span></div>")
            right_output = gr.HTML(elem_id="opposition-output")
            right_audio = gr.Audio(autoplay=True)

    judge_output = gr.HTML(elem_id="judge-output")
    judge_audio = gr.Audio(autoplay=True)

    submit_btn.click(
        fn=format_debate_func,
        inputs=input_box,
        outputs=[left_output, right_output, judge_output, left_audio, right_audio, judge_audio]
    )

if __name__ == "__main__":
    demo.launch()