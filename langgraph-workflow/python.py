import prompt_toolkit
from prompt_toolkit import prompt
# Import prompt_toolkit for user input
# Initialize prompt_toolkit for taking user input
# Removed incorrect promptSync usage as it is not applicable in Python

# Step 1: Ask if user has a project
def get_project():
    response = prompt("Do you have a project? (yes/no): ").lower().strip()
    if response == "yes":
        selected_project = prompt("Select your project: [Project A, Project B]: ").strip()
        return selected_project
    else:
        print("Continuing without project...")
        return None

# Step 2: Select a product
def select_product():
    product = prompt("Select a product to modify: [Product X, Product Y, Product Z]: ").strip()
    return product

# Step 3: Modify product price
def modify_price(product: str) -> None:
    price_type = prompt(f"Which price of '{product}' would you like to modify? (e.g., retail, wholesale): ").lower().strip()
    
    raw_input = prompt(f"Enter new {price_type} price (e.g., 10 or $10): ")
    cleaned_price = raw_input.replace("$", "").strip()  # Removes dollar sign
    
    try:
        new_price = float(cleaned_price)
    except ValueError:
        print("Invalid price! Please enter numbers only (e.g., 30 or 29.99)")
        return

    print(f"{price_type.capitalize()} price of {product} updated to ${new_price}")


# MAIN FLOW FOR MODIFY PRICE
def modify_price_flow():
    project = get_project()
    product = select_product()
    # Call modify_price if needed
    modify_price(product)

# Step 1: Ask for project (reuse)
def get_rollout_date():
    rollout_date = prompt("Enter the rollout (launch) date for the new version (YYYY-MM-DD): ")
    return rollout_date

# Step 2: Create new product version
def create_new_version(product, rollout_date):
    print(f"Creating new version of {product}...")
    print(f"New version scheduled for rollout on {rollout_date}")
    print("New version created successfully.")

# MAIN FLOW FOR NEW PRODUCT VERSION
def create_new_product_version_flow():
    project = get_project()
    product = select_product()
    rollout_date = get_rollout_date()
    create_new_version(product, rollout_date)

# Main Menu to choose the flow
def main():
    print("Choose an option:")
    print("1. Modify Product Price")
    print("2. Create New Product Version")
    choice = prompt("Enter choice (1/2): ").strip()

    if choice == "1":
        modify_price_flow()
    elif choice == "2":
        create_new_product_version_flow()
    else:
        print("Invalid choice.")

# Call main function to start
if __name__ == "__main__":
    main()
