from dotenv import load_dotenv
from anthropic import Anthropic
import requests
import os
from datetime import datetime, timedelta

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

tools = [
    {
        "name": "get_weather_miami",
        "description": "Get the current weather in Miami for this weekend",
        "input_schema": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "enum": ["friday", "saturday", "sunday"],
                    "description": "Day of the weekend"
                }
            },
            "required": ["day"]
        }
    },
    {
        "name": "get_miami_events",
        "description": "Get the available events for this weekend in Miami",
        "input_schema": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "enum": ["friday", "saturday", "sunday"],
                    "description": "Day of the weekend"
                },
                "category": {
                    "type": "string",
                    "enum": ["music", "sports", "beach"],
                    "description": "Event category"
                }
            },
            "required": ["day", "category"]
        }
    },
    {
        "name": "get_traffic_forecast",
        "description": "Get the expected traffic for this weekend in Miami",
        "input_schema": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "enum": ["friday", "saturday", "sunday"],
                    "description": "Day of the weekend"
                },
                "time_of_day": {
                    "type": "string",
                    "enum": ["morning", "afternoon", "evening", "night"],
                    "description": "Time of day"
                }
            },
            "required": ["day", "time_of_day"]
        }
    }
]


def execute_tool(tool_name, tool_input):
    """Execute every tool with real APIs or simulated patterns."""
    if tool_name == "get_weather_miami":
        return get_weather_miami(tool_input.get("day"))

    elif tool_name == "get_miami_events":
        day = tool_input.get("day")
        category = tool_input.get("category")
        return get_miami_events(day, category)

    elif tool_name == "get_traffic_forecast":
        day = tool_input.get("day")
        time_of_day = tool_input.get("time_of_day")
        return get_traffic_forecast(day, time_of_day)

    else:
        return f"Error: Unknown tool '{tool_name}'"


def get_weather_miami(day):
    """
    Real call to Open-Meteo
    Miami coords: 25.76°N, -80.19°W
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": 25.76,
            "longitude": -80.19,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
            "temperature_unit": "celsius",
            "timezone": "America/New_York"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        today = datetime.now()

        day_map = {
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }

        target_weekday = day_map[day.lower()]

        days_ahead = (target_weekday - today.weekday()) % 7
        target_date = (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        daily = data["daily"]
        idx = daily["time"].index(target_date)

        temp_max = daily["temperature_2m_max"][idx]
        temp_min = daily["temperature_2m_min"][idx]
        precip = daily["precipitation_sum"][idx]
        weather_code = daily["weather_code"][idx]

        weather_desc = interpret_weather_code(weather_code)

        return f"{day.capitalize()}: {temp_max}°C / {temp_min}°C, {weather_desc}. Precipitation: {precip}mm"

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


def get_miami_events(day, category):
    """
    Real call to Ticketmaster API
    Searches for events in Miami for the specified day and category
    """
    try:
        api_key = os.getenv("TICKETMASTER_API_KEY")

        if not api_key:
            return "Error: TICKETMASTER_API_KEY not found in .env"

        today = datetime.now()
        day_map = {"friday": 4, "saturday": 5, "sunday": 6}
        target_weekday = day_map.get(day.lower(), 4)

        days_ahead = (target_weekday - today.weekday()) % 7
        event_date = today + timedelta(days=days_ahead)

        # Map category to Ticketmaster classification
        category_map = {
            "music": "music",
            "sports": "sports",
            "beach": "outdoors"
        }
        tm_category = category_map.get(category.lower(), "all")

        url = "https://app.ticketmaster.com/discovery/v2/events"
        params = {
            "apikey": api_key,
            "city": "Miami",
            "startDateTime": event_date.strftime("%Y-%m-%dT00:00:00Z"),
            "endDateTime": event_date.strftime("%Y-%m-%dT23:59:59Z"),
            "size": 5
        }

        if tm_category != "all":
            params["classificationName"] = tm_category

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "_embedded" not in data or "events" not in data["_embedded"]:
            return f"No events found in Miami for {day}."

        events = data["_embedded"]["events"]
        event_list = []

        for event in events[:5]:
            name = event.get("name", "Unknown")
            classifications = event.get("classifications", [])
            catg = classifications[0].get("segment", {}).get("name", "Event") if classifications else "Event"
            event_list.append(f"- {name} ({catg})")

        return f"Events in Miami on {day}:\n" + "\n".join(event_list)

    except Exception as e:
        return f"Error fetching events: {str(e)}"


def get_traffic_forecast(day, time_of_day):
    """
    Realistic pattern simulating traffic in Miami.
    Not a real API, but Claude can use it.
    """
    traffic_patterns = {
        "friday": {
            "morning": "Light traffic. I-95 north flows smoothly. Best time to move around.",
            "afternoon": "Moderate traffic building up. I-95 starts congesting around 3pm.",
            "evening": "HEAVY traffic. I-95 gridlock, Brickell congested. 45-60 min delays expected.",
            "night": "Moderate traffic. Delays decreasing after 8pm."
        },
        "saturday": {
            "morning": "Light to moderate. Weekend traffic lighter than weekdays.",
            "afternoon": "Moderate. Beach-bound traffic on A1A. I-95 manageable.",
            "evening": "Moderate. Saturday night traffic, bar/restaurant areas busy.",
            "night": "Light. Flows smoothly after 11pm."
        },
        "sunday": {
            "morning": "Light. Sunday morning is relaxed in Miami.",
            "afternoon": "Moderate. People returning from beach/events. Expect some delays.",
            "evening": "Heavy returning traffic from weekend activities. I-95 congested 5-8pm.",
            "night": "Light. Evening settles down."
        }
    }

    day_lower = day.lower()
    time_lower = time_of_day.lower()

    if day_lower in traffic_patterns and time_lower in traffic_patterns[day_lower]:
        return f"{day} {time_lower}: {traffic_patterns[day_lower][time_lower]}"
    else:
        return f"Traffic info not available for {day} {time_lower}."


def interpret_weather_code(code):
    """Interpret WMO weather codes."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Fog",
        51: "Light drizzle",
        61: "Slight rain",
        71: "Slight snow",
        80: "Violent rain showers",
        95: "Thunderstorm"
    }
    return codes.get(code, "Unknown weather")

def run_agent(user_message, messages):
    """Run the agent to plan my weekend in Miami."""

    turns = 0
    max_turns = 10

    messages.append({"role" : "user", "content" : user_message})

    while turns < max_turns:
        turns += 1
        print(f"\n===== TURN {turns} =====")

        # Here, call Claude
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        texts = [b for b in response.content if b.type == "text"]

        # print Claude's response
        for text in texts:
            print(f"Claude: {text.text}")

        if not tool_uses:
            # "If no tools were used, end"
            messages.append({
                "role" : "assistant",
                "content" : response.content
            })
            break

        # add Claude's response to history
        messages.append({"role" : "assistant", "content" : response.content})

        # execute tools
        tool_results = []
        for tool_use in tool_uses:
            print(f" Executing: {tool_use.name} with {tool_use.input}")
            result = execute_tool(tool_use.name, tool_use.input)
            print(f" Result: {result}\n")

            tool_results.append({
                "type" : "tool_result",
                "tool_use_id" : tool_use.id,
                "content" : result
            })

        # add results to history
        messages.append({"role" : "user", "content" : tool_results})

        if turns >= max_turns:
            print(f"\n✗ Max {max_turns} turns reached")
            break

if __name__ == "__main__":
    print("\nMiami Weekend Planner Agent\n")

    messages = []

    while True:
        user_input = input("Plan your weekend in Miami (or type 'exit' to quit): ")

        if user_input.lower() == "exit":
            print("\n✓ Agent finished")
            print("Goodbye! Have a nice weekend.")
            break
        run_agent(user_input, messages)