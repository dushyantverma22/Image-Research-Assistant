# simple_test.py
import os
import base64
import mimetypes
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def load_image_from_path(file_path: str):
    """Standalone version of load_image_from_path"""
    try:
        image_path = Path(file_path)
        if not image_path.is_file():
            return {"error": f"File does not exist at path {file_path}"}
        
        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_image = base64.b64encode(image_data).decode('utf-8')
        mime_type, _ = mimetypes.guess_type(image_path)

        if not mime_type:
            mime_type = "application/octet-stream"

        return {
            "base64_image": base64_image,
            "mime_type": mime_type
        }
    except Exception as e:
        return {"error": str(e)}

def get_image_description(base64_image_string: str, mime_type: str):
    """Standalone version of get_image_description"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in one paragraph."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image_string}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error analyzing image: {e}"

def main():
    print("Simple Image Analysis Test")
    print("="*50)
    
    # Get image path from user
    image_path = input("Enter image path (or press Enter for default 'image/pyramid1.jpg'): ").strip()
    if not image_path:
        image_path = "image/pyramid1.jpg"
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        print(f"Current directory: {os.getcwd()}")
        return
    
    print(f"\n1. Loading image: {image_path}")
    print(f"   File size: {os.path.getsize(image_path)} bytes")
    
    # Load image
    result = load_image_from_path(image_path)
    
    if "error" in result:
        print(f"❌ Error loading image: {result['error']}")
        return
    
    print(f"✓ Image loaded successfully")
    print(f"   MIME type: {result['mime_type']}")
    print(f"   Base64 length: {len(result['base64_image'])} chars")
    
    # Ask if user wants to proceed with analysis
    proceed = input("\n2. Proceed with OpenAI analysis? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Analysis cancelled.")
        return
    
    print("\n3. Analyzing image with OpenAI...")
    description = get_image_description(result['base64_image'], result['mime_type'])
    
    print("\n" + "="*50)
    print("ANALYSIS RESULT:")
    print("="*50)
    print(description)
    print("="*50)
    
    # Save result to file
    save = input("\nSave result to file? (y/n): ").strip().lower()
    if save == 'y':
        output_file = f"analysis_{os.path.basename(image_path)}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Image: {image_path}\n")
            f.write(f"Size: {os.path.getsize(image_path)} bytes\n")
            f.write(f"MIME type: {result['mime_type']}\n")
            f.write("\n" + "="*50 + "\n")
            f.write("ANALYSIS:\n")
            f.write("="*50 + "\n")
            f.write(description + "\n")
        print(f"✓ Result saved to: {output_file}")

if __name__ == "__main__":
    main()