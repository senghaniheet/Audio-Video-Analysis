# Excel-Based Order Status System

## Overview

This system replaces the old static order logic with a new Excel-based lookup system that:
- Uses an Excel file with 15 sample records
- Extracts mobile number + order ID from text/audio
- Looks up matching record in Excel (requires BOTH mobile number AND order ID)
- Returns status or appropriate AI message if not found
- Works with both audio and text input

## Files Created/Modified

### 1. Excel File: `data/orders.xlsx`
- **Location**: `backend/data/orders.xlsx`
- **Columns**: MobileNumber, OrderID, CustomerName, OrderStatus, DeliveryDate, LastUpdate
- **Records**: 15 sample orders
- **Creation**: Run `python create_orders_excel.py` in the backend directory

### 2. Order Lookup Module: `order.py`
- **Function**: `check_order_status(mobile_number: str, order_id: str) -> dict`
- **Requirements**: BOTH mobile_number AND order_id are required
- **Returns**: 
  - If found: `{"status_found": True, "customer_name": "...", "order_status": {...}}`
  - If not found: `{"status_found": False, "message": "..."}`

### 3. Updated MCP Server: `services/mcp_server.py`
- **Improved Extraction**: Better prompt for extracting mobile numbers and order IDs
- **Uses order.py**: Calls `check_order_status()` function
- **Requires Both Fields**: Both mobile_number AND order_id must be present for lookup
- **Response Format**: Matches the required API response structure

### 4. Updated Main API: `main.py`
- **Response Format**: Updated to match requirements
- **Error Handling**: Improved error response format

## Setup Instructions

1. **Create Excel File**:
   ```bash
   cd backend
   python create_orders_excel.py
   ```
   This creates `data/orders.xlsx` with 15 sample orders.

2. **Verify Excel File**:
   - Check that `backend/data/orders.xlsx` exists
   - Should contain 15 rows with columns: MobileNumber, OrderID, CustomerName, OrderStatus, DeliveryDate, LastUpdate

3. **Set OpenAI API Key**:
   ```powershell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

4. **Run Backend**:
   ```bash
   python main.py
   ```

## API Response Format

```json
{
  "transcript": "transcribed text",
  "mobile_number": "9876543210",
  "order_id": "AMZ12345",
  "customer_name": "Rahul Sharma",
  "topic": "Order Status Inquiry",
  "intent": "check_status",
  "status_found": true,
  "order_status": {
    "status": "Shipped",
    "delivery_date": "2025-11-20",
    "last_update": "2025-11-15"
  },
  "response_text": "Your order AMZ12345 for Rahul Sharma is Shipped. Expected delivery date: 2025-11-20.",
  "response_voice_text": "Your order AMZ12345 for Rahul Sharma is Shipped. It will be delivered on 20 Nov.",
  "audio_url": "/audio/abc123.mp3"
}
```

## Key Features

### 1. Improved Extraction
- More explicit prompt for finding mobile numbers and order IDs
- Handles various formats:
  - Spoken numbers: "nine eight seven six five four three two one zero"
  - Written digits: "9876543210"
  - Order IDs: "AMZ12345", "A M Z 1 2 3 4 5", etc.
- Lower temperature (0.1) for more consistent extraction
- JSON response format enforcement

### 2. Dual Field Requirement
- **Both mobile_number AND order_id are required** for lookup
- If either is missing, returns appropriate message
- More secure and accurate than single-field lookup

### 3. Excel Lookup
- Uses pandas to read Excel file
- Cleans and normalizes mobile numbers (removes non-digits)
- Case-insensitive order ID matching
- Returns structured order status information

### 4. Response Generation
- Context-aware responses based on lookup results
- Separate text and voice-friendly responses
- Appropriate messages for not-found cases

## Testing

### Test Case 1: Valid Order
- **Mobile**: 9876543210
- **Order ID**: AMZ12345
- **Expected**: Status found, returns order details

### Test Case 2: Invalid Order
- **Mobile**: 9999999999
- **Order ID**: AMZ99999
- **Expected**: Status not found, returns appropriate message

### Test Case 3: Missing Fields
- **Mobile**: 9876543210
- **Order ID**: (missing)
- **Expected**: Returns message that both fields are required

## Troubleshooting

### Issue: Mobile number or order ID not extracted
- **Solution**: Check the transcript text. The improved prompt should handle most cases, but ensure the audio transcription is clear.

### Issue: Excel file not found
- **Solution**: Run `python create_orders_excel.py` to create the file.

### Issue: Order not found even with correct details
- **Solution**: Verify the mobile number and order ID match exactly in the Excel file (case-insensitive for order ID).

## Sample Excel Records

The Excel file contains 15 sample records including:
- MobileNumber: 9876543210, OrderID: AMZ12345, CustomerName: Rahul Sharma
- MobileNumber: 9123456780, OrderID: AMZ98765, CustomerName: Priya Patel
- And 13 more sample records...

See `create_orders_excel.py` for the complete list.

