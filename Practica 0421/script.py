# Run the sample.

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
# from azure.ai.projects.models import ...   # (no se distingue con claridad)

endpoint = "https://MusicLearnChatBot.services.ai.azure.com/api/projects/proj-default"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Create agent
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful agent"
)

# Create a thread
thread = project_client.agents.create_thread()

# Send a message
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Explain the concept of machine learning"
)

# Run the agent
run = project_client.agents.create_run(
    thread_id=thread.id,
    agent_id=agent.id
)

# Poll for completion
run = project_client.agents.get_run(
    thread_id=thread.id,
    run_id=run.id
)

# Get messages
messages = project_client.agents.list_messages(thread_id=thread.id)

for msg in messages:
    print(f"{msg.role}: {msg.content}")