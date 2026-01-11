# test_server.py
from visual_analysis_server import extract_main_topic_from_image

def main():
    print("🔍 Testing Visual Analysis Server...\n")

    test_image_path = "image/pyramid1.jpg"  # relative to visual_analysis_server.py

    print(f"➡️ Testing with image path: {test_image_path}")

    result = extract_main_topic_from_image(test_image_path)

    print("\n================ RESULT ================\n")
    print(result)
    print("\n========================================\n")

if __name__ == "__main__":
    main()
