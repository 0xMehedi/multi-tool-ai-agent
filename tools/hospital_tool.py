from tools.database_tool_base import DatabaseTool


class HospitalsDBTool(DatabaseTool):
    name: str = "hospitals_db"
    db_name: str = "hospitals"
    table_name: str = "hospitals"
    description: str = (
        "Use this tool for questions about hospitals and healthcare facilities in Bangladesh. "
        "Covers hospital names, locations (districts, cities), bed counts, doctor counts, "
        "ICU availability, facility types, ownership types (public/private), "
        "and contact information. "
        "Example: 'How many hospitals are in Dhaka?', 'List hospitals with ICU facilities', "
        "'Top hospitals in Chattogram', 'Hospitals with more than 500 beds'"
    )
