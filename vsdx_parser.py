from vsdx import VisioFile

def extract_vsdx_details(file_path):
    with VisioFile(file_path) as vis:
        details = "Extracted Visio Diagram Data:\n"
        
        for page in vis.pages:
            details += f"\nPage: {page.name}\n"
            
            for shape in page.child_shapes:
                shape_id = shape.ID
                shape_text = shape.text if shape.text else "No text"
                shape_type = shape.shape_type
                shape_x = shape.x
                shape_y = shape.y
                shape_width = shape.width
                shape_height = shape.height
                
                details += (
                    f" - Shape ID {shape_id}:\n"
                    f"   * Text: {shape_text}\n"
                    f"   * Type: {shape_type}\n"
                    f"   * Position: (X: {shape_x}, Y: {shape_y})\n"
                    f"   * Dimensions: (Width: {shape_width}, Height: {shape_height})\n"
                )

                if shape.connects:
                    for conn in shape.connects:
                        connected_shape_id = conn.connector_shape_id
                        details += f"   * Connected to Shape ID {connected_shape_id}\n"
        
        return details

file_path = "Agile.Release.Process.Flowchart.Visiodiagram.vsdx"
parsed_details = extract_vsdx_details(file_path)

print(parsed_details)
