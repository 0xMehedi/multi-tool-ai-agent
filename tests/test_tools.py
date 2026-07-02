import pytest
from unittest.mock import patch, MagicMock
from tools.institution_tool import InstitutionsDBTool
from tools.hospital_tool import HospitalsDBTool
from tools.restaurant_tool import RestaurantsDBTool


class TestDatabaseTools:
    def test_institution_tool_properties(self):
        tool = InstitutionsDBTool()
        assert tool.name == "institutions_db"
        assert tool.db_name == "institutions"
        assert tool.table_name == "institutions"
        assert "universities" in tool.description.lower()

    def test_hospital_tool_properties(self):
        tool = HospitalsDBTool()
        assert tool.name == "hospitals_db"
        assert tool.db_name == "hospitals"
        assert tool.table_name == "hospitals"
        assert "hospitals" in tool.description.lower()

    def test_restaurant_tool_properties(self):
        tool = RestaurantsDBTool()
        assert tool.name == "restaurants_db"
        assert tool.db_name == "restaurants"
        assert tool.table_name == "restaurants"
        assert "restaurants" in tool.description.lower()


class TestWebSearchTool:
    @pytest.fixture
    def tool(self):
        from tools.web_search_tool import WebSearchTool
        return WebSearchTool()

    def test_tool_properties(self, tool):
        assert tool.name == "web_search"
        assert "general knowledge" in tool.description.lower()

    @patch("tools.web_search_tool.WebSearchTool._duckduckgo_search")
    def test_web_search_fallback(self, mock_ddg, tool):
        mock_ddg.return_value = "Mocked search results"
        result = tool._run("test query")
        assert result == "Mocked search results"
        mock_ddg.assert_called_once_with("test query")
