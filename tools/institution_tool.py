from tools.database_tool_base import DatabaseTool


class InstitutionsDBTool(DatabaseTool):
    name: str = "institutions_db"
    db_name: str = "institutions"
    table_name: str = "institutions"
    description: str = (
        "Use this tool for questions about Bangladeshi educational institutions, "
        "universities, schools, colleges, government institutions, training centers, "
        "and educational organizations. Covers data about institution names, types, "
        "locations (districts), establishment years, and institutional categories. "
        "Example: 'List universities in Dhaka', 'How many government colleges in Rajshahi?'"
    )
