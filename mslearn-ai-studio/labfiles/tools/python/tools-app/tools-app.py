import os
from dotenv import load_dotenv
import glob

# Import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )
        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # Create vector store and upload files
        print("Creando vector, subiendo archivos...")
        vector_store = openai_client.vector_stores.create(  
            name = "travel-brochures"
        )
        #Se requiere un file stream para gestionar la subida de los archivos
        file_stream = [open(f, "rb") for f in glob.glob("*brochures/*.pdf")]# open text mode es el significado de rb es la forma en que se abrira un archivo este permitira obtener el binario del archivo y leerlo
        if not file_stream: # en caso de que se borren los pdf
            print("No se encontraron archivos para subir.")
            return
        
        file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id = vector_store.id,
            files = file_stream
        )

        for f in file_stream:
            f.close()
        print(f"Vector store creadi con {file_batch.file_counts.completed} archivos")

        # Track conversation state
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a question (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a question.")
                continue

            # Get a response using tools
            response = openai_client.responses.create(
                model=model_deployment,
                instructions = """
                    Eres un asistente de viajes que da informacion sobre servicions de viajes   disponibles de la agencia     viajes embrujados. Respondes      preguntas hacerca de servicios ofrecudos por la agencia usando los brouchers de viajes brindados busca en internet o para obtener informacion general hacerca de destinos . 
                """,
                input=input_text,
                previous_response_id = last_response_id,
                tools = [
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id] # pueden ser varios, en la documentacion el tipo de dato es lista
                    },
                    {
                        "type": "web_search",
                    }
                ]
            )
            print(response.output_text)
            last_response_id = response.id



    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
