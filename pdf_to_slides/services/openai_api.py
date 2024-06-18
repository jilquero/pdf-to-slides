import os
import inspect
import importlib.resources

from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv


def openai_api(
    markdown: str,
) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_PROJECT_API_KEY")
    if api_key is None:
        raise ValueError("api_key is not defined in .env file")

    client = OpenAI(api_key=api_key)

    # Create a vector store caled "Presentation Base-Files"
    vector_store = client.beta.vector_stores.create(name="Presentation Base-Files")

    markdown_file = BytesIO(bytes(markdown, encoding="utf-8"))
    markdown_file.name = "document.md"
    formatting_file = importlib.resources.files("resources").joinpath("schema.json")

    # Ready the files for upload to OpenAI
    file_streams = [markdown_file]

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    assistant = client.beta.assistants.create(
        name="File summarizer to Presentation Assistant",
        instructions=inspect.cleandoc(
            """This GPT assists with summarizing Markdown text into bullet points, translating to Polish, and inserting a nested JSON object for images.
            The output should be a JSON file with a specific structure, ensuring images fit well within the summary.
            The JSON structure is: {vector_store.id}. You can modify this structure to better fit the task.
            You are assistant that creates json file based on markdown provided.
            Use your skills to summarize and translate the topics from the markdown into cohesive output.
            In the case when authors, university names and bibliography (references) not specified omit them in result json"""
        ),
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )

    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=open(formatting_file, "rb"), purpose="assistants"
    )

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Change the following markdown into json based on the template. Translate text from markdown file to Polish",
                # Attach the new file to the message.
                "attachments": [
                    {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                ],
            }
        ]
    )

    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    return strip_markdown(message_content.value)


def strip_markdown(markdown: str) -> str:
    json_start = markdown.find("```json")
    if json_start == -1:
        return markdown
    json_end = markdown.find("```", json_start + 1)
    return markdown[json_start + 7 : json_end]  # noqa E203
