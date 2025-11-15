# MCP Order Status Server

Python-based MCP Server for checking order status from transcribed audio/text.

## Structure

```
/server/
  ├── order_mcp_server.py    # Main MCP server implementation
  ├── excel_loader.py         # Excel file handling
  ├── requirements.txt        # Python dependencies
  ├── order_data.xlsx         # Auto-generated Excel file (created on first run)
  └── README.md               # This file
```

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python order_mcp_server.py
```

The Excel file (`order_data.xlsx`) will be automatically created on first run with 15 sample orders.

## MCP Tool: `orderStatusChecker`

### Input
- **text** (string): Transcribed audio or text containing mobile number and order ID

### Output
JSON response with one of the following formats:

**If both mobile and order ID found and match:**
```json
{
  "match": true,
  "mobile": "9876543210",
  "order_id": "AMZ12345",
  "status": "Delivered",
  "message": "Order found. Status is Delivered."
}
```

**If not found in database:**
```json
{
  "match": false,
  "mobile": "9876543210",
  "order_id": "AMZ12345",
  "status": null,
  "message": "Mobile or Order ID not found in records."
}
```

**If mobile/order ID not detected:**
```json
{
  "match": false,
  "mobile": null,
  "order_id": null,
  "status": null,
  "message": "I could not find a mobile number or order ID in your message."
}
```

## Excel File Format

The `order_data.xlsx` file contains:

| Column | Description | Example |
|--------|-------------|---------|
| mobile_number | 10-digit mobile number | 9876543210 |
| order_id | Alphanumeric order ID | AMZ12345 |
| order_status | Order status | Delivered, Shipped, Out for Delivery, Processing |

## Extraction Patterns

### Mobile Number
- "My mobile number is 9876543210"
- "9876543210"
- "987-654-3210" or "987 654 3210"

### Order ID
- "My order ID is AMZ12345"
- "order AMZ12345"
- "AMZ12345"
- "MZ12345"

## Usage Example

```python
from order_mcp_server import OrderMCPServer

server = OrderMCPServer()
result = server.orderStatusChecker("My mobile number is 9876543210 and order ID AMZ12345")
print(result)
```

## Testing

Test the server directly:
```bash
python order_mcp_server.py "My mobile number is 9876543210 and order ID AMZ12345"
```

Or test with default example:
```bash
python order_mcp_server.py
```

