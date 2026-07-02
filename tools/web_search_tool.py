from typing import Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from config.logging_config import setup_logging
from config.settings import TAVILY_API_KEY

logger = setup_logging(__name__)


class WebSearchInput(BaseModel):
    query: str = Field(description="Search query for general knowledge")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Use this tool for general knowledge questions about Bangladesh that are NOT "
        "covered by the databases (institutions, hospitals, restaurants). "
        "This includes: government policies, healthcare policies, historical facts, "
        "definitions, news, current events, demographics, geography, economy, "
        "cultural information, and any other general knowledge. "
        "Only use this when the answer is not available in the databases. "
        "Example: 'What is the healthcare policy of Bangladesh?', "
        "'Who regulates hospitals in Bangladesh?', "
        "'Difference between public and private hospitals', "
        "'Population of Bangladesh', 'History of Dhaka'"
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        try:
            if TAVILY_API_KEY:
                return self._tavily_search(query)
            return self._duckduckgo_search(query)
        except ImportError:
            return self._duckduckgo_search(query)
        except Exception as exc:
            logger.error("Web search failed: %s", exc)
            return f"Web search failed: {exc}"

    def _tavily_search(self, query: str) -> str:
        try:
            from langchain_community.tools import TavilySearchResults

            tool = TavilySearchResults(
                api_key=TAVILY_API_KEY,
                max_results=5,
            )
            results = tool.invoke({"query": query})
            formatted = []
            for r in results:
                if isinstance(r, dict):
                    content = r.get("content", str(r))
                    formatted.append(content)
                else:
                    formatted.append(str(r))
            return "\n\n".join(formatted[:5])
        except Exception as exc:
            logger.warning("Tavily search failed, falling back to DuckDuckGo: %s", exc)
            return self._duckduckgo_search(query)

    def _duckduckgo_search(self, query: str) -> str:
        try:
            from langchain_community.tools import DuckDuckGoSearchResults

            tool = DuckDuckGoSearchResults(max_results=5)
            result = tool.invoke({"query": query})
            return str(result)
        except Exception as exc:
            logger.error("DuckDuckGo search failed: %s", exc)
            return f"Search failed: {exc}"

    async def _arun(self, query: str) -> str:
        return self._run(query)
