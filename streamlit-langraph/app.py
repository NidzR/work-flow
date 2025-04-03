import streamlit as st
from langgraph.graph import StateGraph
from typing import Dict, Any
from datetime import date

# Memory store
memory: Dict[str, Any] = {}

# Shared state class
class ProductState(dict):
    pass

# Flow 1: Modify Price
def modify_price(state: ProductState):
    print("Running modify_price function")  # Log for debugging
    product = state.get("product")
    price = state.get("price")
    if not product or price is None:
        state["message"] = "Error: Missing product or price."
        return state
    memory[product] = {"price": price}
    state["message"] = f"Updated price of {product} to ${price}."
    print(f"State after modify_price: {state}")  # Log the state
    return state

# Flow 2: Create New Version
def create_version(state: ProductState):
    print("Running create_version function")  # Log for debugging
    product = state.get("product")
    rollout_date = state.get("rollout")
    if not product or not rollout_date:
        state["message"] = "Error: Missing product or rollout date."
        return state
    if "versions" not in memory:
        memory["versions"] = []
    memory["versions"].append({"product": product, "rollout": rollout_date})
    state["message"] = f"New version of {product} created for rollout on {rollout_date}."
    print(f"State after create_version: {state}")  # Log the state
    return state

# Build Graph
def build_graph(flow_type):
    print(f"Building graph for flow: {flow_type}")  # Log for debugging
    builder = StateGraph(ProductState)
    if flow_type == "Modify Price":
        builder.add_node("modify_price", modify_price)
        builder.set_entry_point("modify_price")
        builder.set_finish_point("modify_price")
    else:
        builder.add_node("create_version", create_version)
        builder.set_entry_point("create_version")
        builder.set_finish_point("create_version")
    return builder.compile()

# --- Streamlit UI ---
st.title("🛠️ Product Workflow App")
flow_type = st.selectbox("Select Flow", ["Modify Price", "Create New Product Version"])

product = st.text_input("Product Name")
price = 0  # Default price
rollout = None  # Default for rollout date

if flow_type == "Modify Price":
    price = st.number_input("Enter New Price", step=1, min_value=0)
else:
    rollout = st.date_input("Enter Rollout Date", min_value=date.today())

state = ProductState()  # Initialize state with a default value

if st.button("🚀 Run Workflow"):
    state = ProductState(product=product)
    if flow_type == "Modify Price":
        state["price"] = price
    else:
        if rollout:
            state["rollout"] = rollout.strftime("%Y-%m-%d")

    graph = build_graph(flow_type)
    
    try:
        result = graph.invoke(state)
        print(f"Result after invoke: {result}")  # Log result for debugging
        if result and "message" in result:
            st.success(result["message"])
        else:
            st.error("Error: No valid result returned.")
            st.write("State was:", state)  # Log state for debugging
    except Exception as e:
        st.error(f"Error during graph invocation: {e}")

# Show memory state and current state
st.subheader("📦 Memory State")
st.json(memory)
st.subheader("🧠 Current State")
st.json(state)
