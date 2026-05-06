import os
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from openai.types.responses.response_input_param import McpApprovalRequest, ResponseInputParam

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client
with(
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Initialize agent MCP tool
    mcp_tool = MCPTool(
        server_label="api-specs",
        server_url="https://learn.microsoft.com/api/mcp",
        require_approval="always"
    )

    # Create a new agent with the MCP tool
    agent = project_client.agents.create_version(
        agent_name="AgentePerri",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="Eres un agente colaborativo que puede usar herramientas MCP para ayudar. Usa las herramientas del MCP para responder preguntas y hacer tareas",
            tools=[mcp_tool]
        )
    )

    print(f"Agente creado | ID: {agent.id}, name: {agent.name}, versión: {agent.version}")

    # Create conversation thread
    

    # Send initial request that will trigger the MCP tool
    

    # Process any MCP approval requests that were generated


    # Send the approval response back and retrieve a response
    
    
    # Clean up resources by deleting the agent version
    