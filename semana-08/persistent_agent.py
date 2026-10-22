# imports
from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import datetime
from pathlib import Path
import csv
import json
import os
import time
import subprocess
import random

load_dotenv()

STATE_DIR = Path(__file__).parent / "state"
STATE_DIR.mkdir(exist_ok=True)
MAX_TURNS = 10
MAX_RETRIES = 3
BASE_DELAY = 1
REQUIRES_APPROVAL = {"save_report"}
MAX_TOOL_FAILURES = 2

log = []
client = Anthropic()
model = "claude-sonnet-4-5"

tools = [
    {
        "name": "search_in_csv",
        "description": "Search products in CSV by criteria (price_high, price_low, electronics, etc). Returns list of matching results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "criteria": {
                    "type": "string",
                    "enum": ["price_high", "price_low", "electronics", "peripherals", "furniture"],
                    "description": "What to search for"
                },
                "quantity": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "How many results to return"
                }
            },
            "required": ["criteria", "quantity"]
        }
    },
    {
        "name": "calculate_discount",
        "description": "Apply a discount percentage to a list of prices. Returns summary with original total, discount amount, and final total.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prices": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of prices to discount"
                },
                "discount_percent": {
                    "type": "number",
                    "description": "Discount percentage (for example, 20 for 20%)"
                }
            },
            "required": ["prices", "discount_percent"]
        }
    },
    {
        "name": "save_report",
        "description": "Save the final report to a text file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to write"
                },
                "filename": {
                    "type": "string",
                    "description": "Filename to save to (example: report.txt)"
                }
            },
            "required": ["content", "filename"]
        }
    }
]

class TransientToolError(Exception):
    pass

flaky_calls = 0
FLAKY_FAILS = 2   # cuántas veces falla antes de andar

def search_in_csv(criteria, quantity):
    global flaky_calls
    if criteria == "price_low":
        flaky_calls += 1
        if flaky_calls <= FLAKY_FAILS:
            raise TransientToolError("connection timeout")

    if criteria == "furniture":
        raise ValueError("❌ Database connection lost while searching furniture category")

    if criteria == "peripherals":
        return ""

    with open("data.csv") as file:
        reader = csv.DictReader(file)
        results = []
        
        for row in reader:
            price = float(row["price"])
            category = row["category"]

            if criteria == "price_high" and price > 500:
                results.append(row)
            elif criteria == "price_low" and price < 200:
                results.append(row)
            elif criteria == "electronics" and category == "electronics":
                results.append(row)
            elif criteria == "peripherals" and category == "peripherals":
                results.append(row)
            elif criteria == "furniture" and category == "furniture":
                results.append(row)

        results = results[:quantity]

        output = ""

        for product in results:
            product_id = product["id"]
            product_name = product["product"]
            product_price = product["price"]
            product_stock = product["stock"]

            output += f"ID: {product_id} | {product_name} | ${product_price} | {product_stock}\n"
    
    return output

def calculate_discount(prices, discount_percent):
    if not prices or len(prices) == 0:
        raise ValueError("❌ No prices provided. Cannot calculate discount.")
    
    original_total = sum(prices)
    discount_amount = original_total * (discount_percent / 100)
    final_total = original_total - discount_amount

    output = f"Original total: ${original_total:.2f}\n"
    output += f"Discount ({discount_percent}%): ${discount_amount:.2f}\n"
    output += f"Final total: ${final_total:.2f}\n"
    output += f"You saved ${discount_amount:.2f}"
    
    return output

def save_report(content, filename):
    filename = os.path.basename(filename)

    if "electronics" in filename:
        time.sleep(3)

    with open(filename, "w") as file:
        file.write(content)

    subprocess.run(["code", "--reuse-window", filename], check=True)
    return f"✓ Report saved to {filename}"

def execute_tool(tool_name, tool_input):
    if tool_name == "search_in_csv":
        criteria = tool_input.get("criteria")
        quantity = tool_input.get("quantity")
        return search_in_csv(criteria, quantity)

    elif tool_name == "calculate_discount":
        prices = tool_input.get("prices")
        discount_percent = tool_input.get("discount_percent")
        return calculate_discount(prices, discount_percent)

    elif tool_name == "save_report":
        content = tool_input.get("content")
        filename = tool_input.get("filename")
        return save_report(content, filename)

    else:
        return f"Error: Unknown tool '{tool_name}'"

def execute_with_retries(tool_name, tool_input):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return execute_tool(tool_name, tool_input)
        except TransientToolError as e:
            if attempt == MAX_RETRIES:
                raise
            delay = BASE_DELAY * 2 ** attempt + random.uniform(0, 0.5)
            print(f"⚠️  {tool_name} failed ({e}). Retry {attempt + 1}/{MAX_RETRIES} in {delay:.1f}s")
            time.sleep(delay)

def ask_approval(tool_use):
    print(f"\n⚠️  Irreversible action requested: {tool_use.name}")
    for key, value in tool_use.input.items():
        print(f"\n--- {key} ---\n{value}")
    print("-------------")
    answer = input("Approve? (y/n): ")
    return answer.strip().lower() == "y"

def save_state(state):
    path = STATE_DIR / f"{state['run_id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    os.replace(tmp, path)

def load_pending():
    for path in sorted(STATE_DIR.glob("*.json"), reverse=True):
        state = json.loads(path.read_text())
        if state["status"] == "running":
            return state
    return None

def new_state(user_message):
    return {
        "run_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "status": "running",
        "user_message": user_message,
        "turn": 0,
        "messages": [{"role": "user", "content": user_message}],
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "tool_failures": {},
    }

def to_plain(content):
    return [b.model_dump(exclude_none=True) for b in content]

def run_agent(state):
    system_prompt = ("You are a helpful assistant that searches products, calculates discounts, and saves reports. "
        "Save the final report with save_report; the user will be asked to approve it before it is written. "
        "If a tool fails or the user rejects an action, say so plainly. Never invent data to continue.")
    messages = state["messages"]
    turns = state["turn"]

    while turns < MAX_TURNS:
        turns += 1
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            tools=tools,
            messages=messages,
            system=system_prompt
        )

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens

        state["total_input_tokens"] += input_tokens
        state["total_output_tokens"] += output_tokens

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        texts = [b for b in response.content if b.type == "text"]

        for text in texts:
            print(f"\nClaude: {text.text}")

        if not tool_uses:
            messages.append({
                "role": "assistant",
                "content": to_plain(response.content)
            })

            log.append({
                "turn": turns,
                "event": "agent_complete",
                "final_response": texts[0].text if texts else "No text response",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            })

            print("\n=== TOKEN USAGE ===")
            print(f"Input tokens: {state['total_input_tokens']}")
            print(f"Output tokens: {state['total_output_tokens']}")
            print(f"Total tokens: {state['total_input_tokens'] + state['total_output_tokens']}")

            state["status"] = "done"
            state["turn"] = turns
            save_state(state)
            break

        tool_results = []
        failures = state.setdefault("tool_failures", {})   # NUEVO: fallos por tool, guardados en el estado

        for tool_use in tool_uses:
            print(f"\nExecuting: {tool_use.name} with {tool_use.input}")

            approved = None
            blocked = failures.get(tool_use.name, 0) >= MAX_TOOL_FAILURES   

            if not blocked and tool_use.name in REQUIRES_APPROVAL:          
                approved = ask_approval(tool_use)

            if blocked:                                                    
                result = (f"Tool '{tool_use.name}' is disabled for this run after "
                          f"{MAX_TOOL_FAILURES} failures. Do not call it again; tell the user.")
                is_error = True
            elif approved is False:                                         
                result = "Action rejected by the user. Do not retry it; tell the user it was not executed."
                is_error = True
            else:
                try:
                    result = execute_with_retries(tool_use.name, tool_use.input)
                    is_error = False

                except Exception as e:
                    result = f"Tool failed: {str(e)}"
                    is_error = True
                    failures[tool_use.name] = failures.get(tool_use.name, 0) + 1   

            print(f"Result: {result}\n")

            log.append({
                "turn": turns,
                "tool_name": tool_use.name,
                "tool_input": tool_use.input,
                "tool_result": result,
                "is_error": is_error,
                "approved": approved,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            })

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
                "is_error": is_error
            })

        messages.append({"role": "assistant", "content": to_plain(response.content)})
        messages.append({"role": "user", "content": tool_results})
        state["turn"] = turns
        save_state(state)

    if state["status"] == "running":
        state["status"] = "max_turns_reached"
        save_state(state)

if __name__ == "__main__":
    print(f"\nChained Task Agent - Searches, Calculates and Saves\n")

    pending = load_pending()
    if pending:
        answer = input(f"Unfinished run ({pending['run_id']}, turn {pending['turn']}): "
                       f"'{pending['user_message'][:60]}'. Resume? (y/n): ")
        if answer.strip().lower() == "y":
            print(f"[resume] continuing from turn {pending['turn']}")
            try:
                run_agent(pending)
            except Exception as e:
                print(f"\n❌ Error in agent: {e}")
        else:
            pending["status"] = "abandoned"
            save_state(pending)

    while True:
        user_input = input("What do you want to do?: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            state = new_state(user_input)
            save_state(state)
            run_agent(state)
        except Exception as e:
            print(f"\n❌ Error in agent: {e}")
            log.append({
                "event": "agent_error",
                "error": str(e)
            })

    print("\n\n=== SESSION LOG ===")
    for entry in log:
        print(entry)
