# Purpose:
# Summarize lengthy bug bounty data or reports using GPT.

from models.llm_helpers.llm_interface import LLMHelper

def summarize_text(text, context="Summarize this for a bug bounty analyst"):
    """
    Uses OpenAI GPT to generate a concise summary of the provided text.
    """
    llm = LLMHelper()
    print("[Summarizer] Sending input to LLM...")
    
    messages = [
        {"role": "system", "content": "You are a security analyst who summarizes content clearly and accurately."},
        {"role": "user", "content": f"{context}\n\n{text}"}
    ]
    
    return llm.chat_completion(messages)

def summarize_file(input_path, output_path):
    """
    Reads a file, summarizes its contents using LLM, and writes the summary to another file.
    """
    print(f"[Summarizer] Reading input from: {input_path}")
    with open(input_path, 'r') as infile:
        raw_text = infile.read()

    summary = summarize_text(raw_text)

    print(f"[Summarizer] Writing summary to: {output_path}")
    with open(output_path, 'w') as outfile:
        outfile.write(summary)

    print("[Summarizer] Done.")

if __name__ == "__main__":
    summarize_file('reports/report.txt', 'reports/report_summary.txt')
