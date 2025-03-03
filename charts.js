import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client
const supabaseUrl = 'https://lmxthwkopahhqzxlhncg.supabase.co';
const supabaseKey = process.env.SUPABASE_KEY; // Ensure you have your Supabase key in your environment variables
const supabase = createClient(supabaseUrl, supabaseKey);

const chartRoutes = (app) => {
    // API route to get city count data
    app.get('/api/citycount', async (req, res) => {
        try {
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
        } catch (err) {
            return res.status(500).json({ error: 'Internal Server Error' });
        }
    });

    app.get('/api/countrycount', async (req, res) => {
        try {
            let { data: people, error } = await supabase
                .from('people')
                .select('id, country');
    
            if (error) {
                return res.status(500).json({ error: error.message });
            }
    
            const countryCounts = people.reduce((acc, { country }) => {
                acc[String(country)] = (acc[String(country)] || 0) + 1;
                return acc;
            }, {});
    
            const x = Object.keys(countryCounts);  // Country names
            const y = Object.values(countryCounts);  // Country counts
    
            // Send the data as JSON response
            res.json({ x, y });
        } catch (err) {
            return res.status(500).json({ error: 'Internal Server Error' });
        }
    });
    
};



export default chartRoutes;
