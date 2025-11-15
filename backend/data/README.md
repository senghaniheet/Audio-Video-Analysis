# Orders Excel File

## Location
**File Path**: `backend/data/orders.xlsx`

## File Structure

The Excel file contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| **MobileNumber** | 10-digit mobile number | 9876543210 |
| **OrderID** | Alphanumeric order ID | AMZ12345 |
| **CustomerName** | Customer's full name | Rahul Sharma |
| **OrderStatus** | Current order status | Shipped, Out for Delivery, Delivered, Processing, Cancelled |
| **DeliveryDate** | Expected delivery date (YYYY-MM-DD) | 2025-11-20 |
| **LastUpdate** | Last update timestamp | 2025-11-15 |

## How to Edit

### Option 1: Microsoft Excel
1. Open `backend/data/orders.xlsx` in Microsoft Excel
2. Add, edit, or delete rows as needed
3. Save the file

### Option 2: LibreOffice Calc
1. Open `backend/data/orders.xlsx` in LibreOffice Calc
2. Make your changes
3. Save the file

### Option 3: Google Sheets
1. Upload the file to Google Sheets
2. Make your changes
3. Download as Excel format (.xlsx)
4. Replace the file in `backend/data/orders.xlsx`

### Option 4: Python Script
You can also regenerate the file by running:
```bash
cd backend
python create_orders_excel.py
```

## Important Notes

⚠️ **Important Requirements:**
- **MobileNumber** must be exactly 10 digits (e.g., 9876543210)
- **OrderID** is case-insensitive but should be alphanumeric (e.g., AMZ12345)
- **Both MobileNumber AND OrderID** are required for order lookup
- **OrderStatus** should be one of: Processing, Shipped, Out for Delivery, Delivered, Cancelled
- **DeliveryDate** format: YYYY-MM-DD (e.g., 2025-11-20)
- **LastUpdate** format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS

## Current Records

The file currently contains **15 sample orders** including:
- Mobile: 9876543210, Order: AMZ12345, Customer: Rahul Sharma
- Mobile: 9123456780, Order: AMZ98765, Customer: Priya Patel
- And 13 more records...

## Adding New Orders

1. Open the Excel file
2. Add a new row at the bottom
3. Fill in all columns:
   - MobileNumber (10 digits)
   - OrderID (alphanumeric)
   - CustomerName
   - OrderStatus
   - DeliveryDate (YYYY-MM-DD)
   - LastUpdate
4. Save the file
5. The backend will automatically use the updated data (no restart needed if using pandas)

## Removing Orders

1. Open the Excel file
2. Select the row(s) you want to delete
3. Right-click and choose "Delete" or press Delete key
4. Save the file

## Troubleshooting

**Issue**: Order not found even after adding to Excel
- **Solution**: Make sure you saved the file. Close and reopen to verify changes were saved.

**Issue**: Invalid format error
- **Solution**: Check that MobileNumber is exactly 10 digits and dates are in YYYY-MM-DD format.

**Issue**: Backend not reading updated data
- **Solution**: Restart the backend server to reload the Excel file.

