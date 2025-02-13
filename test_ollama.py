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
    # "prompt": f"""
    #   Analyze the following JSON data extracted from a VSDX file representing a process flow diagram.

    #   {parsed_details}

    #   ### **Step 1: Identify All Major Process Steps**
    #   - Extract all **process-related shapes** (e.g., Hexagon, Process, Unknown with meaningful text).
    #   - Order them **top-to-bottom (descending Y-coordinates)** to infer flow.
    #   - Classify each shape into **Process, Decision, Validation, or Output**.
    #   - Clearly define what role each plays in the process.

    #   ### **Step 2: Determine Explicit and Inferred Logical Connections**
    #   - Identify **explicit connections** (direct "From" and "To" links).
    #   - For **missing connections**, infer the most logical flow based on:
    #     - **Vertical proximity** (closer Y-values suggest sequential steps).
    #     - **Shape type** (Process → Decision → Verification → Next Process).
    #     - **Contextual meaning** (e.g., "Verify" steps should follow cycle-setting steps).
    #   - Mark where **flow diverges into branches** (decision points).
    #   - Identify where **separate paths converge back into a single sequence**.

    #   ### **Step 3: Infer & Validate Missing Links**
    #   - Check if any shape **has no incoming or outgoing connections** and logically determine its place in the sequence.
    #   - Ensure that **all decisions** flow **back into the main path**.
    #   - If **steps are missing** but needed for logical continuity, explicitly state **the inferred transitions**.

    #   ### **Step 4: Generate the Fully Structured Workflow**
    #   - Output a **clear, numbered step-by-step process** that follows the inferred workflow.
    #   - Ensure **each transition is justified** and properly connected.
    #   - Use **nested conditions** to clearly **differentiate decisions, sequential actions, and validation steps**.
    #   - **The process must begin with "Acquire Units" and end with "Release Units".**
    #   - If any **assumptions are made (e.g., inferred missing connections), explicitly state the reasoning behind them.**

    #   ### **Expected Output Format**
    #   - Numbered list of **each process step** in order.
    #   - **Decision points handled with conditional branches**.
    #   - **Clearly indicate when paths diverge and merge back**.
    #   - If a step **was inferred**, include a note explaining why it logically belongs in the sequence.

    #   Now, perform the analysis and generate the structured workflow.
    # """,
    "prompt": f"""
      Objective
      Analyze JSON data extracted from a VSDX process flow diagram, where explicit shape-to-shape connections may be missing.
      Your task is to strictly reconstruct the logical workflow in a step-by-step manner, ensuring all process steps are sequentially valid and missing links are properly inferred.

      Required Output Format
      Your output must include the following:

      Step-by-Step Ordered Workflow (Human-Readable Explanation)

      Explain the process in natural language as if you were describing it to someone unfamiliar with the diagram.
      Do not just list shape IDs—each step should be described in plain, understandable text.
      
      Divergence and Convergence Analysis (Decision Paths Must Rejoin Before Continuing)

      Clearly state where decisions split into different paths (YES/NO) and how they rejoin.
      Ensure that NO further steps occur before validation is completed.

      Final Release Step Identification

      Explicitly mark the final step that completes the workflow and explain why it is the last step.

      Rules for Logical Flow Determination (Strict Validation & Missing Link Recovery Required)

      1. Identifying Start and End Points
         - Start Point: Identify the shape with the highest Y-coordinate that contains meaningful text and represents an initialization, action, or decision.
         - End Point: Identify the lowest Y-coordinate shape that signals process completion (e.g., "Release Units").
      
      2. Primary Flow Ordering (Strict Positional Alignment)
         - Higher Y-values occur first (earlier in the sequence).
         - Horizontal alignment suggests decision branching (YES/NO paths) or parallel actions.

      3. Missing Link Enforcement (Strict Pre-Validation Required Before Assignments)
         - If a step assigns a value (e.g., setting CYCLES_REMAINING), verification must occur first.
         - If verification (Shape 60) follows assignment (Shape 58), it must explicitly happen before moving forward.

      4. Decision Path Enforcements (Flow Must Merge Before Continuing)
         - YES/NO paths must be explicitly merged before verification happens.
         - Flow cannot continue to assignments like resin type (Shape 56) until the merged path completes validation.

      Example Output Using the Provided JSON Data (Step-by-Step Explanation)

      Step-by-Step Process Flow (Human-Readable Format)

      1. **Acquire the necessary units**
         - The process begins by acquiring the required unit for processing.
         (Shape ID "3" - "Acquire Units")

      2. **Reset the cycle count before starting**
         - The system ensures a clean start by setting CYCLES_REMAINING = 0.
         (Shape ID "48")

      3. **Retrieve instructions for the process**
         - Operators must follow specific instructions to ensure proper execution.
         (Shape ID "51" - "M_Instructions")

      4. **Obtain the packed Q-Sepharose column**
         - This step ensures the required column is obtained before validation.
         (Shape ID "53")

      5. **Enter the column's MEI number for tracking**
         - The operator must record the exact MEI number as labeled.
         (Shape ID "38")

      6. **Decision: "Was the column packed with all new resin?"**
         - At this point, the process branches into two possible paths:
           - **YES Path:** The column is fully new and follows automatic cycle count updating.
           - **NO Path:** The column contains a mix of new and old resin, requiring manual justification.
         (Shape ID "43")

      7. **Parallel Processing (YES/NO Path Enforcement)**
         - **YES Path (New Resin) →**
           - Automatically set CYCLES_REMAINING to 100. (Shape ID "58")
           - Prepare for verification of the updated cycle count.
         - **NO Path (Mixed Resin) →**
           - Manually enter the number of cycles allowed and provide justification. (Shape ID "64")
           - Prepare for verification of the updated cycle count.

      8. **Merge YES/NO Paths Before Verification**
         - Before verification can occur, both paths must **converge into a single flow.**
         - This ensures all cycle counts, whether automatically set or manually entered, are validated **in the same process.**

      9. **Verify that the cycle count is correct before continuing**
         - **This is a critical validation step.**
         - **No further processing (e.g., resin assignment) can occur unless this verification passes.**
         (Shape ID "60")

      10. **Set the resin type after verification confirms correctness**
         - Only after verification passes can the resin type be assigned.
         (Shape ID "56")

      11. **Finalize the process by releasing the units**
         - The final step marks the end of the workflow, confirming all requirements are met.
         (Shape ID "21")

      Divergence and Convergence Analysis (Step-by-Step Explanation)

      - The process diverges at Step 6 when a decision is made regarding whether the column is packed with all new resin.
        - **YES Path (automatic update)** → immediately sets cycles to 100.
        - **NO Path (manual entry required)** → requires user input before continuing.
      - **Paths must merge before verification (Step 8)**
        - **Cycle count verification (Step 9) is the merging point** that ensures process correctness.
      - **Final convergence happens before resin assignment (Step 10)**
        - The **resin type cannot be assigned until verification is completed.**

      Final Release Step Identification

      - The workflow officially ends with Step 11: "Release Units".
      - This ensures all units are processed correctly and released according to the verified cycle count.

      {parsed_details}
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