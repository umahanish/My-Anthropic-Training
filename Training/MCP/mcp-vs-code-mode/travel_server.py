# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp==2.3.0"]
# ///
"""One real MCP server (stdio) used by BOTH demos.

Demo 1 (classic MCP): Claude calls these tools one by one.
Demo 2 (Code Mode):   Claude writes TypeScript that calls them inside a sandbox.
"""

from typing import TypedDict

from mcp.server import MCPServer

mcp = MCPServer("travel")

OFFICES = ["Chennai", "Bengaluru", "Mumbai", "Delhi", "London", "Tokyo", "Singapore", "Dubai"]
WEATHER = {
    "Chennai": (33, "humid"), "Bengaluru": (24, "cloudy"), "Mumbai": (31, "rain"),
    "Delhi": (27, "haze"), "London": (12, "rain"), "Tokyo": (18, "clear"),
    "Singapore": (30, "thunderstorms"), "Dubai": (35, "clear"),
}


# Typed returns give each tool an outputSchema, so Code Mode can generate accurate interfaces.
class Offices(TypedDict):
    offices: list[str]


class Hour(TypedDict):
    hour: int
    temp_c: int
    humidity: int
    wind_kph: int


class Weather(TypedDict):
    city: str
    temp_c: int
    condition: str
    hourly: list[Hour]


class Booking(TypedDict):
    status: str
    destination: str
    date: str
    pnr: str


@mcp.tool()
def list_offices() -> Offices:
    """List the cities where the company has offices. Returns {"offices": [city, ...]}."""
    return {"offices": OFFICES}


@mcp.tool()
def get_weather(city: str) -> Weather:
    """Get weather for one city: current temp_c, condition, and a 24-hour hourly forecast."""
    temp, cond = WEATHER.get(city, (25, "sunny"))
    # Real weather APIs return bulky payloads like this; classic MCP pushes all of it through the model.
    hourly = [{"hour": h, "temp_c": temp + (h % 6) - 3, "humidity": 60 + h, "wind_kph": 8 + h % 5} for h in range(24)]
    return {"city": city, "temp_c": temp, "condition": cond, "hourly": hourly}


@mcp.tool()
def book_flight(destination: str, date: str) -> Booking:
    """Book a flight to a destination on a date (YYYY-MM-DD). Returns the booking reference."""
    return {"status": "BOOKED", "destination": destination, "date": date, "pnr": f"PNR-{destination[:3].upper()}42"}


if __name__ == "__main__":
    mcp.run()  # stdio
