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
    "model": "llama3.1:8b",
    "prompt": f"""
      Analyze the following JSON data extracted from a VSDX file representing a process flow diagram.

      {parsed_details}

      ### **Step 1: Identify All Major Process Steps**
      - Extract all **process-related shapes** (e.g., Hexagon, Process, Unknown with meaningful text).
      - Order them **top-to-bottom (descending Y-coordinates)** to infer flow.
      - Classify each shape into **Process, Decision, Validation, or Output**.
      - Clearly define what role each plays in the process.

      ### **Step 2: Determine Explicit and Inferred Logical Connections**
      - Identify **explicit connections** (direct "From" and "To" links).
      - For **missing connections**, infer the most logical flow based on:
        - **Vertical proximity** (closer Y-values suggest sequential steps).
        - **Shape type** (Process → Decision → Verification → Next Process).
        - **Contextual meaning** (e.g., "Verify" steps should follow cycle-setting steps).
      - Mark where **flow diverges into branches** (decision points).
      - Identify where **separate paths converge back into a single sequence**.

      ### **Step 3: Infer & Validate Missing Links**
      - Check if any shape **has no incoming or outgoing connections** and logically determine its place in the sequence.
      - Ensure that **all decisions** flow **back into the main path**.
      - If **steps are missing** but needed for logical continuity, explicitly state **the inferred transitions**.

      ### **Step 4: Generate the Fully Structured Workflow**
      - Output a **clear, numbered step-by-step process** that follows the inferred workflow.
      - Ensure **each transition is justified** and properly connected.
      - Use **nested conditions** to clearly **differentiate decisions, sequential actions, and validation steps**.
      - **The process must begin with "Acquire Units" and end with "Release Units".**
      - If any **assumptions are made (e.g., inferred missing connections), explicitly state the reasoning behind them.**

      ### **Expected Output Format**
      - Numbered list of **each process step** in order.
      - **Decision points handled with conditional branches**.
      - **Clearly indicate when paths diverge and merge back**.
      - If a step **was inferred**, include a note explaining why it logically belongs in the sequence.

      Now, perform the analysis and generate the structured workflow.
    """,
    # "prompt": f"""
    #   {parsed_details}

    #   Analyze the following JSON data extracted from a VSDX file, representing a process flow diagram. Determine the logical order of the diagram based on the spatial relationships of shapes, including their positions (X, Y coordinates), shape types, and structural connections, rather than relying solely on explicitly defined links. Identify points where the flow diverges, converges, or requires validation, and infer their role within the diagram. When missing connectors are detected, use positioning logic to infer the most probable flow sequence. Generate a structured, numbered step-by-step process that accurately describes the workflow. Ensure that actions are naturally incorporated into the description by integrating the textual content of each shape while maintaining contextual accuracy. Maintain clear differentiation between distinct process paths and actions that adjust or validate system states. The final release step should be identified and positioned as the conclusion of the structured sequence, following the inferred workflow based on the available diagram structure.
    # """,
    # "prompt": f"""
    #   {parsed_details}

    #   These are data extracted from a VSDX file. Can you understand what the diagram represents?
    #   Can you understand the flow of diagram based on their positions and not only rely on connectors reference?
    #   Also give me a step by step process listed by numbers.
    #   Some connectors may lack explicit links, you should use positional logic to determine the flow.
    #   Don't purely base your logic on positional you can still use connectors.
    #   Can you use the text content of shapes in the sentence and not mention shape ID.
    #   Treat it as flow chart and adjust your response base on keywords on the texts.

    #   Increasing Y means going up.
    #   Increasing X means going to right.

    #   Include all the shapes from the data and don't forget the number of shapes.
    # """,
    # "prompt": f"""
    #   Analyze the following JSON data extracted from a VSDX file, representing a process flow diagram. Determine the logical order of the diagram based on the spatial relationships of shapes, including their positions (X, Y coordinates), shape types, and structural connections, rather than relying solely on explicitly defined links. Identify points where the flow diverges, converges, or requires validation, and infer their role within the diagram. When missing connectors are detected, use positioning logic to infer the most probable flow sequence. Generate a structured, numbered step-by-step process that accurately describes the workflow. Ensure that actions are naturally incorporated into the description by integrating the textual content of each shape while maintaining contextual accuracy. Maintain clear differentiation between distinct process paths and actions that adjust or validate system states. The final release step should be identified and positioned as the conclusion of the structured sequence, following the inferred workflow based on the available diagram structure.
    #   {parsed_details}
    # """,
    # These are data extracted from a VSDX file. Can you understand what the diagram represents?
    # Can you understand the flow of diagram based on their positions and not only rely on connectors reference?
    # Can you identify which is the starting point and end of the diagram without relying on connectors?

    # Step-by-Step Process in sentence:
    #   Provide a step-by-step process listed by numbers.
    #   DO NOT include IDs.
    #   Enclose all text inside shapes within [brackets].

    # Notes:
    #   There might be shapes that are inside other shapes (Resource Box).
    #   There are connectors that has no connection to other shape in the data but is connected visually. You can take advantage of shape's positioning for this.
    #   There are shapes that are positioned above connectors and is necessary steps before moving to end point of connector. So you should consider them as steps too.
    #   Think of the texts as a logical flow too. Based on the words which is the next step.


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
    "stream": True,
    # "options": {
    #   "num_ctx": 32768,
    #   "seed": 1
    # }
    "options": {
      "num_ctx": 32768,
      "temperature": 0.4,
      "top_p": 0.9
    }
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
  # print(parsed_details)
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