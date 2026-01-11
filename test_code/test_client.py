# test_client_fixed.py
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_mcp_adapters.client import MultiServerMCPClient

async def test_tool_execution_fixed(tools):
    """Fixed version that handles list responses from tools"""
    print("\n⚡ Testing Tool Execution...")
    print("=" * 50)
    
    # Find the tools
    load_tool = next((t for t in tools if t.name == "load_image_from_path"), None)
    desc_tool = next((t for t in tools if t.name == "get_image_description"), None)
    
    if not load_tool:
        print("❌ 'load_image_from_path' tool not found")
        return False
    
    if not desc_tool:
        print("❌ 'get_image_description' tool not found")
        return False
    
    print("✅ Found both required tools")
    
    # Test 1: Create a test image
    print("\n1. Creating test image...")
    test_image_path = "test_quick_image.jpg"
    
    try:
        from PIL import Image
        img = Image.new('RGB', (50, 50), color='blue')
        img.save(test_image_path)
        print(f"✅ Created test image: {test_image_path} (50x50 blue)")
    except ImportError:
        print("❌ PIL/Pillow not installed")
        return False
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return False
    
    # Test 2: Execute load_image_from_path
    print("\n2. Testing 'load_image_from_path'...")
    try:
        result = await load_tool.ainvoke({"file_path": test_image_path})
        print(f"✅ Tool executed successfully")
        
        # DEBUG: Print the actual result
        print(f"   Result type: {type(result)}")
        print(f"   Result: {result}")
        
        # Handle different return types
        if isinstance(result, list):
            print("   ⚠ Tool returned a list (not dict)")
            # Try to find dictionary in list
            dict_item = None
            for item in result:
                if isinstance(item, dict):
                    dict_item = item
                    break
            
            if dict_item:
                result = dict_item
                print(f"   Found dict in list: {dict_item.keys()}")
            else:
                # Try to extract from text
                print(f"   List contents: {result}")
                # Maybe it's a list of strings?
                if len(result) > 0 and isinstance(result[0], str):
                    print(f"   First item (string): {result[0][:100]}...")
                    # Try to parse as JSON
                    import json
                    try:
                        parsed = json.loads(result[0])
                        if isinstance(parsed, dict):
                            result = parsed
                            print(f"   Parsed as dict: {parsed.keys()}")
                    except:
                        pass
        
        # Now check for errors/success
        if isinstance(result, dict):
            if "error" in result:
                print(f"❌ Tool returned error: {result['error']}")
                return False
            
            print(f"   Result keys: {list(result.keys())}")
            
            if "base64_image" in result:
                print(f"   ✅ Got base64 string ({len(result['base64_image'])} chars)")
                base64_data = result['base64_image']
            else:
                # Try alternative key names
                alt_keys = ['image', 'data', 'base64', 'content']
                for key in alt_keys:
                    if key in result:
                        base64_data = result[key]
                        print(f"   ✅ Got data from key '{key}' ({len(base64_data)} chars)")
                        break
                else:
                    print(f"❌ Missing 'base64_image' in result. Available keys: {list(result.keys())}")
                    return False
                    
            if "mime_type" in result:
                print(f"   ✅ Got MIME type: {result['mime_type']}")
                mime_type = result['mime_type']
            else:
                # Try to guess MIME type
                mime_type = "image/jpeg"
                print(f"   ⚠ Using default MIME type: {mime_type}")
                
        elif isinstance(result, str):
            print(f"   Tool returned string: {result[:100]}...")
            # Try to extract base64 from string
            import re
            base64_match = re.search(r'([A-Za-z0-9+/=]{20,})', result)
            if base64_match:
                base64_data = base64_match.group(1)
                print(f"   Extracted base64 ({len(base64_data)} chars)")
                mime_type = "image/jpeg"
            else:
                print(f"❌ Could not extract base64 from string result")
                return False
        else:
            print(f"❌ Unexpected result type: {type(result)}")
            return False
            
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Execute get_image_description
    print("\n3. Testing 'get_image_description'...")
    try:
        result = await desc_tool.ainvoke({
            "base64_image_string": base64_data,
            "mime_type": mime_type
        })
        print(f"✅ Tool executed successfully")
        print(f"   Result type: {type(result)}")
        
        # Handle different return types
        if isinstance(result, str):
            print(f"   ✅ Got string result")
            print(f"   Preview: {result[:200]}...")
            
            # Check for errors
            if "Error" in result or "error" in result.lower():
                print(f"⚠ Tool might have returned an error")
                if "rate limit" in result.lower() or "429" in result:
                    print(f"   Rate limit issue detected")
            else:
                print(f"✅ Looks like a valid image description")
                
        elif isinstance(result, list):
            print(f"   Tool returned list")
            for i, item in enumerate(result):
                print(f"   Item {i}: {type(item)} - {str(item)[:100]}...")
        elif isinstance(result, dict):
            print(f"   Tool returned dict: {result}")
        else:
            print(f"   Result: {str(result)[:200]}...")
            
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Clean up
    try:
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"\n🧹 Cleaned up test file: {test_image_path}")
    except:
        pass
    
    return True

async def main():
    """Quick test focusing on the tool execution issue"""
    print("🔍 Debugging Tool Execution Issue")
    print("=" * 60)
    
    server_configs = {
        "vision": {
            "command": "python",
            "args": ["visual_analysis_server.py"],
            "transport": "stdio",
        }
    }
    
    try:
        # Create client
        client = MultiServerMCPClient(server_configs)
        print("✅ Client created")
        
        # Get tools
        tools = await client.get_tools()
        print(f"✅ Got {len(tools)} tools")
        
        # Test the problematic tool
        print("\n🔧 Testing load_image_from_path specifically...")
        load_tool = next((t for t in tools if t.name == "load_image_from_path"), None)
        
        if load_tool:
            print(f"Found tool: {load_tool.name}")
            print(f"Tool type: {type(load_tool)}")
            print(f"Tool class: {load_tool.__class__.__name__}")
            
            # Create test image
            from PIL import Image
            test_path = "debug_test.jpg"
            img = Image.new('RGB', (10, 10), color='red')
            img.save(test_path)
            
            # Call the tool with different methods to see what it returns
            print(f"\n1. Calling tool with ainvoke()...")
            result1 = await load_tool.ainvoke({"file_path": test_path})
            print(f"   Result type: {type(result1)}")
            print(f"   Result: {result1}")
            
            print(f"\n2. Calling tool with invoke() (sync)...")
            try:
                result2 = load_tool.invoke({"file_path": test_path})
                print(f"   Result type: {type(result2)}")
                print(f"   Result: {result2}")
            except Exception as e:
                print(f"   Error: {e}")
            
            print(f"\n3. Checking tool metadata...")
            print(f"   Name: {load_tool.name}")
            print(f"   Description: {load_tool.description[:100]}...")
            print(f"   Args schema: {load_tool.args}")
            
            # Clean up
            os.remove(test_path)
            
        # Also test the other tool
        print("\n🔧 Testing get_image_description...")
        desc_tool = next((t for t in tools if t.name == "get_image_description"), None)
        
        if desc_tool:
            print(f"Found tool: {desc_tool.name}")
            print(f"Testing with dummy data...")
            
            # Create a tiny base64 image (1x1 pixel red PNG)
            tiny_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            result = await desc_tool.ainvoke({
                "base64_image_string": tiny_base64,
                "mime_type": "image/png"
            })
            print(f"   Result type: {type(result)}")
            print(f"   Result preview: {str(result)[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())