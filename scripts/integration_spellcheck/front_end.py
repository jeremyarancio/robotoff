import gradio as gr

from .back_end import next_annotation, submit_correction, diff_texts


# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Ingredients Spellcheck 🍊")
    
    insight_id = gr.Textbox(
        label="Insight Id",
        interactive=False,
        visible=False,
    )

    original_text = gr.Textbox(
        label="Original Text (Uneditable)",
        info="This is the original text.",
        interactive=False,  # Make this text box uneditable
        lines=3
    )
    
    corrected_text = gr.Textbox(
        label="Corrected Text (Editable)",
        info="This is the AI-corrected text. You can modify it.",
        interactive=True,  # Make this text box editable
        lines=3
    )
    
    # Diff Display using HighlightedText
    diff_display = gr.HighlightedText(
        label="Difference Between Original and Corrected Text",
        combine_adjacent=True,
        show_legend=True,
        color_map={"+": "green", "-": "red"}  # "+" for inserted text, "-" for deleted text
    )
    
    # Validate button to move to next annotation
    with gr.Row():
        validate_button = gr.Button("Validate")
        skip_button = gr.Button("Skip")
    
    # Define action when validate button is clicked
    validate_button.click(
        submit_correction,  # Function to handle submission
        inputs=[insight_id, original_text, corrected_text],  # Original and edited texts as inputs
        outputs=[insight_id, original_text, corrected_text]  # Load next pair of texts
    )

    skip_button.click(
        next_annotation,  # Function to handle submission
        inputs=[],  # Original and edited texts as inputs
        outputs=[insight_id, original_text, corrected_text]  # Load next pair of texts
    )
    
    # Update diff display dynamically when corrected text is modified
    corrected_text.change(
        diff_texts,  # Call diff function
        inputs=[original_text, corrected_text],  # Compare original and corrected texts
        outputs=diff_display  # Update diff display
    )
    
    # Load the first set of texts when the demo starts
    demo.load(next_annotation, inputs=[], outputs=[insight_id, original_text, corrected_text])
