from tools.database_tool_base import DatabaseTool


class RestaurantsDBTool(DatabaseTool):
    name: str = "restaurants_db"
    db_name: str = "restaurants"
    table_name: str = "restaurants"
    description: str = (
        "Use this tool for questions about restaurants, food, cuisine, dining "
        "in Bangladesh. Covers restaurant names, locations (cities, districts), "
        "cuisine types, ratings, price ranges, food categories, and contact details. "
        "Example: 'Top restaurants in Sylhet', 'Restaurants serving biryani in Chattogram', "
        "'Best rated restaurants in Dhaka', 'Restaurants with Chinese cuisine'"
    )
