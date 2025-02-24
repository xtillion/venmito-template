import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, Sector, ResponsiveContainer } from 'recharts';
import { fetchPromotedPeople } from '../services/api';
import { useNavigate } from 'react-router-dom';

// Custom active shape: note that the text label has been removed.
const renderActiveShape = (props) => {
    const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill } = props;
    return (
        <g style={{ cursor: 'pointer' }}>
            <Sector
                cx={cx}
                cy={cy}
                innerRadius={innerRadius}
                outerRadius={outerRadius + 10}
                startAngle={startAngle}
                endAngle={endAngle}
                fill={fill}
            />
        </g>
    );
};

const PromotionsPieChart = () => {
    const [chartData, setChartData] = useState([]);
    const [rawData, setRawData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedPromotion, setSelectedPromotion] = useState(null);
    const [activeIndex, setActiveIndex] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const getData = async () => {
            try {
                const promotedData = await fetchPromotedPeople();
                setRawData(promotedData);
                // Group by promotion and count occurrences
                const counts = promotedData.reduce((acc, curr) => {
                    const promo = curr.promotion;
                    acc[promo] = (acc[promo] || 0) + 1;
                    return acc;
                }, {});
                const data = Object.keys(counts).map(key => ({
                    name: key,
                    value: counts[key]
                }));
                setChartData(data);
            } catch (error) {
                console.error('Error fetching promotions:', error);
            } finally {
                setLoading(false);
            }
        };

        getData();
    }, []);

    // Define colors for the slices
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560'];

    const handleSliceClick = (data) => {
        if (data && data.payload) {
            const promotionName = data.payload.name;
            const promotionResponses = rawData.filter(r => r.promotion === promotionName);

            setSelectedPromotion(promotionName);

            // Navigate to the new page and pass promotion data via `state`
            navigate(`/promotion-chart/${promotionName}`, {
                state: { promotion: promotionName, responses: promotionResponses },
            });
        }
    };

    if (loading) {
        return <p>Loading promotions data...</p>;
    }

    return (
        <div className="my-6">
            <h2 className="text-xl font-semibold mb-4 text-center">Promotions Distribution</h2>
            <div style={{ width: 400, height: 400 }}>
                <ResponsiveContainer>
                    <PieChart>
                        <Pie
                            data={chartData}
                            outerRadius={120}
                            dataKey="value"
                            fill="#8884d8"
                            labelLine={false}
                            activeIndex={activeIndex}
                            activeShape={renderActiveShape}
                            onMouseEnter={(_, index) => setActiveIndex(index)}
                            onMouseLeave={() => setActiveIndex(null)}
                            onClick={(data) => handleSliceClick(data)}
                        >
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>

        </div>
    );
};

export default PromotionsPieChart;
