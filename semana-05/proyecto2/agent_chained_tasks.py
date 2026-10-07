from dotenv import load_dotenv
from anthropic import Anthropic
import csv
import os

load_dotenv()

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
    
    with open(filename, "w") as file:
        file.write(content)
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

    while turns < max_turns:
        turns += 1
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            tools=tools,
            messages=messages,
            system=system_prompt
        )

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        texts = [b for b in response.content if b.type == "text"]

        for text in texts:
            print(f"\nClaude: {text.text}")

        if not tool_uses:
            messages.append({
                "role" : "assistant",
                "content" : response.content
            })
            break

        messages.append({"role" : "assistant", "content" : response.content})

        tool_results = []
        for tool_use in tool_uses:
            print(f"\nExecuting: {tool_use.name} with {tool_use.input}")
            result = execute_tool(tool_use.name, tool_use.input)
            print(f"Result: {result}\n")

            tool_results.append({
                "type" : "tool_result",
                "tool_use_id" : tool_use.id,
                "content" : result
            })

        messages.append({"role" : "user", "content" : tool_results})

if __name__ == "__main__":
    print(f"\nChained Task Agent - Searches, Calculates and Saves\n")
    user_input = input("What do you want to do?: ")
    run_agent(user_input)
          
        