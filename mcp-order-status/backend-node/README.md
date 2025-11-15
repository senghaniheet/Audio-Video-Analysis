# Node.js Backend - MCP Order Status

Express server with Server-Sent Events (SSE) for streaming order status results.

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

Or with auto-reload (development):
```bash
npm run dev
```

Server runs on `http://localhost:3000`

## Endpoints

### 1. SSE Endpoint (Streaming)

```
GET /api/order-status-stream?text=YOUR_TEXT
```

**Response:** Server-Sent Events stream

**Events:**
- `processing` - Initial processing stage
- `extracting_keywords` - Extracting mobile number and order ID
- `excel_lookup` - Searching in Excel database
- `final_result` - Final result with complete data
- `error` - Error occurred

**Example:**
```javascript
const eventSource = new EventSource(
  'http://localhost:3000/api/order-status-stream?text=My%20mobile%20number%20is%209876543210%20and%20order%20ID%20AMZ12345'
);

eventSource.addEventListener('final_result', (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
  // {
  //   "mobile": "9876543210",
  //   "order_id": "AMZ12345",
  //   "status": "Delivered",
  //   "message": "Order found. Status is Delivered."
  // }
});
```

### 2. REST Endpoint (Non-Streaming)

```
POST /api/order-status
Content-Type: application/json

{
  "text": "My mobile number is 9876543210 and order ID AMZ12345"
}
```

**Response:**
```json
{
  "mobile": "9876543210",
  "order_id": "AMZ12345",
  "status": "Delivered",
  "message": "Order found. Status is Delivered."
}
```

### 3. Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "MCP Order Status Backend"
}
```

## How It Works

1. Receives text from Angular frontend
2. Calls Python MCP Server via subprocess
3. Streams progress events via SSE
4. Returns final result with order status

## Python Integration

The backend calls the Python MCP server located at:
```
../server/order_mcp_server.py
```

Make sure Python is installed and the MCP server is accessible.

## CORS

CORS is enabled for all origins. In production, configure allowed origins:

```javascript
app.use(cors({
  origin: 'http://localhost:4200' // Your Angular app
}));
```

## Error Handling

Errors are sent as SSE events:
```javascript
eventSource.addEventListener('error', (event) => {
  const data = JSON.parse(event.data);
  console.error(data.error);
});
```

## Testing

### Test SSE Endpoint
```bash
curl "http://localhost:3000/api/order-status-stream?text=My%20mobile%20number%20is%209876543210%20and%20order%20ID%20AMZ12345"
```

### Test REST Endpoint
```bash
curl -X POST http://localhost:3000/api/order-status \
  -H "Content-Type: application/json" \
  -d '{"text":"My mobile number is 9876543210 and order ID AMZ12345"}'
```

## Environment Variables

- `PORT` - Server port (default: 3000)
- `PYTHON_PATH` - Python executable path (default: 'python')

## Troubleshooting

**Issue:** Python process not found
- **Solution:** Ensure Python is in PATH or update spawn command in `server.js`

**Issue:** MCP server file not found
- **Solution:** Check that `../server/order_mcp_server.py` exists

**Issue:** SSE connection closes immediately
- **Solution:** Check browser console for errors, ensure CORS is configured

