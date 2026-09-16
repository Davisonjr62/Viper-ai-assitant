import os
import signal
import sys
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from tools.windows import WindowsTools

AGENT_ID = os.getenv("VIPER_AGENT_ID", "").strip()
API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()


def main():
    if not API_KEY:
        print("ERROR: ELEVENLABS_API_KEY is not set.")
        sys.exit(1)
    if not AGENT_ID:
        print("ERROR: VIPER_AGENT_ID is not set.")
        sys.exit(1)

    tools = WindowsTools()
    client_tools = ClientTools()
    registrations = {
        "open_app": tools.open_app, "open_url": tools.open_url,
        "open_folder": tools.open_folder, "take_screenshot": tools.take_screenshot,
        "lock_pc": tools.lock_pc, "play_media": tools.play_media,
        "open_settings": tools.open_settings, "control_volume": tools.control_volume,
        "clipboard": tools.clipboard, "type_text": tools.type_text,
        "press_key": tools.press_key, "mouse_click": tools.mouse_click,
        "mouse_move": tools.mouse_move, "mouse_scroll": tools.mouse_scroll,
        "mouse_drag": tools.mouse_drag, "get_screen_info": tools.get_screen_info,
        "get_active_window": tools.get_active_window, "get_screen_image": tools.get_screen_image,
        "close_app": tools.close_app, "open_task_manager": tools.open_task_manager,
        "restart_app": tools.restart_app, "minimize_all_windows": tools.minimize_all_windows,
        "show_desktop": tools.show_desktop, "shutdown_pc": tools.shutdown_pc,
    }
    for name, callback in registrations.items():
        client_tools.register(name, callback)

    elevenlabs = ElevenLabs(api_key=API_KEY)
    conversation = Conversation(
        elevenlabs, AGENT_ID, requires_auth=True, client_tools=client_tools,
        callback_agent_response=lambda response: print(f"Viper: {response}"),
        callback_agent_response_correction=lambda original, corrected: print(f"Viper correction: {corrected}"),
        callback_user_transcript=lambda transcript: print(f"You: {transcript}"),
        callback_latency_measurement=lambda latency: print(f"[latency] {latency} ms"),
    )
    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

    print("========================================")
    print(" Viper Core — ElevenLabs Voice Backend")
    print("========================================")
    print(f"Agent: {AGENT_ID}")
    print("Voice: ElevenLabs Agents")
    print("Brain: GPT-5.6 Luna (configured in ElevenLabs)")
    print(f"Tools: {len(registrations)} local Windows tools")
    print("Press Ctrl+C to stop.\n")
    conversation.start_session()
    conversation_id = conversation.wait_for_session_end()
    print(f"\nConversation ended: {conversation_id}")


if __name__ == "__main__":
    main()
