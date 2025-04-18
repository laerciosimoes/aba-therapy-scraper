from typing import List
from scrapegraphai.graphs import SmartScraperGraph, SmartScraperMultiGraph  # type: ignore
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


class TeamExtractor:
    def __init__(self, llm=None):
        load_dotenv()

        self.graph_config = {
            "llm": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "openai/gpt-4o-mini",
            },
            "verbose": True,
            "headless": False,
        }

    def ensure_protocol(self, url: str, default_scheme: str = "https") -> str:
        """
        Guarantee that the returned URL has a scheme.
        If the input has no scheme, prepend `default_scheme://`.
        """
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"{default_scheme}://{url}"
        return url

    def extract(self, url: str) -> list[dict]:

        try:

            # Create the SmartScraperGraph instance
            smart_scraper_graph = SmartScraperGraph(
                prompt="Extract all the links on the page for the same domain. Do not include anchor links (#xxx). Return a list of links will full url.",
                source=self.ensure_protocol(url),
                config=self.graph_config,
            )

            # Run the pipeline
            result = smart_scraper_graph.run()

            if (
                not isinstance(result, dict)
                or "content" not in result
                or not result["content"]
            ):
                return []

            smart_multi_graph = SmartScraperMultiGraph(
                prompt="Extract the name and position of the team members. Remove duplicate names.",
                source=result["content"],
                config=self.graph_config,
            )

            result = smart_multi_graph.run()

            if (
                not isinstance(result, dict)
                or "team_members" not in result
                or not result["team_members"]
            ):
                return []

            return [
                {"Url": url, "name": member["name"], "position": member["position"]}
                for member in result["team_members"]
            ]
        except Exception as e:
            # If the url is not valid, return an empty list or has an error, return an empty list
            print(f"Error: {e}")
            return []
