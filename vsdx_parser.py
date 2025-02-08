# Is this effective for Swimlane Diagrams?
# return diagram in ascii to double check if diagram is accurate
# before identifying the contents of diagram
# can you rebuild this ms visio diagram in ascii
# if the condition says loop back just say Loops back to "That part" ex. (Loops back to "Development & User Testing")
# can you get the process description of this diagram?

import json
import pandas as pd
from vsdx import VisioFile

def extract_vsdx_details(file_path):
  shapes_list = []

  with VisioFile(file_path) as vis:
    for page in vis.pages:
      for shape in page.child_shapes:
        shape_id = shape.ID
        shape_text = shape.text.strip() if shape.text else "No Text"
        
        shape_text = shape_text.replace("\u2028", " ").replace("\u2029", " ")

        shape_type = shape.universal_name if shape.universal_name else "Unknown"

        # Additional Classification
        if shape_text.endswith("?"):
          shape_type = "Decision"

        shape_x = shape.x
        shape_y = shape.y
        shape_width = shape.width
        shape_height = shape.height

        shape_data = {
          "Page": page.name,
          "Shape ID": shape_id,
          "Text": shape_text,
          "Type": shape_type,
          "X": shape_x,
          "Y": shape_y,
          "Dimensions": {"Width": shape_width, "Height": shape_height},
          "Is Connector": False,
          "Connections": []
        }

        is_connector_added = False

        if shape.connects:
          for conn in shape.connects:
            connected_shape = conn.shape
            from_shape = conn.from_id
            from_cell = conn.from_rel

            if connected_shape and connected_shape.ID == shape.ID:
              continue

            if from_shape and connected_shape:
              if not is_connector_added:
                shape_data["Is Connector"] = True
                is_connector_added = True

              if from_cell == 'BeginX':
                shape_data["Connections"].append(
                  {"Direction": "From", "Connected To": connected_shape.text.strip()}
                )
              elif from_cell == 'EndX':
                shape_data["Connections"].append(
                  {"Direction": "To", "Connected To": connected_shape.text.strip()}
                )

        shapes_list.append(shape_data)

  # Convert to DataFrame for sorting
  df = pd.DataFrame(shapes_list)

  # Sort by Y descending (higher values first) and then X ascending (left-to-right)
  df = df.sort_values(by=["Y", "X"], ascending=[False, True])

  # Convert sorted DataFrame back to list of dictionaries
  sorted_shapes_list = df.to_dict(orient="records")

  # Convert to JSON format with `ensure_ascii=False` to keep special characters readable
  json_output = json.dumps(sorted_shapes_list, indent=2, ensure_ascii=False)

  return json_output

# Example Usage
# file_path = "docs/Agile.Release.Process.Flowchart.Visiodiagram.vsdx"
# file_path = "docs/Basic Flowchart Diagram - Student Enrollment Process.vsdx"
# file_path = "docs/Drawing2.vsdx"
# parsed_details = extract_vsdx_details(file_path)
# print(parsed_details)