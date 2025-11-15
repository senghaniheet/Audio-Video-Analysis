/**
 * Node.js Backend Server with SSE endpoint
 * Connects to MCP Server and streams results via SSE
 */
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

/**
 * Call Python MCP Server
 */
function callMCPServer(text) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, '../server/order_mcp_server.py');
        const pythonProcess = spawn('python', [pythonScript, text]);
        
        let output = '';
        let errorOutput = '';
        
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });
        
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python process exited with code ${code}: ${errorOutput}`));
                return;
            }
            
            try {
                // Try to parse JSON output
                const result = JSON.parse(output.trim());
                resolve(result);
            } catch (e) {
                // If not JSON, create a result object
                resolve({
                    match: false,
                    message: output.trim() || "Error processing request"
                });
            }
        });
        
        pythonProcess.on('error', (error) => {
            reject(error);
        });
    });
}

/**
 * SSE Endpoint: GET /api/order-status-stream
 */
app.get('/api/order-status-stream', (req, res) => {
    const text = req.query.text || req.query.input || '';
    
    if (!text) {
        res.status(400).json({ error: 'Text parameter is required' });
        return;
    }
    
    // Set SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    
    // Send processing event
    res.write(`event: processing\n`);
    res.write(`data: ${JSON.stringify({ stage: 'processing', message: 'Starting order status check...' })}\n\n`);
    
    // Send extracting event
    setTimeout(() => {
        res.write(`event: extracting_keywords\n`);
        res.write(`data: ${JSON.stringify({ stage: 'extracting_keywords', message: 'Extracting mobile number and order ID...' })}\n\n`);
    }, 500);
    
    // Send excel lookup event
    setTimeout(() => {
        res.write(`event: excel_lookup\n`);
        res.write(`data: ${JSON.stringify({ stage: 'excel_lookup', message: 'Searching in order database...' })}\n\n`);
    }, 1000);
    
    // Call MCP Server
    callMCPServer(text)
        .then((result) => {
            // Send final result
            setTimeout(() => {
                res.write(`event: final_result\n`);
                res.write(`data: ${JSON.stringify({
                    mobile: result.mobile || '',
                    order_id: result.order_id || '',
                    status: result.status || '',
                    message: result.message || ''
                })}\n\n`);
                
                res.end();
            }, 500);
        })
        .catch((error) => {
            res.write(`event: error\n`);
            res.write(`data: ${JSON.stringify({
                error: error.message,
                message: 'Error processing order status request'
            })}\n\n`);
            res.end();
        });
});

/**
 * Alternative REST endpoint (non-SSE)
 */
app.post('/api/order-status', async (req, res) => {
    const { text } = req.body;
    
    if (!text) {
        return res.status(400).json({ error: 'Text parameter is required' });
    }
    
    try {
        const result = await callMCPServer(text);
        res.json({
            mobile: result.mobile || '',
            order_id: result.order_id || '',
            status: result.status || '',
            message: result.message || ''
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'MCP Order Status Backend' });
});

// Start server
app.listen(PORT, () => {
    console.log(`MCP Order Status Backend running on http://localhost:${PORT}`);
    console.log(`SSE Endpoint: http://localhost:${PORT}/api/order-status-stream?text=YOUR_TEXT`);
});

