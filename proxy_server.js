const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const upload = multer();

// Enable CORS for all routes with specific configuration
app.use(cors({
  origin: [
    'https://frontend-two-mu-37.vercel.app',
    'https://ai-skin-analyzer.vercel.app',
    'http://localhost:3000',
    'http://localhost:5173'
  ],
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Accept', 'Authorization'],
  credentials: true
}));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ 
    error: 'Internal server error',
    message: err.message 
  });
});

app.post('/predict', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        // Create form data
        const formData = new FormData();
        formData.append('file', req.file.buffer, {
            filename: 'image.jpg',
            contentType: 'image/jpeg'
        });

        // Forward to cloud function
        const response = await axios.post(
            'https://us-central1-aurora-457407.cloudfunctions.net/predict',
            formData,
            {
                headers: {
                    ...formData.getHeaders(),
                    'Accept': 'application/json'
                },
                timeout: 120000 // 120 seconds timeout
            }
        );

        // Set CORS headers explicitly for this response
        res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
        res.header('Access-Control-Allow-Credentials', 'true');
        res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.header('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization');

        res.json(response.data);
    } catch (error) {
        console.error('Error:', error.message);
        
        // Set CORS headers even for error responses
        res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
        res.header('Access-Control-Allow-Credentials', 'true');
        res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.header('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization');

        if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            res.status(error.response.status).json({
                error: 'AI model error',
                message: error.response.data?.message || error.message
            });
        } else if (error.request) {
            // The request was made but no response was received
            res.status(504).json({
                error: 'Gateway timeout',
                message: 'No response received from AI model'
            });
        } else {
            // Something happened in setting up the request that triggered an Error
            res.status(500).json({
                error: 'Internal server error',
                message: error.message
            });
        }
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Proxy server running on port ${PORT}`);
}); 