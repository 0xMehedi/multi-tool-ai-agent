from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from agent.prompt import SYSTEM_PROMPT
from agent.router import AgentState
from config.logging_config import setup_logging
from config.settings import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE

logger = setup_logging(__name__)


class AgentFactory:
    def __init__(self, tools: list[Any]) -> None:
        self.tools = tools
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not set. "
                "Create a .env file with your Google API key."
            )

    def _create_llm(self) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            google_api_key=GOOGLE_API_KEY,
            convert_system_message_to_human=False,
        )

    def _call_model(self, state: AgentState) -> dict[str, Any]:
        messages = state["messages"]
        llm = self._create_llm().bind_tools(self.tools)
        response = llm.invoke(messages)
        logger.info("LLM response: %s", response)
        return {"messages": [response]}

    def build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)

        tool_node = ToolNode(self.tools)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", tool_node)

        workflow.add_conditional_edges(
            "agent",
            tools_condition,
        )
        workflow.add_edge("tools", "agent")
        workflow.add_entry_point(START, "agent")

        graph = workflow.compile()

        return graph


def create_agent(tools: list[Any]) -> StateGraph:
    factory = AgentFactory(tools)
    return factory.build_graph()


def prepare_initial_message(user_input: str) -> list[Any]:
    return [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]
