import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Ensure you have the updated CSS

function App() {
    const [chain, setChain] = useState([]);
    const [newTransaction, setNewTransaction] = useState("");
    const [valid, setValid] = useState(null);

    useEffect(() => {
        fetchChain();
    }, []);

    const fetchChain = async () => {
        const response = await axios.get("http://127.0.0.1:5000/chain");
        setChain(response.data);
    };

    const addBlock = async () => {
        await axios.post("http://127.0.0.1:5000/add_block", { transactions: newTransaction });
        setNewTransaction("");
        fetchChain();
    };

    const validateChain = async () => {
        const response = await axios.get("http://127.0.0.1:5000/validate");
        setValid(response.data.valid);
    };

    return (
        <div className="container">
            <h1>🚀 Blockchain Simulation</h1>
            <input
                type="text"
                placeholder="Enter transaction"
                value={newTransaction}
                onChange={(e) => setNewTransaction(e.target.value)}
            />
            <button className="add" onClick={addBlock}>➕ Add Block</button>
            <button className="validate" onClick={validateChain}>✔️ Validate Blockchain</button>
            {valid !== null && <p className="validation">Blockchain Valid: {valid ? "✅ Yes" : "❌ No"}</p>}

            <h2>Blockchain:</h2>
            <div className="blockchain">
                {chain.map((block, index) => (
                    <div key={block.index} className="block">
                        <h3>🧱 Block {block.index}</h3>
                        <p><b>Transactions:</b> {block.transactions}</p>
                        <p><b>Prev Hash:</b> <span className="hash">{block.previous_hash}</span></p>
                        <p><b>Hash:</b> <span className="hash">{block.hash}</span></p>

                        {index < chain.length - 1 && <div className="connector">🔗</div>}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
