# https://console.groq.com/

from dotenv import load_dotenv
from groq import Groq
from vsdx_parser import extract_vsdx_details

load_dotenv()

client = Groq()

# file_path = "docs/Basic Flowchart Diagram - Student Enrollment Process.vsdx"
# file_path = "docs/Agile.Release.Process.Flowchart.Visiodiagram.vsdx"
file_path = "docs/Drawing2.vsdx"

parsed_details = extract_vsdx_details(file_path)

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            # "content": "Explain the importance of fast language models",
            # "content": f"""
            #   These are data extracted from a VSDX file. Can you understand what the diagram represents?
            #   Give me a step by step process
            #   if the condition says loop back just say Loops back to "That part" ex. (Loops back to "Development & User Testing")
            #   On your output, dont include ID's 
            #   also the text inside the shapes should be enclosed in [brackets]

            #   {parsed_details}

            #   also can you can you recreate it in a python code, use while for loop and if for conditions
            #   no need to format it as a code block for markdown, just plain python
            # """,
            # "content": f"""
            #   Analyze the following JSON data extracted from a VSDX file, representing a process flow diagram. Determine the logical order of the diagram based on the spatial relationships of shapes, including their positions (X, Y coordinates), shape types, and structural connections, rather than relying solely on explicitly defined links. Identify points where the flow diverges, converges, or requires validation, and infer their role within the diagram. When missing connectors are detected, use positioning logic to infer the most probable flow sequence. Generate a structured, numbered step-by-step process that accurately describes the workflow. Ensure that actions are naturally incorporated into the description by integrating the textual content of each shape while maintaining contextual accuracy. Maintain clear differentiation between distinct process paths and actions that adjust or validate system states. The final release step should be identified and positioned as the conclusion of the structured sequence, following the inferred workflow based on the available diagram structure.
            #   {parsed_details}

            #   Don't mention ID
            # """
            "content": f"""
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

              Don't ignore shapes and dont mention shape id in output.
              Give fully detailed output, mention the texts inside shapes.
            """,
            # "content": f"""
            #   Objective
            #   Analyze JSON data extracted from a VSDX file representing a process flow diagram where explicit connectors may be missing. The data consists of various shapes with associated properties, including spatial positions (X, Y coordinates), dimensions, text, and connectivity status.

            #   Your task is to reconstruct the logical workflow sequence using strict positional inference, ensuring process continuity, correct step ordering, and accurate branch merging.

            #   Rules for Logical Flow Determination (Strict Positional Analysis Required)
            #   Start and End Points Identification:

            #   Start Point: The highest Y-coordinate with a meaningful text label (not "No Text"). If ambiguous, select the nearest relevant process step (e.g., an initialization or data acquisition step).
            #   End Point: The lowest Y-coordinate with a completion-related action (e.g., "Release Units").
            #   Sequential Ordering Based on Spatial Positioning:

            #   Shapes with higher Y-values come earlier in the workflow.
            #   If multiple shapes share the same Y, assume vertical flow is primary, while horizontal alignment suggests parallel processes or branching paths.
            #   Decision Points and Divergences (Strict Path Inference Required):

            #   Explicit decision points (e.g., "Column packed with new resin?") will have branches to alternative paths, but if no direct connections exist, infer paths based on proximity and expected logical sequence.
            #   YES/NO flows are assumed by identifying the closest step vertically aligned below (default) or horizontally adjacent (only if logical).
            #   Inferring Missing Connections (Strict Proximity-Based Logic):

            #   If a step directly follows another in logical function (e.g., setting a variable after acquiring a unit), assume an implicit connection even if missing.
            #   If values are referenced from previous steps (e.g., a column cycle count appearing later), ensure that earlier steps logically lead to it.
            #   Structural and Functional Validation:

            #   Assignments (e.g., "Set CYCLES_REMAINING = 100") must follow a related input or validation.
            #   Processes related to equipment status, unit release, or state verification occur in the final stages before release.
            #   Expected Output Format (Strict Structure Enforcement)
            #   1. Step-by-Step Ordered Workflow (Ensuring Correct Process Continuity)
            #   Present the reconstructed process as a numbered sequence, logically ordered from start to finish.
            #   Ensure decisions and alternative paths are clearly separated, maintaining correct branching logic.
            #   2. Divergence and Convergence Analysis (Strict Flow Path Evaluation Required)
            #   Identify where the process branches and how it rejoins, ensuring there are no gaps in the inferred flow.
            #   3. Final Release Step Identification (Explicit End of Process)
            #   Explicitly mark the final process action that concludes the workflow, ensuring that all previous steps logically lead to it.
            #   Example Using Provided Data (Strict Path Enforcement Applied)
            #   Step-by-Step Process Flow
            #   1. Acquire Units (Start) → (First Process Action, Y-Highest Meaningful Step)

            #   "Acquire Units" (Shape "3") initiates the process.
            #   2. Set Initial Conditions → (Directly Below Acquisition Step, Assigns Initial State)

            #   "Set CYCLES_REMAINING = 0" (Shape "48") resets the cycle count.
            #   3. Retrieve Instructions → (Instructions Follow Initialization, Sequential Flow Maintained)

            #   "M_Instructions" (Shape "51") loads operational guidance.
            #   4. Obtain Packed Column → (Column Information Directly Follows Instructions Step)

            #   Reference ticket and obtain the "Q-Sepharose column" (Shape "53").
            #   5. Enter Column MEI# → (Follows Packing Step, Data Entry Required)

            #   "Enter the packed Q-Sepharose column MEI# exactly as it appears in the MEI label."
            #   6. Decision: "Column packed with all new resin?" → (Decision Path Detected)

            #   YES Path: Move to automatic cycle count setting.
            #   NO Path: Move to manual entry with justification.
            #   7. Set or Enter Cycle Count → (Parallel Paths Exist Here Based on Decision Outcome)

            #   YES Path → "Set PC_SKID_BAY3COL..CYCLES_REMAINING = 100" (Automatic Assignment).
            #   NO Path → "Enter allowable column cycles + justification" (Manual Input Required).
            #   8. Verify Cycle Count → (Mandatory Verification Before Proceeding)

            #   Ensure that CYCLES_REMAINING is properly updated.
            #   9. Assign Resin Type → (Final Preparation Before Release)

            #   "Set RESIN_TYPE = Q2C4v1.0" (Shape "56").
            #   10. Release Units (Final Step) → (Explicit End Step with No Further Processing)

            #   Process completes with "Release Units" (Shape "21").
            #   Divergence and Convergence Analysis (Strict Flow Path Verification)
            #   Flow Diverges at Decision Point: "Column packed with all new resin?"
            #   YES Path: Direct update of cycle count.
            #   NO Path: Manual entry + justification.
            #   Flow Converges After Validation:
            #   Both paths merge before verification and resin type assignment.
            #   Final Release Step Identification (Process Completion Verified)
            #   Final step: "Release Units" (Shape "21") explicitly marks the end of the workflow.
            #   Instructions for Any Similar Data (Strictly Enforce This Approach)
            #   Determine sequence based on Y-position first (vertical flow priority).
            #   Use X-axis alignment only for branching decisions (parallel paths).
            #   Infer missing links using process logic, variable references, and functional grouping.
            #   Ensure the final step is explicitly marked and logically connected.

            #   {parsed_details}
            # """
        }
    ],

    # The language model which will generate the completion.
    model="llama-3.3-70b-versatile",

    #
    # Optional parameters
    #

    # Controls randomness: lowering results in less random completions.
    # As the temperature approaches zero, the model will become deterministic
    # and repetitive.
    temperature=0.5,

    # The maximum number of tokens to generate. Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_completion_tokens=1024,

    # Controls diversity via nucleus sampling: 0.5 means half of all
    # likelihood-weighted options are considered.
    top_p=1,

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    stop=None,

    # If set, partial message deltas will be sent.
    stream=False,
)

# Print the completion returned by the LLM.
print(chat_completion.choices[0].message.content)
#test comment TESTER
#test grock
#test grock part 2
#test grock part 3