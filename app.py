import os
import html as html_mod
import gradio as gr
from llms.llm_engine import debate_func_for_gradio


# ── HTML Card Builders ──────────────────────────────────────

def build_single_card(text, is_streaming, card_class, icon, round_num):
    """Builds a single round card HTML. Only the active card gets updated."""
    if text is None:
        return ""
        
    content = text.strip()
    # Replace newlines for HTML
    safe_content = html_mod.escape(content).replace("\n", "<br>")
    
    current_class = f"round-card {card_class} streaming" if is_streaming else f"round-card {card_class}"
    badge_style = "" if is_streaming else ' style="display: none; visibility: hidden;"'
    
    if is_streaming:
        content_html = f'<span class="text-content">{safe_content}</span><span class="typing-indicator"></span>'
    else:
        content_html = f'<span class="text-content">{safe_content}</span>'

    return f'''
<div class="{current_class}">
    <div class="round-header">
        <span class="round-title">{icon} Round {round_num}</span>
        <span class="streaming-badge"{badge_style}>● LIVE</span>
    </div>
    <div class="round-content">
        {content_html}
    </div>
</div>'''


def build_judge_card(judge_text):
    """Wrap judge output in a premium verdict card."""
    if not judge_text or not judge_text.strip():
        return ""
    safe = html_mod.escape(judge_text.strip()).replace("\n", "<br>")
    return f'''
<div class="judge-card">
    <div class="judge-title">⚖️ The Verdict</div>
    <div class="judge-content">{safe}</div>
</div>'''


# ── Formatting wrapper ──────────────────────────────────────

def format_debate_func(statement, favor_model, opp_model):
    """
    Consumes the generator from the backend and yields structured HTML.
    Crucially, it uses gr.skip() for components that have not changed,
    drastically reducing payload size and preventing previous UI components
    from flickering or re-rendering.
    """
    
    last_htmls = [""] * 7
    
    # Reset all components to empty
    yield (
        "", "", "",  # Favor rounds
        "", "", "",  # Opp rounds
        "",          # Judge
        None, None, None
    )

    for active_side, active_round, a_accum, b_accum, j_text, a_aud, b_aud, j_aud in debate_func_for_gradio(statement, favor_model, opp_model):
        outputs = []
        
        # 1. Favor Cards (0, 1, 2)
        for i in range(3):
            if i < len(a_accum):
                is_stream = (active_side == "A" and active_round == i)
                html = build_single_card(a_accum[i], is_stream, "favor-card", "🟢", i + 1)
                if html != last_htmls[i]:
                    outputs.append(html)
                    last_htmls[i] = html
                else:
                    outputs.append(gr.skip())
            else:
                outputs.append(gr.skip())
                
        # 2. Opposition Cards (3, 4, 5)
        for i in range(3):
            if i < len(b_accum):
                is_stream = (active_side == "B" and active_round == i)
                html = build_single_card(b_accum[i], is_stream, "opposition-card", "🔴", i + 1)
                idx = i + 3
                if html != last_htmls[idx]:
                    outputs.append(html)
                    last_htmls[idx] = html
                else:
                    outputs.append(gr.skip())
            else:
                outputs.append(gr.skip())

        # 3. Judge Card (6)
        if j_text:
            j_clean = j_text.replace("Judgement: \n", "").replace("Judgement:\n", "").strip()
            html = build_judge_card(j_clean)
            if html != last_htmls[6]:
                outputs.append(html)
                last_htmls[6] = html
            else:
                outputs.append(gr.skip())
        else:
            outputs.append(gr.skip())
            
        # 4. Audio (7, 8, 9)
        outputs.append(a_aud if a_aud is not None else gr.skip())
        outputs.append(b_aud if b_aud is not None else gr.skip())
        outputs.append(j_aud if j_aud is not None else gr.skip())
        
        yield tuple(outputs)


# ── Load external CSS ──────────────────────────────────────

css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    custom_css = f.read()

# ── Gradio UI ───────────────────────────────────────────────

model_options = ["mistral:7b", "deepseek-r1:8b", "llama3.1:8b", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]

with gr.Blocks(theme=gr.themes.Monochrome(), css=custom_css) as demo:

    # ─ Header
    gr.HTML("""
    <div class="header-banner">
        <div class="header-icon">🧠</div>
        <h1>ArguGen<span class="highlight">_AI</span></h1>
        <h3>AI-Powered Real-Time Debate Arena</h3>
        <p>Enter a statement and watch two AI models engage in an eloquent real-time debate.</p>
    </div>
    """)

    # ─ Input & Model Selection
    with gr.Row():
        input_box = gr.Textbox(
            label="💬 Debate Topic",
            placeholder="e.g., AI will replace Humans",
            lines=1,
            elem_id="topic-input",
            scale=3
        )
        favor_model_drop = gr.Dropdown(
            choices=model_options,
            value="gpt-4o-mini",
            label="Favorable Model (OpenAI or Ollama)",
            scale=1
        )
        opp_model_drop = gr.Dropdown(
            choices=model_options,
            value="mistral:7b",
            label="Opposition Model (OpenAI or Ollama)",
            scale=1
        )

    submit_btn = gr.Button("⚡ Start Debate", variant="primary", elem_id="start-btn")

    # ─ Arena title
    gr.HTML("""
    <div class="arena-title-wrapper">
        <div class="arena-divider"></div>
        <h2 class="arena-title">🥊 The Debate Arena</h2>
        <div class="arena-divider"></div>
    </div>
    """)

    # ─ Audio players row
    with gr.Row(elem_classes="audio-controls-row"):
        with gr.Column(min_width=0):
            gr.HTML("<div class='audio-label favor-audio-label'>🎧 Favor Voice</div>")
            left_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact")
        with gr.Column(min_width=0):
            gr.HTML("<div class='audio-label opposition-audio-label'>🎧 Opposition Voice</div>")
            right_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact")

    # ─ Debate columns (Discrete statically mounted HTML cards)
    with gr.Row(elem_classes="debate-arena"):
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header favor-col-header'><span class='col-dot green-dot'></span> In Favor <span class='column-tag'>(Opponent A)</span></div>")
            favor_cards = [gr.HTML(elem_id=f"f-card-{i}") for i in range(3)]

        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header opposition-col-header'><span class='col-dot red-dot'></span> In Opposition <span class='column-tag'>(Opponent B)</span></div>")
            opp_cards = [gr.HTML(elem_id=f"o-card-{i}") for i in range(3)]

    # ─ Judge section
    judge_output = gr.HTML(elem_id="judge-output")
    judge_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact judge-audio-player")

    # ─ Output Lists mapping
    all_outputs = favor_cards + opp_cards + [judge_output, left_audio, right_audio, judge_audio]

    # Disable inputs during generation
    interactive_components = [submit_btn, input_box, favor_model_drop, opp_model_drop]

    def disable_inputs():
        return [gr.update(interactive=False)] * len(interactive_components)

    def enable_inputs():
        return [gr.update(interactive=True)] * len(interactive_components)

    # ─ Wire it up
    debate_event = submit_btn.click(
        fn=disable_inputs,
        outputs=interactive_components
    ).then(
        fn=format_debate_func,
        inputs=[input_box, favor_model_drop, opp_model_drop],
        outputs=all_outputs,
    ).then(
        fn=enable_inputs,
        outputs=interactive_components
    )

if __name__ == "__main__":
    demo.launch()