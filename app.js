import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { createClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();

// Initialize Supabase client
const supabaseUrl = 'https://lmxthwkopahhqzxlhncg.supabase.co';
const supabaseKey = process.env.SUPABASE_KEY; // Ensure you have your Supabase key in your environment variables
const supabase = createClient(supabaseUrl, supabaseKey);

// Define a route to serve the index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API route to fetch data from Supabase
app.get('/citycount', async (req, res) => {
    let { data: people, error } = await supabase
        .from('people')
        .select('id, city');

    if (error) {
        return res.status(500).json({ error: error.message });
    }

    const cityCounts = people.reduce((acc, { city }) => {
        acc[String(city)] = (acc[String(city)] || 0) + 1;
        return acc;
    }, {});

    const x = Object.keys(cityCounts);  // City names
    const y = Object.values(cityCounts);  // City counts

    // Send the data as JSON response
    res.json({ x, y });
});

app.get('/countrycount', async (req, res) => {
    let { data: people, error } = await supabase
        .from('people')
        .select('id, country');

    if (error) {
        return res.status(500).json({ error: error.message });
    }

    const countryCount = people.reduce((acc, { country }) => {
        acc[String(country)] = (acc[String(country)] || 0) + 1;
        return acc;
    }, {});

    const x = Object.keys(countryCount);  // City names
    const y = Object.values(countryCount);  // City counts

    // Send the data as JSON response
    res.json({ x, y });
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
