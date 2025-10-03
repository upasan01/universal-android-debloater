import subprocess
import os

# --- Configuration ---
# NOTE: You MUST have ADB (Android Debug Bridge) installed and in your system's PATH
# You MUST enable Developer Options and USB Debugging on your Android device
# The device must be connected via USB and authorized for debugging

PACKAGE_NAME_TO_REMOVE = "com.samsung.android.email.provider"  # Example bloatware package
USER_ID = "0"  # User 0 is the main user. For work profiles, it might be different.
UNINSTALL_COMMAND = "pm uninstall --user" # The command to uninstall for a specific user
# The '-k' flag (optional) can be added to the command to *keep* the app data: 'pm uninstall -k --user'

def run_adb_command(command):
    """Executes an ADB shell command and returns the output."""
    try:
        # Construct the full command: adb shell <command>
        full_command = f"adb shell {command}"
        print(f"Executing: {full_command}")
        
        # Execute the command
        result = subprocess.run(
            full_command, 
            shell=True, 
            check=True,  # Raise an exception for non-zero exit codes
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        print(f"\n--- ADB COMMAND FAILED ---")
        print(f"Error executing command: {e.cmd}")
        print(f"Stderr: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        print("\n--- ERROR ---")
        print("ADB is not found. Ensure 'adb' is installed and correctly added to your system's PATH.")
        return None

def check_device_connection():
    """Checks if a device is connected and authorized."""
    try:
        output = subprocess.run(
            "adb devices", 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        ).stdout.strip().split('\n')
        
        if len(output) > 1 and "device" in output[1]:
            print("Device is connected and authorized.")
            return True
        
        print("No authorized device found. Check USB Debugging and authorization pop-up.")
        return False
    except:
        return False

def uninstall_bloatware(package, user):
    """Uninstalls a package using ADB's pm uninstall command."""
    
    # The actual ADB shell command being executed is:
    # pm uninstall --user 0 com.package.name
    adb_command = f"{UNINSTALL_COMMAND} {user} {package}"
    
    output = run_adb_command(adb_command)

    if output is not None:
        if "Success" in output:
            print(f"\nSUCCESS: Package '{package}' uninstalled for user {user}.")
        else:
            print(f"\nFAILURE: Could not uninstall '{package}'. Output: {output}")

if __name__ == "__main__":
    if check_device_connection():
        # --- List all packages (optional, but helpful for debloating) ---
        print("\n--- Listing Packages (system only) ---")
        package_list_output = run_adb_command("pm list packages -s | grep 'samsung'")
        print(package_list_output) # Will show a list like: package:com.samsung.android.app.xxx
        
        # --- Attempt to uninstall the specified package ---
        print(f"\n--- Attempting to uninstall {PACKAGE_NAME_TO_REMOVE} ---")
        input("Press ENTER to proceed with uninstallation (Ctrl+C to cancel)...")
        uninstall_bloatware(PACKAGE_NAME_TO_REMOVE, USER_ID)
    else:
        print("\nPlease resolve the connection issue and try again.")
