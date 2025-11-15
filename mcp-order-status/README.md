# MCP Order Status Project

Complete MCP Server project for order status checking with Excel-based lookup, Node.js SSE backend, and Angular integration.

## Project Structure

```
/mcp-order-status/
  ├── /server/                    # Python MCP Server
  │   ├── order_mcp_server.py     # Main MCP server
  │   ├── excel_loader.py          # Excel file handling
  │   ├── requirements.txt        # Python dependencies
  │   ├── order_data.xlsx         # Auto-generated Excel (15 orders)
  │   └── README.md               # Server documentation
  │
  ├── /backend-node/              # Node.js Backend with SSE
  │   ├── server.js                # Express server with SSE endpoint
  │   ├── package.json             # Node.js dependencies
  │   └── README.md                # Backend documentation
  │
  ├── /angular/                    # Angular Service
  │   └── order.service.ts         # SSE client service
  │
  └── README.md                    # This file
```

## Quick Start

### 1. Python MCP Server

```bash
cd server
pip install -r requirements.txt
python order_mcp_server.py
```

The Excel file will be auto-generated on first run.

### 2. Node.js Backend

```bash
cd backend-node
npm install
npm start
```

Server runs on `http://localhost:3000`

### 3. Angular Integration

Copy `angular/order.service.ts` to your Angular project and inject it:

```typescript
import { OrderService } from './services/order.service';

constructor(private orderService: OrderService) {}

// Use SSE
this.orderService.checkOrderStatus(text).subscribe(event => {
  console.log(event);
});

// Or use REST
const result = await this.orderService.checkOrderStatusRest(text);
```

## API Endpoints

### SSE Endpoint
```
GET /api/order-status-stream?text=YOUR_TEXT
```

**Events:**
- `processing` - Processing started
- `extracting_keywords` - Extracting mobile/order ID
- `excel_lookup` - Searching database
- `final_result` - Final result with JSON data

### REST Endpoint (Alternative)
```
POST /api/order-status
Content-Type: application/json

{
  "text": "My mobile number is 9876543210 and order ID AMZ12345"
}
```

## Features

✅ **Auto-Generated Excel** - 15 sample orders created automatically  
✅ **Smart Extraction** - Regex patterns for mobile numbers and order IDs  
✅ **SSE Streaming** - Real-time progress updates  
✅ **Error Handling** - Graceful handling of missing data  
✅ **TypeScript Support** - Full type definitions for Angular  

## Excel Data

The Excel file contains 15 sample orders:

| mobile_number | order_id | order_status |
|---------------|----------|--------------|
| 9876543210 | AMZ12345 | Delivered |
| 9988776655 | AMZ22222 | Shipped |
| ... | ... | ... |

## Response Format

```json
{
  "mobile": "9876543210",
  "order_id": "AMZ12345",
  "status": "Delivered",
  "message": "Order found. Status is Delivered."
}
```

## Requirements

- Python 3.7+
- Node.js 14+
- Angular 12+ (for service integration)

## Dependencies

**Python:**
- openpyxl
- mcp

**Node.js:**
- express
- cors

## Testing

### Test Python Server
```bash
cd server
python order_mcp_server.py "My mobile number is 9876543210 and order ID AMZ12345"
```

### Test Node.js Backend
```bash
curl "http://localhost:3000/api/order-status-stream?text=My%20mobile%20number%20is%209876543210%20and%20order%20ID%20AMZ12345"
```

## Documentation

- [Server README](server/README.md) - Python MCP Server details
- [Backend README](backend-node/README.md) - Node.js SSE backend details

## License

MIT

