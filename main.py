# Step 1: Ask if user has a project
def get_project():
    print("Do you have a project? (yes/no)")
    response = input().lower()
    if response == "yes":
        # Project list could come from a database
        print("Select your project: [Project A, Project B]")
        selected_project = input("Enter project name: ")
        return selected_project
    else:
        print("Continuing without project...")
        return None

# Step 2: Select a product
def select_product():
    print("Select a product to modify: [Product X, Product Y, Product Z]")
    product = input("Enter product name: ")
    return product

# Step 3: Modify product price
def modify_price(product):
    print(f"Which price of '{product}' would you like to modify? (e.g., retail, wholesale)")
    price_type = input("Price type: ").lower()
    
    raw_input = input(f"Enter new {price_type} price (e.g., 10 or $10): ")
    cleaned_price = raw_input.replace("$", "").strip()  # Removes dollar sign
    new_price = float(cleaned_price)
    
    # In actual implementation, here we would update in DB
    print(f"{price_type.capitalize()} price of {product} updated to ${new_price}")

# MAIN FLOW FOR MODIFY PRICE
def modify_price_flow():
    project = get_project()
    product = select_product()
    modify_price(product)

# Step 1: Ask for project (reuse)
#Already defined: get_project()

# Step 2: Select a product (reuse)
# Already defined: select_product()

# Step 3: Get rollout date
def get_rollout_date():
    print("Enter the rollout (launch) date for the new version (YYYY-MM-DD):")
    date = input("Date: ")
    return date

# Step 4: Create new product version
def create_new_version(product, rollout_date):
    # In real application: clone product data, apply changes
    print(f"Creating new version of {product}...")
    print(f"New version scheduled for rollout on {rollout_date}")
    # Save to DB (simulated)
    print("New version created successfully.")

# MAIN FLOW FOR NEW PRODUCT VERSION
def create_new_product_version_flow():
    project = get_project()
    product = select_product()
    rollout_date = get_rollout_date()
    create_new_version(product, rollout_date)

print("Choose an option:")
print("1. Modify Product Price")
print("2. Create New Product Version")
choice = input("Enter choice (1/2): ")

if choice == "1":
    modify_price_flow()
elif choice == "2":
    create_new_product_version_flow()
else:
    print("Invalid choice.")
