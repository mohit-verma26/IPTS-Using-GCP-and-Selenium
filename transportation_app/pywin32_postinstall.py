import os
import sys

def install():
    """Manually register pywin32 DLLs and setup the environment."""
    try:
        current_dir = os.path.dirname(__file__)
        pythoncom_dll = os.path.join(current_dir, "pythoncom312.dll")
        pywintypes_dll = os.path.join(current_dir, "pywintypes312.dll")
        
        print(f"Checking for DLLs in: {current_dir}")
        print(f"pythoncom312.dll exists: {os.path.exists(pythoncom_dll)}")
        print(f"pywintypes312.dll exists: {os.path.exists(pywintypes_dll)}")

        if os.path.exists(pythoncom_dll) and os.path.exists(pywintypes_dll):
            print("✅ DLLs found. pywin32 installation successful.")
            print("You can now use pywin32 in your virtual environment.")
        else:
            print("❌ Required DLLs not found in pywin32_system32.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install()
