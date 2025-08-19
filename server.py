print("Server is starting…")
from typing import Any
from mcp.server.fastmcp import FastMCP
import logging
from db_manager import cancel_order, comment_order, check_order_status, food_search

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("FoodServices")


@mcp.tool()
async def food_search_tool(food_name: str = None, restaurant_name: str = None, max_distance: int = 1) -> str:
    """Search specific food or restaurant in database with edit distance."""
    result = food_search(food_name=food_name, restaurant_name=restaurant_name, max_distance=max_distance)
    return str(result)


@mcp.tool()
async def cancel_order_tool(order_id: int, phone_number: str) -> str:
    """Cancel an order if status is 'preparation'."""
    result = cancel_order(order_id, phone_number)
    return str(result)


@mcp.tool()
async def comment_order_tool(order_id: int, person_name: str, comment: str) -> str:
    """Add or overwrite a comment for an order."""
    result = comment_order(order_id, person_name, comment)
    return str(result)


@mcp.tool()
async def check_order_status_tool(order_id: int) -> str:
    """Check the status of an order."""
    result = check_order_status(order_id)
    return str(result)



if __name__ == "__main__":
    # Run on stdio 
    mcp.run(transport="stdio")
