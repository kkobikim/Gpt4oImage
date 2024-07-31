import openai

def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def upload_image(client, file_path):
    with open(file_path, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")
    return response['id']

def add_image_message(client, thread_id, file_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Please evaluate this parking photo: {file_id}"
    )
    return message

def run_assistant(client, thread_id, assistant_id):
    from openai import AssistantEventHandler
    from typing_extensions import override

    class EventHandler(AssistantEventHandler):
        @override
        def on_text_created(self, text) -> None:
            print(f"\nassistant > ", end="", flush=True)
          
        @override
        def on_text_delta(self, delta, snapshot):
            print(delta.value, end="", flush=True)

    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Evaluate the parking photo.",
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()