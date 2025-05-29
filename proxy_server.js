const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const upload = multer();

// Enable CORS for all routes
app.use(cors());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
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

        res.json(response.data);
    } catch (error) {
        console.error('Error:', error.message);
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Proxy server running on port ${PORT}`);
}); 