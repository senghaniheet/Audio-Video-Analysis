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
        """Extract order ID (AMZxxxxx pattern) from text - prioritize explicit 'order ID' mentions"""
        
        # Pattern 1: "order ID is MZ12345" - Most specific, check first
        pattern1 = r'(?:order\s*(?:id|ID|number|Number)[\s:]*is[\s:]+)([A-Z]{1,4}[\s-]?\d{3,6})'
        match = re.search(pattern1, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper().replace(" ", "").replace("-", "")
            if len(order_id) >= 5:  # At least 5 chars (e.g., MZ123)
                return order_id
        
        # Pattern 2: "order ID MZ12345" or "order ID: MZ12345"
        pattern2 = r'(?:order\s*(?:id|ID|number|Number)[\s:]+)([A-Z]{1,4}[\s-]?\d{3,6})'
        match = re.search(pattern2, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper().replace(" ", "").replace("-", "")
            if len(order_id) >= 5:
                return order_id
        
        # Pattern 3: "order MZ12345" or "order AMZ12345"
        pattern3 = r'(?:order|Order)[\s:]+([A-Z]{1,4}[\s-]?\d{3,6})'
        match = re.search(pattern3, text, re.IGNORECASE)
        if match:
            order_id = match.group(1).strip().upper().replace(" ", "").replace("-", "")
            if len(order_id) >= 5:
                return order_id
        
        # Pattern 4: Standalone AMZ12345 or MZ12345 (but not part of mobile number)
        # Make sure it's not immediately after digits (to avoid matching parts of phone numbers)
        pattern4 = r'(?<!\d)([A-Z]{2,4}\d{4,6})(?!\d)'
        matches = re.finditer(pattern4, text, re.IGNORECASE)
        for match in matches:
            order_id = match.group(1).strip().upper()
            # Make sure it's not part of a longer number sequence
            start_pos = match.start()
            end_pos = match.end()
            # Check if surrounded by non-digit characters or word boundaries
            if (start_pos == 0 or not text[start_pos-1].isdigit()) and \
               (end_pos >= len(text) or not text[end_pos].isdigit()):
                if len(order_id) >= 5:
                    return order_id
        
        return None
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Process transcription text: Extract mobile number and order ID, then lookup in Excel
        
        Args:
            text: Input text (transcribed audio)
            
        Returns:
            Dictionary with extracted data and order status (backend format)
        """
        
        print(f"[INFO] Processing transcription: {text[:100]}...")
        
        # Extract mobile number and order ID
        mobile_number = self.extract_mobile_number(text)
        order_id = self.extract_order_id(text)
        
        print(f"[INFO] Extracted Mobile: {mobile_number}")
        print(f"[INFO] Extracted Order ID: {order_id}")
        
        # Lookup order in Excel
        order_data = None
        status_found = False
        
        if mobile_number and order_id:
            order_data = find_order(mobile_number, order_id)
            if order_data:
                status_found = True
                print(f"[OK] Order found: {order_data.get('order_status', 'Unknown')}")
            else:
                print(f"[WARNING] Order not found in Excel")
        
        # Generate response messages
        if not mobile_number and not order_id:
            response_text = "I could not find a mobile number or order ID in your message. Please provide both your mobile number and order ID to check the status."
        elif not mobile_number:
            response_text = f"I found order ID {order_id}, but I need your mobile number as well to check the order status. Please provide your 10-digit mobile number."
        elif not order_id:
            response_text = f"I found mobile number {mobile_number}, but I need your order ID as well to check the order status. Please provide your order ID."
        elif order_data:
            customer_name = order_data.get("customer_name", "")
            status = order_data.get("order_status", "Unknown")
            delivery_date = order_data.get("delivery_date", "")
            response_text = f"Hello {customer_name if customer_name else 'there'}, your order {order_id} is currently {status}."
            if delivery_date:
                response_text += f" Expected delivery date is {delivery_date}."
        else:
            response_text = f"I could not find order {order_id} for mobile number {mobile_number} in our records. Please verify your mobile number and order ID are correct."
        
        # Determine intent and topic
        intent = "order_status" if (mobile_number and order_id) else "general_query"
        # Topic should be set to last_update from Excel, or default if not found
        topic = str(order_data.get("last_update", "")) if order_data and order_data.get("last_update") else ("Order Status Inquiry" if intent == "order_status" else "General Query")
        
        # Build result in backend format
        result = {
            "transcript": text,
            "mobile_number": mobile_number,
            "order_id": order_id,
            "customer_name": order_data.get("customer_name") if order_data else None,
            "topic": topic,
            "intent": intent,
            "status_found": status_found,
            "order_status": {
                "status": order_data.get("order_status", "") if order_data else "",
                "delivery_date": str(order_data.get("delivery_date", "")) if order_data else "",
                "last_update": str(order_data.get("last_update", "")) if order_data else ""
            },
            "response_text": response_text,
            "response_voice_text": response_text
        }
        
        return result
    
    def orderStatusChecker(self, text: str) -> Dict[str, Any]:
        """Legacy method - calls process() for backward compatibility"""
        return self.process(text)

# MCP Server instance
mcp_server = OrderMCPServer()

def handle_mcp_request(text: str) -> Dict[str, Any]:
    """Handle MCP request - entry point for external calls"""
    return mcp_server.process(text)

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
