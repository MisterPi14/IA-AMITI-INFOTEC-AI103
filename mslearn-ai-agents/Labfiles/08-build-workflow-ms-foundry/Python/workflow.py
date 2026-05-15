import os
from dotenv import load_dotenv

#Notese que en el script no se crea un agene sino que se llama al workflow dado que el agente ya se encuentra dentro del mismo definido en azure


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
endpoint = os.environ["PROJECT_ENDPOINT"]

# Connect to the AI Project client
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Specify the workflow
    workflow = {
        "name": "AgenteTriageSoporte"
    }

    # Create a conversation and run the workflow
    conversation = openai_client.conversations.create()
    print(f"Conversación creada {conversation.id}")
        #Response, completition, stream (se usara esta)


    stream = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": workflow["name"], "type": "agent_reference"}},
        input="Start",
        stream=True
    )

    # Process events from the workflow run

    #se usa por que tendremos una respuesta ademas ya la tenemos en comparacion al while que la va recibiendo
    for event in stream:
        if (event.type == "response.completed"):
            response = openai_client.responses.retrieve(event.response.id)
            print(f"{response.output_text}")

    # Clean up resources
    openai_client.conversations.delete(conversation_id=conversation.id)
print("\nConversación eliminada")

 