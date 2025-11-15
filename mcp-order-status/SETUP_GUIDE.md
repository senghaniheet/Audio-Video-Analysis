# Setup Guide - MCP Order Status Project

Complete step-by-step setup guide for the entire project.

## Prerequisites

- Python 3.7+ installed
- Node.js 14+ installed
- npm or yarn installed

## Step 1: Setup Python MCP Server

```bash
cd mcp-order-status/server
pip install -r requirements.txt
```

**Test the server:**
```bash
python order_mcp_server.py "My mobile number is 9876543210 and order ID AMZ12345"
```

Expected output:
```json
{
  "match": true,
  "mobile": "9876543210",
  "order_id": "AMZ12345",
  "status": "Delivered",
  "message": "Order found. Status is Delivered."
}
```

The Excel file (`order_data.xlsx`) will be automatically created with 15 sample orders.

## Step 2: Setup Node.js Backend

```bash
cd mcp-order-status/backend-node
npm install
npm start
```

The server will start on `http://localhost:3000`

**Test the SSE endpoint:**
```bash
curl "http://localhost:3000/api/order-status-stream?text=My%20mobile%20number%20is%209876543210%20and%20order%20ID%20AMZ12345"
```

**Test the REST endpoint:**
```bash
curl -X POST http://localhost:3000/api/order-status \
  -H "Content-Type: application/json" \
  -d '{"text":"My mobile number is 9876543210 and order ID AMZ12345"}'
```

## Step 3: Integrate Angular Service

1. **Copy the service file:**
   - Copy `mcp-order-status/angular/order.service.ts` to your Angular project
   - Place it in `src/app/services/order.service.ts`

2. **Import in your component:**
```typescript
import { OrderService } from './services/order.service';

constructor(private orderService: OrderService) {}
```

3. **Use SSE (Recommended):**
```typescript
checkOrder(text: string) {
  this.orderService.checkOrderStatus(text).subscribe({
    next: (event) => {
      console.log('Event:', event);
      if (event.mobile && event.order_id) {
        // Final result received
        console.log('Mobile:', event.mobile);
        console.log('Order ID:', event.order_id);
        console.log('Status:', event.status);
        console.log('Message:', event.message);
      }
    },
    error: (error) => {
      console.error('Error:', error);
    }
  });
}
```

4. **Or use REST (Alternative):**
```typescript
async checkOrder(text: string) {
  try {
    const result = await this.orderService.checkOrderStatusRest(text);
    console.log('Result:', result);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

## Project Structure

```
mcp-order-status/
├── server/
│   ├── order_mcp_server.py    ✅ Main MCP server
│   ├── excel_loader.py        ✅ Excel handling
│   ├── requirements.txt        ✅ Python deps
│   ├── order_data.xlsx         ✅ Auto-generated
│   └── README.md              ✅ Server docs
│
├── backend-node/
│   ├── server.js               ✅ Express + SSE
│   ├── package.json            ✅ Node deps
│   └── README.md              ✅ Backend docs
│
├── angular/
│   └── order.service.ts       ✅ Angular service
│
├── README.md                   ✅ Main docs
└── SETUP_GUIDE.md             ✅ This file
```

## Verification Checklist

- [ ] Python dependencies installed
- [ ] Excel file auto-generated (15 orders)
- [ ] Python MCP server runs successfully
- [ ] Node.js dependencies installed
- [ ] Node.js backend runs on port 3000
- [ ] SSE endpoint responds correctly
- [ ] REST endpoint responds correctly
- [ ] Angular service integrated
- [ ] Angular can connect to backend

## Common Issues

### Issue 1: Python not found
**Solution:** Ensure Python is in PATH or use full path in `server.js`

### Issue 2: Excel file not created
**Solution:** Check file permissions, ensure write access in `server/` directory

### Issue 3: SSE connection fails
**Solution:** 
- Check CORS settings
- Ensure backend is running
- Check browser console for errors

### Issue 4: Order not found
**Solution:** 
- Verify mobile number and order ID in Excel file
- Check extraction patterns match your input format
- Test Python server directly first

## Next Steps

1. Customize Excel data - Edit `order_data.xlsx` with your own orders
2. Adjust extraction patterns - Modify regex in `order_mcp_server.py`
3. Add more MCP tools - Extend the server with additional functionality
4. Deploy - Set up production environment

## Support

Refer to individual README files:
- [Server README](server/README.md)
- [Backend README](backend-node/README.md)
- [Main README](README.md)

