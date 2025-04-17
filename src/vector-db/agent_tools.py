import json
import vertexai
from vertexai.generative_models import FunctionDeclaration, Tool, Part

# Specify a function declaration and parameters for an API request

get_book_by_search_content_func = FunctionDeclaration(
    name="get_specie_info_by_search_content",
    description="Get the bird info chunks filtered by search terms",
    # Function parameters are specified in OpenAPI JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "search_content": {"type": "string", "description": "The search text to filter content from texts. The search term is compared against the texts based on cosine similarity. Expand the search term to a a sentence or two to get better matches"},
        },
        "required": ["search_content"],
    },
)
def get_specie_info_by_search_content(search_content, collection, embed_func):

    query_embedding = embed_func(search_content)

    # Query based on embedding value 
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )
    return "\n".join(results["documents"][0])

# Define all functions available to the bird expert
bird_expert_tool = Tool(function_declarations=[get_book_by_search_content_func])


def execute_function_calls(function_calls,collection, embed_func):
    parts = []
    for function_call in function_calls:
        print("Function:",function_call.name)
      
        if function_call.name == "get_specie_info_by_search_content":
            print("Calling function with args:", function_call.args["search_content"])
            response = get_specie_info_by_search_content(function_call.args["search_content"],collection, embed_func)
            print("Response:", response)
            #function_responses.append({"function_name":function_call.name, "response": response})
            parts.append(
					Part.from_function_response(
						name=function_call.name,
						response={
							"content": response,
						},
					),
			)

    
    return parts
