# visual_analysis_server.py
import os
import base64
import mimetypes
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

mcp = FastMCP("VisualAnalysisServer")

@mcp.tool()
def extract_main_topic_from_image(file_path: str) -> str:
    """
    Loads an image and extracts the main identifiable topic/object/place/person.
    Returns ONLY the topic name (no sentences, no extra text).
    Example: "Eiffel Tower", "Pyramids of Giza", "Taj Mahal"
    """
    try:
        BASE_DIR = Path(__file__).parent.resolve()
        image_path = (BASE_DIR / file_path).resolve()
        if not image_path.is_file():
            return f"Error: File does not exist at path {file_path}"

        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_image = base64.b64encode(image_data).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/jpeg"

        client = OpenAI(api_key=OPENAI_API_KEY)

        image_data_url = f"data:{mime_type};base64,{base64_image}"

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Identify the main topic or landmark in this image. Respond with ONLY the name, no description."
                        },
                        {
                            "type": "input_image",
                            "image_url": image_data_url
                        }
                    ]
                }
            ],
            max_output_tokens=50
        )


        topic = response.output_text.strip()
        return topic

    except Exception as e:
        return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    logging.getLogger("mcp").setLevel(logging.WARNING)
    print("[Server] Visual Analysis Server started...")
    mcp.run(transport="stdio")
