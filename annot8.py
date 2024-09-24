import subprocess
import os
import time
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
import threading

# Define directories
project_dir = os.path.expanduser("~/tutorial_project")
screenshot_dir = os.path.join(project_dir, "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)

# Function to save clipboard content (screenshot) to a file
def save_clipboard_image(step_num):
    filename = f"screenshot_step_{step_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(screenshot_dir, filename)

    try:
        clipboard_content = subprocess.check_output(['wl-paste', '-t', 'image/png'], stderr=subprocess.DEVNULL)
        with open(filepath, 'wb') as f:
            f.write(clipboard_content)
        print(f"Screenshot saved: {filepath}")

        # Clear clipboard after saving
        subprocess.run(['wl-copy', '-n', ''])
        return filepath
    except subprocess.CalledProcessError:
        return None

# Function to convert keycodes to readable characters
def parse_keypress(keycode, capitalize):
    if keycode.startswith("KEY_"):
        key = keycode[4:]

        if key in ["LEFTSHIFT", "LEFTCTRL"]:
            return None
        if key == "SPACE":
            return " "
        if key == "DOT":
            return "."
        if key == "ENTER":
            return "\r"

        return key.upper() if capitalize else key.lower()
    return key

caps = False;

# Function to continuously capture keypresses
def capture_keypresses(dev, keypresses, esc_event):
    global caps
    print(f"Listening to {dev.name}...\nPress Ctrl+C to stop.")
    shift_active = False

    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)

                if key_event.keystate == key_event.key_down:
                    raw_key = key_event.keycode

                    if raw_key == "KEY_LEFTSHIFT":
                        shift_active = True
                    elif raw_key == "KEY_CAPSLOCK":
                        caps = not caps
                    elif raw_key == "KEY_SYSRQ":
                        continue
                    elif raw_key == "KEY_F9":
                        esc_event.set()
                        continue

                    capitalize = shift_active or caps
                    key = parse_keypress(raw_key, capitalize)

                    if key is not None:
                        keypresses.append(key)
    except Exception as e:
        print(f"Error capturing keypresses: {e}")

# Function to generate Markdown output
def generate_markdown(steps):
    with open(os.path.join(project_dir, "tutorial.md"), "w") as f:
        for i, step in enumerate(steps, 1):
            f.write(f"## Step {i}: {step['description']}\n")
            f.write(f"**Context**: {step['keypresses']}\n")
            f.write("\n")
    print(f"Markdown saved to {project_dir}/tutorial.md")

# Main loop to capture screenshots and keypresses
def main():
    steps = []
    step_num = 0
    device_path = '/dev/input/by-path/<insert your device here>'

    try:
        dev = InputDevice(device_path)
    except Exception as e:
        print(f"Error accessing device: {e}")
        return

    keypresses = []
    esc_event = threading.Event()
    keypress_thread = threading.Thread(target=capture_keypresses, args=(dev, keypresses, esc_event))
    keypress_thread.daemon = True  # Ensure thread exits when main program does
    keypress_thread.start()

    print("Starting tutorial creation... Press Ctrl+C to stop.")

    try:
        while True:
            # Wait for the user to copy a screenshot
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Listening for input ...")
            time.sleep(1)  # Adjust sleep time as needed

            # Save the screenshot
            screenshot_path = save_clipboard_image(step_num)
            if screenshot_path:
                keypresses.append(f"\r![Screenshot]({screenshot_path})\r")


            if esc_event.is_set():
                step_num += 1
                description = f"step {step_num}"
                # Store the accumulated keypresses for the current step
                steps.append({
                    "description": description,
                    "keypresses": "".join(keypresses)  # Get last input as string
                })
                print(f"Step {step_num} recorded with keypresses: {keypresses}")
                # Reset current_input for the next round
                keypresses.clear()  # Clear the keypresses for the next step
                esc_event.clear()

    except KeyboardInterrupt:
        print("Stopping tutorial creation...")
        if steps:
            generate_markdown(steps)
        else:
            print("No steps recorded, Markdown file not created.")

if __name__ == "__main__":
    main()
