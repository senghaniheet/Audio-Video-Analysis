"""
MCP Server for Order Status Processing
Handles text analysis, Excel lookup, and response generation
"""
import pandas as pd
import os
import json
import re
from openai import OpenAI
from typing import Dict, Optional, Any

class MCPServer:
    """MCP Server for order status extraction and lookup"""
    
    def __init__(self, excel_path: str = "data/orders.xlsx", openai_api_key: str = None):
        """
        Initialize MCP Server
        
        Args:
            excel_path: Path to Excel file with orders
            openai_api_key: OpenAI API key (or uses environment variable)
        """
        self.excel_path = excel_path
        self.client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))
        self.orders_df = None
        self._load_excel()
    
    def _load_excel(self):
        """Load Excel file with orders"""
        try:
            if os.path.exists(self.excel_path):
                self.orders_df = pd.read_excel(self.excel_path)
                print(f"Loaded {len(self.orders_df)} orders from Excel")
            else:
                print(f"Excel file not found at {self.excel_path}, using empty dataframe")
                self.orders_df = pd.DataFrame(columns=[
                    'MobileNumber', 'OrderID', 'CustomerName', 
                    'OrderStatus', 'DeliveryDate', 'LastUpdate'
                ])
        except Exception as e:
            print(f"Error loading Excel: {str(e)}")
            self.orders_df = pd.DataFrame(columns=[
                'MobileNumber', 'OrderID', 'CustomerName', 
                'OrderStatus', 'DeliveryDate', 'LastUpdate'
            ])
    
    def extract_from_text(self, transcript: str) -> Dict[str, Any]:
        """
        Extract information from transcript using AI
        
        Args:
            transcript: Text transcript from audio
            
        Returns:
            dict with mobile_number, order_id, customer_name, topic, intent
        """
        prompt = f"""You are an MCP server specializing in order status extraction and lookup.

TASK:
1. Read the transcript text below.
2. Extract:
   - mobile_number (10 digits, Indian format like 9876543210)
   - order_id (alphanumeric, could be AMZ12345, ORD123, etc.)
   - customer_name
   - topic (what the conversation is about)
   - intent (user's intention: "check_status", "delivery_inquiry", "complaint", etc.)
3. If mobile number or order ID is not found, return them as null.
4. Return only valid JSON, no markdown, no code blocks.

Transcript:
{transcript}

Return only JSON:
{{
  "mobile_number": "",
  "order_id": "",
  "customer_name": "",
  "topic": "",
  "intent": ""
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            text = response.choices[0].message.content or "{}"
            text = text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```"):
                text = re.sub(r'^```json\s*', '', text)
                text = re.sub(r'^```\s*', '', text)
                text = re.sub(r'```\s*$', '', text)
            
            extracted = json.loads(text)
            return extracted
        except Exception as e:
            print(f"Error in extraction: {str(e)}")
            return {
                "mobile_number": None,
                "order_id": None,
                "customer_name": None,
                "topic": "Order Inquiry",
                "intent": "check_status"
            }
    
    def lookup_order(self, mobile_number: str = None, order_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Lookup order in Excel file by mobile number or order ID
        
        Args:
            mobile_number: Customer mobile number
            order_id: Order ID
            
        Returns:
            dict with order details or None if not found
        """
        if self.orders_df is None or len(self.orders_df) == 0:
            return None
        
        try:
            # Search by mobile number
            if mobile_number:
                # Clean mobile number (remove spaces, dashes, etc.)
                mobile_clean = re.sub(r'[^\d]', '', str(mobile_number))
                match = self.orders_df[
                    self.orders_df['MobileNumber'].astype(str).str.replace(r'[^\d]', '', regex=True) == mobile_clean
                ]
                if len(match) > 0:
                    row = match.iloc[0]
                    return {
                        "status": str(row.get('OrderStatus', 'Unknown')),
                        "delivery_date": str(row.get('DeliveryDate', '')),
                        "last_update": str(row.get('LastUpdate', '')),
                        "customer_name": str(row.get('CustomerName', ''))
                    }
            
            # Search by order ID
            if order_id:
                match = self.orders_df[
                    self.orders_df['OrderID'].astype(str).str.upper() == str(order_id).upper()
                ]
                if len(match) > 0:
                    row = match.iloc[0]
                    return {
                        "status": str(row.get('OrderStatus', 'Unknown')),
                        "delivery_date": str(row.get('DeliveryDate', '')),
                        "last_update": str(row.get('LastUpdate', '')),
                        "customer_name": str(row.get('CustomerName', ''))
                    }
        except Exception as e:
            print(f"Error in Excel lookup: {str(e)}")
        
        return None
    
    def generate_response(self, extracted: Dict, order_status: Optional[Dict], status_found: bool) -> Dict[str, str]:
        """
        Generate response text based on extracted data and order status
        
        Args:
            extracted: Extracted data from transcript
            order_status: Order status from Excel lookup
            status_found: Whether order was found in Excel
            
        Returns:
            dict with response_text and response_voice_text
        """
        mobile = extracted.get("mobile_number") or "Not provided"
        order_id = extracted.get("order_id") or "Not provided"
        customer_name = extracted.get("customer_name") or "Customer"
        intent = extracted.get("intent", "check_status")
        
        if status_found and order_status:
            status = order_status.get("status", "Unknown")
            delivery_date = order_status.get("delivery_date", "")
            last_update = order_status.get("last_update", "")
            
            response_text = f"Hello {customer_name}, your order {order_id} is currently {status}."
            if delivery_date:
                response_text += f" Expected delivery date: {delivery_date}."
            if last_update:
                response_text += f" Last updated: {last_update}."
            
            response_voice_text = f"Hello {customer_name}, your order ending with {order_id[-3:] if len(order_id) > 3 else order_id} is {status.lower()}."
            if delivery_date:
                response_voice_text += f" It will be delivered on {delivery_date}."
        else:
            response_text = "Sorry, we couldn't find any order for this mobile number or order ID. Please verify your details and try again."
            response_voice_text = "I'm sorry, but I couldn't find any order linked with this mobile number or order ID. Please check your details and contact support if needed."
        
        return {
            "response_text": response_text,
            "response_voice_text": response_voice_text
        }
    
    def process(self, transcript: str) -> Dict[str, Any]:
        """
        Main processing function: Extract -> Lookup -> Generate Response
        
        Args:
            transcript: Text transcript from audio
            
        Returns:
            Complete JSON response with all extracted data and order status
        """
        # Step 1: Extract information
        extracted = self.extract_from_text(transcript)
        
        mobile_number = extracted.get("mobile_number")
        order_id = extracted.get("order_id")
        customer_name = extracted.get("customer_name")
        topic = extracted.get("topic", "Order Inquiry")
        intent = extracted.get("intent", "check_status")
        
        # Step 2: Lookup in Excel
        order_status = None
        status_found = False
        
        if mobile_number or order_id:
            order_status = self.lookup_order(
                mobile_number=mobile_number,
                order_id=order_id
            )
            status_found = order_status is not None
        
        # Step 3: Generate response
        response = self.generate_response(extracted, order_status, status_found)
        
        # Step 4: Build final response
        result = {
            "transcript": transcript,
            "mobile_number": mobile_number,
            "order_id": order_id,
            "customer_name": customer_name,
            "topic": topic,
            "intent": intent,
            "status_found": status_found,
            "order_status": order_status if status_found else {
                "status": "Not Found",
                "delivery_date": None,
                "last_update": None
            },
            "response_text": response["response_text"],
            "response_voice_text": response["response_voice_text"]
        }
        
        return result

