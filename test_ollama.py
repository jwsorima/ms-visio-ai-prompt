from http.client import HTTPResponse
import urllib.request
import json
from typing import Dict, Any
from vsdx_parser import extract_vsdx_details

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

def insert_vsdx_data(parsed_details: str) -> Dict[str, Any]:
  return {
    # "model": "llama3.2",
    "model": "deepseek-r1:14b",
    "prompt": f"""
      Forget all details that I sent you before this prompt

      {parsed_details}

      These are data extracted from a VSDX file. Can you understand what the diagram represents?
      Can you understand the flow of diagram based on their positions and not rely on connectors reference?
      Also give me a step by step process listed by numbers.
    """,
    # "prompt": f"""
    #   Forget all details that I sent you before this prompt

    #   {parsed_details}

    #   These are data extracted from a VSDX file. Can you understand what the diagram represents?

    #   I need two outputs:

    #   Step-by-Step Process in sentence:
    #     Provide a step-by-step process listed by numbers.
    #     If a condition causes a loop back, state: Loops back to "[That part]", e.g., (Loops back to "[Development & User Testing]").
    #     DO NOT include IDs or extra explanations.
    #     Enclose all text inside shapes within [brackets].

    #   And

    #   Python Implementation:
    #     Provide a Python implementation that follows this process exactly.
    #     Use while loops for repetition and if conditions for checks.
    #     The Python code must be logically correct.
    #     DO NOT include comments or formatting syntax; return only plain Python code.
    # """,
    "stream": True
  }

def prompt_ai_with_vsdx_data(file_path: str) -> HTTPResponse:
  parsed_details = extract_vsdx_details(file_path)
  data = insert_vsdx_data(parsed_details)
  json_data = json.dumps(data).encode("utf-8")

  req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

  return urllib.request.urlopen(req)

def _main():
  file_path = "docs/Drawing2.vsdx"
  parsed_details = extract_vsdx_details(file_path)
  print(parsed_details)
  data = insert_vsdx_data(parsed_details)
  json_data = json.dumps(data).encode("utf-8")

  req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")

  with urllib.request.urlopen(req) as response:
    for line in response:
      if line:
        line_data = line.decode("utf-8").strip()
        if line_data:
          try:
            json_line = json.loads(line_data)
            print(json_line.get("response", ""), end="", flush=True)
          except json.JSONDecodeError:
            pass

if __name__ == "__main__":
  _main()