import os
import signal
import sys
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from tools.windows import WindowsTools

AGENT_ID = os.getenv("VIPER_AGENT_ID", "agent_7001m2na03rgfv6teda5dc0pm83d").strip()
API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()


def main():
    if not API_KEY:
        print("ERROR: ELEVENLABS_API_KEY is not set.")
        print('PowerShell: $env:ELEVENLABS_API_KEY="your-key"')
        sys.exit(1)

    tools = WindowsTools()
    client_tools = ClientTools()
    client_tools.register("open_app", tools.open_app)
    client_tools.register("open_url", tools.open_url)
    client_tools.register("open_folder", tools.open_folder)
    client_tools.register("take_screenshot", tools.take_screenshot)
    client_tools.register("lock_pc", tools.lock_pc)

    elevenlabs = ElevenLabs(api_key=API_KEY)
    conversation = Conversation(
        elevenlabs,
        AGENT_ID,
        requires_auth=True,
        client_tools=client_tools,
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
    print("Tools: local Windows allowlist")
    print("Press Ctrl+C to stop.\n")

    conversation.start_session()
    conversation_id = conversation.wait_for_session_end()
    print(f"\nConversation ended: {conversation_id}")


if __name__ == "__main__":
    main()
