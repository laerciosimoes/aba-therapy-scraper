from scrapegraphai.graphs import (
    SmartScraperGraph,
    SmartScraperMultiGraph,
)
from dotenv import load_dotenv
import json
import os

# Define the configuration for the scraping pipeline
# graph_config = {
#    "llm": {"model": "ollama/llama3.2", "model_tokens": 8192},
# "verbose": True,
# "headless": False,
# }
load_dotenv()


graph_config = {
    "llm": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}
#     prompt="Extract the name and position of the team members",

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract all the links on the page for the same domain. Do not include anchor links (#xxx). Return a list of links will full url.",
    source="https://abaenhancement.com/",
    config=graph_config,
)

# Run the pipeline
result = smart_scraper_graph.run()

for link in result["content"]:
    print(link)


smart_multi_graph = SmartScraperMultiGraph(
    prompt="Extract the name and position of the team members. Remove duplicate names.",
    source=result["content"],
    config=graph_config,
)

result = smart_multi_graph.run()

print(json.dumps(result, indent=4))
