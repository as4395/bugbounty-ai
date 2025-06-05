# Purpose:
# Converts scan findings into a professional bug bounty report using GPT.

import json
from models.llm_helpers.llm_interface import LLMHelper

def load_findings(path='data/processed/findings.json'):
    print(f"[ReportWriter] Loading findings from {path}")
    with open(path, 'r') as f:
        return json.load(f)

def build_prompt(findings):
    print("[ReportWriter] Building prompt for LLM...")
    prompt = "You are a professional bug bounty analyst. Based on the following structured scan results, generate a clear, concise vulnerability report with impacted IPs, services, ports, and risk levels. Use bullet points and markdown formatting.\n\n"
    prompt += json.dumps(findings, indent=2)
    return [{"role": "user", "content": prompt}]

def write_report(findings_path='data/processed/findings.json', output_path='reports/report_llm.md'):
    llm = LLMHelper()
    findings = load_findings(findings_path)
    messages = build_prompt(findings)
    report = llm.chat_completion(messages)
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"[ReportWriter] LLM-generated report saved to {output_path}")

if __name__ == "__main__":
    write_report()
