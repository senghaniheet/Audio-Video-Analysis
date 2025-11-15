"""
MCP Server for Order Status Checking
Extracts mobile number and order ID from text and looks up in Excel
"""
import re
import json
import sys
from typing import Dict, Any, Optional
from excel_loader import find_order, create_sample_excel
import os

class OrderMCPServer:
    """MCP Server for order status checking"""
    
    def __init__(self):
        """Initialize MCP Server"""
        # Ensure Excel file exists
        if not os.path.exists("order_data.xlsx"):
            create_sample_excel()
    
    def extract_mobile_number(self, text: str) -> Optional[str]:
        """Extract 10-digit mobile number from text"""
        
        # Pattern 1: "mobile number is 9876543210"
        pattern1 = r'(?:mobile|number|phone|contact)[\s:]*(\d{10})'
        match = re.search(pattern1, text, re.IGNORECASE)
        if match:
            mobile = re.sub(r'[^\d]', '', match.group(1))
            if len(mobile) == 10:
                return mobile
        
        # Pattern 2: Any 10 consecutive digits
        pattern2 = r'\b(\d{10})\b'
        match = re.search(pattern2, text)
        if match:
            mobile = match.group(1)
            if len(mobile) == 10:
                return mobile
        
        # Pattern 3: Formatted number (987-654-3210 or 987 654 3210)
        pattern3 = r'(\d{3}[\s-]?\d{3}[\s-]?\d{4})'
        match = re.search(pattern3, text)
        if match:
            mobile = re.sub(r'[^\d]', '', match.group(1))
            if len(mobile) == 10:
                return mobile
        
        return None
    
    def extract_order_id(self, text: str) -> Optional[str]:
        """Extract order ID (AMZxxxxx pattern) from text"""
        
        # Pattern 1: "order ID is AMZ12345" or "order AMZ12345"
        pattern1 = r'(?:order\s*(?:id|number|ID|Number)[\s:]*)?([A-Z]{2,4}[\s-]?\d{4,6})'
        match = re.search(pattern1, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper().replace(" ", "").replace("-", "")
            if len(order_id) >= 5:  # At least 5 chars (e.g., AMZ12)
                return order_id
        
        # Pattern 2: Standalone AMZ12345 or MZ12345
        pattern2 = r'\b([A-Z]{2,4}\d{4,6})\b'
        match = re.search(pattern2, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper()
            if len(order_id) >= 5:
                return order_id
        
        # Pattern 3: "order MZ12345" or "order AMZ12345"
        pattern3 = r'(?:order|Order)[\s:]+([A-Z]{1,4}[\s-]?\d{3,6})'
        match = re.search(pattern3, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper().replace(" ", "").replace("-", "")
            if len(order_id) >= 5:
                return order_id
        
        return None
    
    def orderStatusChecker(self, text: str) -> Dict[str, Any]:
        """
        MCP Tool: Check order status from text
        
        Args:
            text: Input text (transcribed audio)
            
        Returns:
            JSON response with match status and order details
        """
        
        # Extract mobile number and order ID
        mobile_number = self.extract_mobile_number(text)
        order_id = self.extract_order_id(text)
        
        # If both not found, return natural AI response
        if not mobile_number and not order_id:
            return {
                "match": False,
                "mobile": None,
                "order_id": None,
                "status": None,
                "message": "I could not find a mobile number or order ID in your message."
            }
        
        # If only one found, return helpful message
        if not mobile_number:
            return {
                "match": False,
                "mobile": None,
                "order_id": order_id,
                "status": None,
                "message": "I found an order ID but could not find a mobile number. Please provide both mobile number and order ID."
            }
        
        if not order_id:
            return {
                "match": False,
                "mobile": mobile_number,
                "order_id": None,
                "status": None,
                "message": "I found a mobile number but could not find an order ID. Please provide both mobile number and order ID."
            }
        
        # Both found - search in Excel
        order = find_order(mobile_number, order_id)
        
        if order:
            return {
                "match": True,
                "mobile": mobile_number,
                "order_id": order_id,
                "status": order["order_status"],
                "message": f"Order found. Status is {order['order_status']}."
            }
        else:
            return {
                "match": False,
                "mobile": mobile_number,
                "order_id": order_id,
                "status": None,
                "message": "Mobile or Order ID not found in records."
            }

# MCP Server instance
mcp_server = OrderMCPServer()

def handle_mcp_request(text: str) -> Dict[str, Any]:
    """Handle MCP request - entry point for external calls"""
    return mcp_server.orderStatusChecker(text)

if __name__ == "__main__":
    # Handle command line input
    if len(sys.argv) > 1:
        # Text passed as command line argument
        text = ' '.join(sys.argv[1:])
        result = mcp_server.orderStatusChecker(text)
        print(json.dumps(result, indent=2))
    else:
        # Test the MCP server
        test_text = "My mobile number is 9876543210 and order ID AMZ12345"
        result = mcp_server.orderStatusChecker(test_text)
        print(json.dumps(result, indent=2))
