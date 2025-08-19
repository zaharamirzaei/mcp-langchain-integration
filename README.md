# MCP-LangChain Server & Client

This repository contains a **Food Services MCP server** and a **LangChain-based client** that interact via the [MCP protocol](https://modelcontextprotocol.io/).
The project demonstrates how to build custom MCP tools (for food ordering services) and integrate them into a conversational assistant powered by **LangChain** and **OpenAI**.

---

## 📚 Project Structure

```
.
├── server.py         # MCP server exposing food-related tools
├── food_client.py    # LangChain client connecting to MCP server
├── db_manager.py     # Database manager (order handling, search, etc.)
├── .env              # Environment variables (API keys)
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## ⚙️ Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/mcp-langchain-server-client.git
   cd mcp-langchain-server-client
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac
   .venv\Scripts\activate     # On Windows

   pip install -r requirements.txt
   ```

3. **Set environment variables**
   Create a `.env` file and add your OpenAI key:

   ```env
   OPENAI_API_KEY=sk-xxxxxxx
   ```

---

## 🚀 Running the Server

The MCP server exposes tools like `food_search`, `cancel_order`, `comment_order`, and `check_order_status`.

```bash
python server.py
```

By default, it runs on **stdio transport**.

---

## 💬 Running the Client

The client connects to the server and provides a **CLI-based Food Assistant** using LangChain.

```bash
python food_client.py
```

Example interaction:

```
Food Assistant Chat (type 'exit' to quit)

You: search for pizza
Assistant: Found results: Pizza Margherita at Local Restaurant (2km away)

You: check status of order 12
Assistant: Order #12 is currently being prepared.
```

---

## 🛠️ Tools Provided

1. **food\_search(food\_name, restaurant\_name, max\_distance)** → Search for foods/restaurants.
2. **cancel\_order(order\_id, phone\_number)** → Cancel an order (if in preparation).
3. **comment\_order(order\_id, person\_name, comment)** → Add or overwrite a comment.
4. **check\_order\_status(order\_id)** → Check the status of an order.

---

## 📌 Requirements

* Python 3.10+
* OpenAI API key
* Dependencies listed in `requirements.txt`
