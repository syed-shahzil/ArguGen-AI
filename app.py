import os
import html as html_mod
import gradio as gr
from llms.llm_engine import debate_func_for_gradio


# ── HTML Card Builders ──────────────────────────────────────

def build_round_cards(accumulated_list, card_class, icon):
    """Convert a list of round texts into stacked HTML round-cards.

    Each entry in `accumulated_list` is the text for one round.
    The FULL html for ALL rounds is rebuilt every call so that
    previous rounds are never lost.
    """
    cards_html = ""
    for i, text in enumerate(accumulated_list):
        content = text.strip()
        if not content:
            # Round is still streaming — show a placeholder pulse
            cards_html += f'''
<div class="round-card {card_class} streaming">
    <div class="round-header">
        <span class="round-title">{icon} Round {i + 1}</span>
        <span class="streaming-badge">● LIVE</span>
    </div>
    <div class="round-content">
        <span class="typing-indicator"></span>
    </div>
</div>'''
            continue

        # Escape any raw HTML in the LLM output, then convert newlines
        safe_content = html_mod.escape(content).replace("\n", "<br>")
        cards_html += f'''
<div class="round-card {card_class}">
    <div class="round-header">
        <span class="round-title">{icon} Round {i + 1}</span>
    </div>
    <div class="round-content">{safe_content}</div>
</div>'''
    return cards_html


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

def format_debate_func(statement):
    """Consume the generator from the backend and yield structured HTML
    cards + audio components.  Every yield rebuilds the FULL card HTML
    so that Gradio's gr.HTML replacement semantics never lose content."""

    for a_accumulated, b_accumulated, j_text, a_aud, b_aud, j_aud in debate_func_for_gradio(statement):
        favor_html = build_round_cards(a_accumulated, "favor-card", "🟢")
        opposition_html = build_round_cards(b_accumulated, "opposition-card", "🔴")

        j_text_clean = ""
        if j_text and j_text.strip():
            j_text_clean = j_text.replace("Judgement: \n", "").replace("Judgement:\n", "").strip()
        judge_html = build_judge_card(j_text_clean)

        yield (
            favor_html,
            opposition_html,
            judge_html,
            a_aud if a_aud is not None else gr.skip(),
            b_aud if b_aud is not None else gr.skip(),
            j_aud if j_aud is not None else gr.skip(),
        )


# ── Load external CSS ──────────────────────────────────────

css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    custom_css = f.read()


# ── Gradio UI ───────────────────────────────────────────────

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

    # ─ Input
    with gr.Row():
        input_box = gr.Textbox(
            label="💬 Debate Topic",
            placeholder="e.g., AI will replace Humans",
            lines=1,
            elem_id="topic-input",
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

    # ─ Audio players row (isolated from debate cards to prevent re-render issues)
    with gr.Row(elem_classes="audio-controls-row"):
        with gr.Column(min_width=0):
            gr.HTML("<div class='audio-label favor-audio-label'>🎧 Favor Voice</div>")
            left_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact")
        with gr.Column(min_width=0):
            gr.HTML("<div class='audio-label opposition-audio-label'>🎧 Opposition Voice</div>")
            right_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact")

    # ─ Debate columns (HTML only — no audio here)
    with gr.Row(elem_classes="debate-arena"):
        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header favor-col-header'><span class='col-dot green-dot'></span> In Favor <span class='column-tag'>(Opponent A)</span></div>")
            left_output = gr.HTML(elem_id="favor-output")

        with gr.Column(elem_classes="scrollable-column"):
            gr.HTML("<div class='column-header opposition-col-header'><span class='col-dot red-dot'></span> In Opposition <span class='column-tag'>(Opponent B)</span></div>")
            right_output = gr.HTML(elem_id="opposition-output")

    # ─ Judge section
    judge_output = gr.HTML(elem_id="judge-output")
    judge_audio = gr.Audio(autoplay=True, elem_classes="audio-player-compact judge-audio-player")

    # ─ Wire it up
    submit_btn.click(
        fn=format_debate_func,
        inputs=input_box,
        outputs=[left_output, right_output, judge_output, left_audio, right_audio, judge_audio],
    )

if __name__ == "__main__":
    demo.launch()