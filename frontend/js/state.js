// AnnaSetu Central State Store

export const state = {
    role: 'farmer',
    isBackendConnected: false,
    latestTransitPassId: 'AS-PASS-2026-9042',
    mandiRates: [
        { crop: 'Wheat (Lokwan)', district: 'Karnal, Haryana', msp: 2275, marketRate: 2380, trend: 'up' },
        { crop: 'Paddy Rice (Basmati)', district: 'Amritsar, Punjab', msp: 2183, marketRate: 3450, trend: 'up' },
        { crop: 'Red Onion', district: 'Nashik, Maharashtra', msp: 1800, marketRate: 2100, trend: 'up' },
        { crop: 'Yellow Soybean', district: 'Indore, Madhya Pradesh', msp: 4600, marketRate: 4450, trend: 'down' }
    ],
    procurementOrders: [
        { id: 'ORD-8821', farmer: 'Ramesh Kumar', crop: 'Wheat (Lokwan)', qty: '120 Qt', location: 'Karnal, Haryana', value: '₹2,85,600', status: 'Matched' },
        { id: 'ORD-8822', farmer: 'Sukhwinder Singh', crop: 'Paddy Rice (Basmati)', qty: '85 Qt', location: 'Amritsar, Punjab', value: '₹2,93,250', status: 'Pending' },
        { id: 'ORD-8823', farmer: 'Anil Deshmukh', crop: 'Soybean (Yellow)', qty: '50 Qt', location: 'Indore, Madhya Pradesh', value: '₹2,22,500', status: 'In-Transit' }
    ],
    surplusItems: [
        { id: 'SUR-101', donor: 'Royal Palace Banquet', food: 'Cooked Meals (Veg)', servings: 180, window: '2 Hours Left', location: 'North Sector 4' },
        { id: 'SUR-102', donor: 'Apex Corporate Canteen', food: 'Packaged / Dry Rations', servings: 75, window: '4 Hours Left', location: 'Tech Park Hub' },
        { id: 'SUR-103', donor: 'Metro Fresh Supermarket', food: 'Fresh Produce / Fruits', servings: 200, window: '5 Hours Left', location: 'Central District' }
    ]
};
