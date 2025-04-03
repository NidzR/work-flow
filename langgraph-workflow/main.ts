class MemoryDB {
  private data: Record<string, any> = {};

  set(key: string, value: any) {
    this.data[key] = value;
  }

  get(key: string) {
    return this.data[key];
  }

  all() {
    return this.data;
  }
}

// User input simulate karne ke liye
function prompt(question: string): Promise<string> {
  return new Promise((resolve) => {
    process.stdout.write(question + " ");
    process.stdin.once("data", (data) => {
      resolve(data.toString().trim());
    });
  });
}

// Flow 1: Modify Price
async function modifyPriceFlow(db: MemoryDB) {
  const hasProject = await prompt("Kya aap ke paas koi project hai? (yes/no):");
  
  if (hasProject.toLowerCase() === "no") {
    console.log("Chalen bina project ke continue karte hain.");
  }

  const product = await prompt("Product ka naam likhein:");
  const priceInput = await prompt("Naya price kya hona chahiye? (number):");
  const newPrice = parseFloat(priceInput);

  if (isNaN(newPrice)) {
    console.log("Invalid price number.");
    return;
  }

  db.set(product, { price: newPrice });
  console.log(`✅ ${product} ka price update hogaya: $${newPrice}`);
}

// Flow 2: Create New Product Version
async function createNewVersionFlow(db: MemoryDB) {
  const hasProject = await prompt("Kya aap ke paas koi project hai? (yes/no):");

  if (hasProject.toLowerCase() === "no") {
    console.log("Chalen bina project ke continue karte hain.");
  }

  const product = await prompt("Product ka naam likhein:");
  const rolloutDate = await prompt("Naya rollout date kya hai? (YYYY-MM-DD):");

  const versions = db.get("versions") || [];
  versions.push({ product, rolloutDate });
  db.set("versions", versions);

  console.log(`✅ ${product} ka naya version ban gaya with rollout date: ${rolloutDate}`);
}

// Main function
async function main() {
  const db = new MemoryDB();

  console.log("\n🎯 Welcome to Product Workflow System 🎯");
  console.log("1. Modify Price");
  console.log("2. Create New Product Version");

  const choice = await prompt("Aap kaunsa flow run karna chahtay hain? (1/2):");

  if (choice === "1") {
    await modifyPriceFlow(db);
  } else if (choice === "2") {
    await createNewVersionFlow(db);
  } else {
    console.log("❌ Invalid choice!");
  }

  console.log("\n📦 Current Memory State:");
  console.log(db.all());

  process.exit();
}

main();
