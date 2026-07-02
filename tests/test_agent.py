import pytest
from agent.prompt import SYSTEM_PROMPT
from agent.router import AgentState, should_continue, create_router_workflow


class TestPrompt:
    def test_system_prompt_contains_key_elements(self):
        assert "Institutions Database" in SYSTEM_PROMPT
        assert "Hospitals Database" in SYSTEM_PROMPT
        assert "Restaurants Database" in SYSTEM_PROMPT
        assert "Web Search" in SYSTEM_PROMPT
        assert "SELECT" in SYSTEM_PROMPT
        assert "DROP" in SYSTEM_PROMPT
        assert "database" in SYSTEM_PROMPT.lower()


class TestRouter:
    def test_agent_state_has_messages(self):
        state: AgentState = {"messages": []}
        assert "messages" in state

    def test_workflow_created(self):
        workflow, state_schema = create_router_workflow()
        assert workflow is not None
        assert state_schema is not None
