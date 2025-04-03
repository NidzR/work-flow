from langgraph.workflow import StateGraph

# Define the state interface as a Python class
class State:
    def __init__(self, has_project=None, selected_product=None, new_price=None, rollout_date=None, current_flow=None):
        self.has_project = has_project
        self.selected_product = selected_product
        self.new_price = new_price
        self.rollout_date = rollout_date
        self.current_flow = current_flow

# Nodes for each step of the flow

# Ask if the user has a project
async def askProjectStatus(state: State):
    import prompt_toolkit
    prompt = prompt_toolkit.prompt
    has_project = prompt("Do you have a project? (yes/no): ").lower().strip() == "yes"
    return {"has_project": has_project}

# Ask the user to select a product
async def selectProduct(state: State):
    import prompt_toolkit
    prompt = prompt_toolkit.prompt
    products = ["Product A", "Product B", "Product C"]
    print(f"Available products: {products}")
    selected_product = prompt("Select a product: ").strip()
    return {"selected_product": selected_product}

# Modify the price of the selected product
async def modifyPrice(state: State):
    import prompt_toolkit
    prompt = prompt_toolkit.prompt
    price_input = prompt("Enter new price (numbers only): ").strip()
    clean_price = "".join(c for c in price_input if c == '.' or c.isdigit())
    try:
        new_price = float(clean_price)
    except ValueError:
        print("Invalid price! Please enter numbers only (e.g., 30 or 29.99)")
        return

    return {"new_price": new_price}

# Get the rollout date for a new product version
async def getRolloutDate(state: State):
    import prompt_toolkit
    prompt = prompt_toolkit.prompt
    rollout_date = prompt("Enter rollout date (YYYY-MM-DD): ")
    return {"rollout_date": rollout_date}

# Routing function to handle which step should come next based on the current flow
def routeFlows(state: State) -> str:
    if state.current_flow == "modify_price":
        return "ask_project"  # Start with asking if the user has a project
    elif state.current_flow == "create_version":
        return "ask_project"  # Ask if the user has a project for creating a new version
    else:
        return "END"

# Conditional routing for skipping steps based on user responses
def checkProjectSkip(state: State) -> str:
    if state.has_project:
        return "select_product"  # If the user has a project, proceed to select a product
    else:
        return "select_product"  # If no project, proceed to product selection anyway

# Graph setup
workflow = StateGraph[State]()  # Correcting the syntax for generic type

# Add nodes to the graph
workflow.addNode("ask_project", askProjectStatus)
workflow.addNode("select_product", selectProduct)
workflow.addNode("modify_price", modifyPrice)
workflow.addNode("get_rollout_date", getRolloutDate)

# Set entry point for the graph
workflow.setEntryPoint("ask_project")

# Define conditional edges (routing between nodes based on state)
workflow.addConditionalEdges(
    "ask_project",
    checkProjectSkip,
    {
        "select_product": "select_product"
    }
)

workflow.addConditionalEdges(
    "select_product",
    lambda state: "modify_price" if state.current_flow == "modify_price" else "get_rollout_date",
    {
        "modify_price": "modify_price",
        "get_rollout_date": "get_rollout_date"
    }
)

# Final edges to exit the graph
workflow.addEdge("modify_price", "END")
workflow.addEdge("get_rollout_date", "END")

# Compile the graph
app = workflow.compile()

# Running the flows
import asyncio  # Ensure asyncio is imported for running async functions

print("\n=== Modify Price Flow ===")
modifyPriceInputs = State(current_flow="modify_price")
asyncio.run(app.invoke(modifyPriceInputs)).then(lambda result: print(
    f"Updated price for {result.selected_product}: ${result.new_price}"
))

print("\n=== Create Version Flow ===")
createVersionInputs = State(current_flow="create_version")
asyncio.run(app.invoke(createVersionInputs)).then(lambda result: print(
    f"New version of {result.selected_product} created with rollout date: {result.rollout_date}"
))
