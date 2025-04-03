import { StateGraph } from '@langchain/langgraph';

// 1. Type Definitions
interface Product {
  id: string;
  name: string;
  price: number;
  currentVersion?: string;
}

interface WorkflowState {
  hasProject: boolean | null;
  selectedProduct: Product | null;
  newPrice: number | null;
  rolloutDate: string | null;
  currentFlow: 'modify_price' | 'create_version' | null;
}

// 2. Mock Database
const products: Product[] = [
  { id: 'prod1', name: 'Product A', price: 100, currentVersion: '1.0' },
  { id: 'prod2', name: 'Product B', price: 200, currentVersion: '2.0' },
  { id: 'prod3', name: 'Product C', price: 300, currentVersion: '3.0' }
];

// 3. Helper Functions
function askQuestion(question: string): Promise<string> {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    readline.question(question, answer => {
      readline.close();
      resolve(answer);
    });
  });
}

function displayProducts() {
  console.log("\nAvailable Products:");
  products.forEach(p => {
    console.log(`- ${p.name} (ID: ${p.id})`);
    console.log(`  Price: $${p.price}`);
    console.log(`  Version: ${p.currentVersion}\n`);
  });
}

// 4. Node Functions
async function askProjectStatus(state: WorkflowState): Promise<Partial<WorkflowState>> {
  const response = await askQuestion("Do you have a project? (yes/no): ");
  return { hasProject: response.toLowerCase() === 'yes' };
}

async function selectProduct(state: WorkflowState): Promise<Partial<WorkflowState>> {
  displayProducts();
  const productId = await askQuestion("Select a product ID: ");
  const product = products.find(p => p.id === productId);
  
  if (!product) throw new Error("Invalid product selection");
  return { selectedProduct: product };
}

async function modifyPrice(state: WorkflowState): Promise<Partial<WorkflowState>> {
  if (!state.selectedProduct) throw new Error("No product selected");
  
  const newPrice = parseFloat(await askQuestion(
    `Current price: ${state.selectedProduct.price}. Enter new price: `
  ));
  
  if (isNaN(newPrice)) throw new Error("Invalid price");
  return { newPrice };
}

async function getRolloutDate(state: WorkflowState): Promise<Partial<WorkflowState>> {
  const date = await askQuestion("Enter rollout date (YYYY-MM-DD): ");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error("Invalid date format");
  return { rolloutDate: date };
}

// 5. Workflow Setup
const END = 'end'; // Define END as a special node name

const workflow = new StateGraph<WorkflowState>({
  initialState: {
    hasProject: null,
    selectedProduct: null,
    newPrice: null,
    rolloutDate: null,
    currentFlow: null
  }
});

// Add all nodes
workflow.addNode('ask_project', askProjectStatus);
workflow.addNode('select_product', selectProduct);
workflow.addNode('modify_price', modifyPrice);
workflow.addNode('get_rollout_date', getRolloutDate);

// Set entry point
workflow.setEntryPoint('ask_project');

// Conditional edges
workflow.addConditionalEdges(
  'ask_project',
  (state) => state.currentFlow === 'modify_price' ? 'modify_price' : 'get_rollout_date'
);

workflow.addEdge('select_product', 'modify_price');
workflow.addEdge('modify_price', END);
workflow.addEdge('get_rollout_date', END);

// 6. Compile and Run
const app = workflow.compile();

async function runWorkflow() {
  console.log("1. Modify Price");
  console.log("2. Create New Version");
  const choice = await askQuestion("Select workflow (1-2): ");

  const initialState: WorkflowState = {
    hasProject: null,
    selectedProduct: null,
    newPrice: null,
    rolloutDate: null,
    currentFlow: choice === '1' ? 'modify_price' : 'create_version'
  };

  console.log(`\n=== Running ${choice === '1' ? 'Modify Price' : 'Create Version'} Flow ===`);
  
  for await (const step of app.stream(initialState)) {
    console.log("Current step:", step);
    
    if (step.newPrice) {
      console.log(`✅ Price updated to $${step.newPrice}`);
    }
    
    if (step.rolloutDate) {
      console.log(`✅ New version scheduled for ${step.rolloutDate}`);
    }
  }
}

runWorkflow().catch(console.error);