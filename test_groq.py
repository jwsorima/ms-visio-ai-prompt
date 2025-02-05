# https://console.groq.com/

from dotenv import load_dotenv
from groq import Groq
from vsdx_parser import extract_vsdx_details

load_dotenv()

client = Groq()

# file_path = "docs/Basic Flowchart Diagram - Student Enrollment Process.vsdx"
# file_path = "docs/Agile.Release.Process.Flowchart.Visiodiagram.vsdx"
file_path = "docs/converttoMPHtoKPH.vsdx"

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
            "content": "Explain the importance of fast language models",
            "content": f"""
              These are data extracted from a VSDX file. Can you understand what the diagram represents?
              Give me a step by step process
              if the condition says loop back just say Loops back to "That part" ex. (Loops back to "Development & User Testing")
              On your output, dont include ID's 
              also the text inside the shapes should be enclosed in [brackets]

              {parsed_details}

              also can you can you recreate it in a python code, use while for loop and if for conditions
              no need to format it as a code block for markdown, just plain python
            """,
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