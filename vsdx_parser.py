# Is this effective for Swimlane Diagrams?

# return diagram in ascii to double check if diagram is accurate
# before identifying the contents of diagram
# can you rebuild this ms visio diagram in ascii

# if the condition says loop back just say Loops back to "That part" ex. (Loops back to "Development & User Testing")


from vsdx import VisioFile
from collections import defaultdict

def extract_vsdx_details(file_path):
    with VisioFile(file_path) as vis:
      details = "Extracted Visio Diagram Data:\n"
      
      for page in vis.pages:
        details += f"\nPage: {page.name}\n"
        
        for shape in page.child_shapes:
          shape_id = shape.ID
          shape_text = shape.text.strip() if shape.text else ""

          shape_type = shape.universal_name if shape.universal_name else "Unknown"
          
          # Additional Classification
          if shape_text.endswith("?"):
            shape_type = "Decision"

          
          shape_x = shape.x
          shape_y = shape.y
          shape_width = shape.width
          shape_height = shape.height
          
          details += (
              f"Shape ID {shape_id}:\n"
              f"   • Is Connector: {True if shape.end_arrow and shape.end_arrow != 0 else False}\n"
              f"   • Text: '{shape_text}'\n"
              f"   • Type: {shape_type}\n"
              f"   • Position: (X: {shape_x}, Y: {shape_y})\n"
              f"   • Dimensions: (Width: {shape_width}, Height: {shape_height})\n"
          )

          unique_connections = set()

          if shape.connects:
            details += (f"\n")
            for conn in shape.connects:
              connected_shape = conn.shape
              # from_shape = conn.from_id

              # if from_shape and connected_shape:
              #   print(f"Shape ID {shape.ID} :Connector from '{from_shape}' to '{connected_shape.ID}'")


              from_shape = conn.from_id  # Get source shape ID
              from_cell = conn.from_rel  # Get specific connection point (may be None)



              if connected_shape and connected_shape.ID == shape.ID:
                  continue

              if from_shape and connected_shape:
                # print(f"Shape ID {shape.ID}: Connector from '{from_shape}' ({from_cell}) to '{connected_shape.ID}'")

                if (from_cell == 'BeginX'):
                  details += (f"   • From '{connected_shape.text.strip()}' to this arrow\n")
                elif (from_cell == 'EndX'):
                  details += (f"   • This arrow to '{connected_shape.text.strip()}'\n")

              # connected_text = (
              #   connected_shape.text.strip()
              #   if connected_shape and connected_shape.text
              #   else f"Shape ID {connected_shape.ID}"
              #   if connected_shape
              #   else "Unknown"
              # )

              # # Store as a tuple to avoid duplicates
              # connection_tuple = (shape_text, connected_text)
              # if connection_tuple not in unique_connections:
              #   unique_connections.add(connection_tuple)
              #   details += f"   • Connected to: {connected_text}\n"


      return details

# Example Usage
file_path = "Agile.Release.Process.Flowchart.Visiodiagram.vsdx"
# file_path = "Basic Flowchart Diagram - Student Enrollment Process.vsdx"
parsed_details = extract_vsdx_details(file_path)
print(parsed_details)
