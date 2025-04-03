# work-flow
 langraph
#python.py fil ka output 
{python python.py}
Choose an option:
1. Modify Product Price
2. Create New Product Version
Enter choice (1/2): 1
Do you have a project? (yes/no): yes
Select your project: [Project A, Project B]: B
Select a product to modify: [Product X, Product Y, Product Z]: Z
Which price of 'Z' would you like to modify? (e.g., retail, wholesale): retail
Enter new retail price (e.g., 10 or $10): 20
Retail price of Z updated to $20.0
{python python.py}
Choose an option:
1. Modify Product Price
2. Create New Product Version
Enter choice (1/2): 2
Do you have a project? (yes/no): no
Continuing without project...
Select a product to modify: [Product X, Product Y, Product Z]: Z
Enter the rollout (launch) date for the new version (YYYY-MM-DD): 2024-03-04
Creating new version of Z...
New version scheduled for rollout on 2024-03-04
New version created successfully.
{app.py}
same results
{main.ts}
npm install -g typescript
npm install prompt-sync
tsc main.ts
node main.js
npm install -g typescript
npm install prompt-sync
tsc main.ts
node main.js
result like ::::
🎯 Welcome to Product Workflow System 🎯
1. Modify Price
2. Create New Product Version
Aap kaunsa flow run karna chahtay hain? (1/2): 1
Kya aap ke paas koi project hai? (yes/no): yes
Product ka naam likhein: Product A
Naya price kya hona chahiye? (number): 25
✅ Product A ka price update hogaya: $25

📦 Current Memory State:
{ 'Product A': { price: 25 } }
