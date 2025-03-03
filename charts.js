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

    app.get('/api/devicedistrib', async (req, res) => {
        try {
            let { data: people, error } = await supabase
            .from('people')
            .select('Android,Iphone,Desktop')
              
            if (error) {
                return res.status(500).json({ error: error.message });
            }
        
        let sums = { Android: 0, iPhone: 0, Desktop: 0 };
        // Loop through each row and sum up the values
        
        people.forEach(person => {
            if (person['Android'] === 1) sums.Android += 1;
            if (person['Iphone'] === '1') sums.iPhone += 1;
            if (person['Desktop'] === '1') sums.Desktop += 1;
        });

        console.log(sums)
        // Return the result in the desired format
        return res.status(200).json(sums);
        } catch (error) {
            return res.status(500).json({ error: error.message });
        }    
    });

    // ran this in the supabase postgres
    // ALTER TABLE transfers
    // ADD COLUMN sender_loc VARCHAR(255),
    // ADD COLUMN recipient_loc VARCHAR(255);

    // UPDATE transfers t
    // SET 
    //     sender_loc = u_sender.country,
    //     recipient_loc = u_recipient.country
    // FROM 
    //     people u_sender
    // JOIN 
    //     people u_recipient ON t.recipient_id = u_recipient.id
    // WHERE 
    //     t.sender_id = u_sender.id;
    
    app.get('/api/internationTransfer', async (req, res) => {
        try {
            let { data: transfers, error } = await supabase
            .from('transfers')
            .select('sender_loc, recipient_loc')
              
            if (error) {
                return res.status(500).json({ error: error.message });
            }
        
        let totals = { Domestic: 0, International: 0 };
        // Loop through each row and sum up the values
        
        transfers.forEach(transfer => {
            if (transfer['sender_loc'] !== transfer['recipient_loc']) totals.International += 1;
            else totals.Domestic += 1
        });
        // Return the result in the desired format
        return res.status(200).json(totals);
        } catch (error) {
            return res.status(500).json({ error: error.message });
        }    
    });

    app.get('/api/promoResponse', async (req, res) => {
        try {
            let { data: promotions, error } = await supabase
            .from('promotions')
            .select('responded')
              
            if (error) {
                return res.status(500).json({ error: error.message });
            }
        
        let totals = { Yes: 0, No: 0 };
        // Loop through each row and sum up the values
        
        promotions.forEach(promotion => {
            if (promotion['responded'] === 'Yes') totals.Yes += 1;
            else totals.No += 1
        });
        return res.status(200).json(totals);
        } catch (error) {
            return res.status(500).json({ error: error.message });
        }    
    });

};

export default chartRoutes;
