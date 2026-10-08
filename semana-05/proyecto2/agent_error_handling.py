# imports
from dotenv import load_dotenv
from anthropic import Anthropic
import csv
import os
import time
import subprocess

load_dotenv()
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

def search_in_csv(criteria, quantity):
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

def run_agent(user_message):
    system_prompt = "You are a helpful assistant that searches products, calculates discounts, and saves reports. " \
    "Always save the final report without asking."
    messages = [{"role" : "user", "content": user_message}]
    turns = 0
    max_turns = 10

    total_input_tokens = 0
    total_output_tokens = 0

    while turns < max_turns:
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

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        texts = [b for b in response.content if b.type == "text"]

        for text in texts:
            print(f"\nClaude: {text.text}")

        if not tool_uses:
            messages.append({
                "role" : "assistant",
                "content" : response.content
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
            print(f"Input tokens: {total_input_tokens}")
            print(f"Output tokens: {total_output_tokens}")
            print(f"Total tokens: {total_input_tokens + total_output_tokens}")

            break

        messages.append({"role" : "assistant", "content" : response.content})

        tool_results = []

        for tool_use in tool_uses:
            print(f"\nExecuting: {tool_use.name} with {tool_use.input}")

            try:
                result = execute_tool(tool_use.name, tool_use.input)
                is_error = False

            except Exception as e:
                result = f"Tool failed: {str(e)}"
                is_error = True

            print(f"Result: {result}\n")

            log.append({
                "turn": turns,
                "tool_name": tool_use.name,
                "tool_input": tool_use.input,
                "tool_result": result,
                "is_error": is_error,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            })

            tool_results.append({
                "type" : "tool_result",
                "tool_use_id" : tool_use.id,
                "content" : result,
                "is_error": is_error
            })

        messages.append({"role" : "user", "content" : tool_results})

if __name__ == "__main__":
    print(f"\nChained Task Agent - Searches, Calculates and Saves\n")
    
    while True:
            user_input = input("What do you want to do?: ")

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            try:
                run_agent(user_input)
            except Exception as e:
                print(f"\n❌ Error in agent: {e}")
                log.append({
                    "event": "agent_error",
                    "error": str(e)
                })
    
    print("\n\n=== SESSION LOG ===")
    for entry in log:
        print(entry)