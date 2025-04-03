from typing import TypedDict, Optional, Literal
from datetime import date
from langgraph.graph import END, StateGraph

# State definition (same as before)
class State(TypedDict):
    has_project: Optional[bool]
    selected_product: Optional[str]
    new_price: Optional[float]
    rollout_date: Optional[date]
    current_flow: Optional[Literal["modify_price", "create_version"]]

# Nodes (same as before)
def ask_project_status(state: State):
    has_project = input("Do you have a project? (yes/no): ").lower().strip() == "yes"
    return {"has_project": has_project}

def select_product(state: State):
    products = ["Product A", "Product B", "Product C"]
    print(f"Available products: {products}")
    selected = input("Select a product: ").strip()
    return {"selected_product": selected}

def modify_price(state: State):
    while True:
        price_input = input("Enter new price (numbers only): ").strip()
        # Remove any non-numeric characters except decimal point
        clean_price = ''.join(c for c in price_input if c.isdigit() or c == '.')
        try:
            new_price = float(clean_price)
            return {"new_price": new_price}
        except ValueError:
            print("Invalid price! Please enter numbers only (e.g., 30 or 29.99)")

def get_rollout_date(state: State):
    while True:
        rollout_date = input("Enter rollout date (YYYY-MM-DD): ")
        try:
            return {"rollout_date": date.fromisoformat(rollout_date)}
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")

# Conditional routing (thoda sa modify kiya)
def route_flows(state: State):
    if state["current_flow"] == "modify_price":
        return "ask_project"  # Pehle project poocho
    elif state["current_flow"] == "create_version":
        return "ask_project"  # Pehle project poocho
    else:
        return END

def check_project_skip(state: State):
    if state["has_project"]:
        return "select_product"  # Agar project hai toh product select karo
    else:
        return "select_product"  # Warna bina project ke hi select karo

# Graph setup (Yeh woh part hai jo fix karna hai)
workflow = StateGraph(State)

# Sab nodes add karo
workflow.add_node("ask_project", ask_project_status)
workflow.add_node("select_product", select_product)
workflow.add_node("modify_price", modify_price)
workflow.add_node("get_rollout_date", get_rollout_date)

# Entry point set karo (Yeh zaroori hai!)
workflow.set_entry_point("ask_project")

# Conditional edges add karo
workflow.add_conditional_edges(
    "ask_project",
    check_project_skip,
    {"select_product": "select_product"}
)

workflow.add_conditional_edges(
    "select_product",
    lambda state: "modify_price" if state["current_flow"] == "modify_price" else "get_rollout_date",
    {
        "modify_price": "modify_price",
        "get_rollout_date": "get_rollout_date"
    }
)

# Final edges
workflow.add_edge("modify_price", END)  # Bas itna kaafi hai
workflow.add_edge("get_rollout_date", END)  # Yahan bhi khatam

# Graph compile karo
app = workflow.compile()

# Chalane ka tarika (Thoda sa change kiya)
print("\n=== Modify Price Flow ===")
inputs = {"current_flow": "modify_price"}
result = app.invoke(inputs)
print(f"Updated price: {result['selected_product']} -> ${result['new_price']}")

print("\n=== Create Version Flow ===")
inputs = {"current_flow": "create_version"}
result = app.invoke(inputs)
print(f"New version: {result['selected_product']} for {result['rollout_date']}")
# print(f"Updated price: {result['selected_product']} -> ${result['new_price']:.2f}")