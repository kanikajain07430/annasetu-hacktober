// AnnaSetu Network & REST API Client

export const API_BASE = (window.location.protocol.startsWith('http') && window.location.port === '8000') 
    ? '' 
    : 'http://127.0.0.1:8000';

export async function checkBackendHealth() {
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        return res.ok;
    } catch {
        return false;
    }
}

export async function fetchMandiRates(cropQuery = '') {
    const url = cropQuery 
        ? `${API_BASE}/api/v1/mandi/rates?crop=${encodeURIComponent(cropQuery)}`
        : `${API_BASE}/api/v1/mandi/rates`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch mandi rates');
    return await res.json();
}

export async function fetchProcurementOrders(statusFilter = '') {
    const url = (statusFilter && statusFilter !== 'all')
        ? `${API_BASE}/api/v1/procurement/orders?status=${encodeURIComponent(statusFilter)}`
        : `${API_BASE}/api/v1/procurement/orders`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch procurement orders');
    return await res.json();
}

export async function createHarvestListing(payload) {
    const res = await fetch(`${API_BASE}/api/v1/procurement/listings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to create harvest listing');
    return await res.json();
}

export async function fetchAvailableSurplus() {
    const res = await fetch(`${API_BASE}/api/v1/surplus/available`);
    if (!res.ok) throw new Error('Failed to fetch surplus items');
    return await res.json();
}

export async function createSurplusDonation(payload) {
    const res = await fetch(`${API_BASE}/api/v1/surplus/donations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to broadcast surplus donation');
    return await res.json();
}

export async function reserveSurplusBatch(surplusId, ngoId, pickupTime) {
    const res = await fetch(`${API_BASE}/api/v1/surplus/reserve/${surplusId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ngoId, estimatedPickupTime: pickupTime })
    });
    if (!res.ok) throw new Error('Failed to reserve surplus');
    return await res.json();
}

export async function runSmartMatchApi(cropType, quantity, originDistrict) {
    const res = await fetch(`${API_BASE}/api/v1/logistics/smart-match`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cropType, quantity, originDistrict })
    });
    if (!res.ok) throw new Error('Smart match algorithm failed');
    return await res.json();
}

export async function fetchTransitPass(passOrOrderId) {
    const res = await fetch(`${API_BASE}/api/v1/logistics/pass/${passOrOrderId}`);
    if (!res.ok) throw new Error('Failed to retrieve transit pass');
    return await res.json();
}

export async function submitGrievanceApi(name, category, issueDetails) {
    const res = await fetch(`${API_BASE}/api/v1/support/grievance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, issueDetails })
    });
    if (!res.ok) throw new Error('Failed to log grievance');
    return await res.json();
}

export async function fetchAnalyticsStats() {
    const res = await fetch(`${API_BASE}/api/v1/analytics/stats`);
    if (!res.ok) throw new Error('Failed to fetch analytics statistics');
    return await res.json();
}
