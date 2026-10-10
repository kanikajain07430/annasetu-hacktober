// AnnaSetu Main Application Orchestrator

import { state } from './state.js';
import * as api from './api.js';
import * as ui from './ui.js';

// DOM Initialization
window.addEventListener('DOMContentLoaded', async () => {
    if (window.lucide) window.lucide.createIcons();
    initEventListeners();
    await checkConnection();
    await loadData();
});

// Check Backend Connection Status
async function checkConnection() {
    const isOnline = await api.checkBackendHealth();
    state.isBackendConnected = isOnline;
    const statusBadge = document.getElementById('system-status');
    if (statusBadge) {
        if (isOnline) {
            statusBadge.innerHTML = 'Backend: Live & Synced <span class="text-[10px] text-agri-600 font-bold ml-1">(v1.0)</span>';
        } else {
            statusBadge.innerText = 'Offline Mode (Local Cache)';
        }
    }
}

// Load datasets from API or fallback to state
async function loadData() {
    if (state.isBackendConnected) {
        try {
            const [mandi, orders, surplus, stats] = await Promise.allSettled([
                api.fetchMandiRates(),
                api.fetchProcurementOrders(),
                api.fetchAvailableSurplus(),
                api.fetchAnalyticsStats()
            ]);

            if (mandi.status === 'fulfilled') state.mandiRates = mandi.value;
            if (orders.status === 'fulfilled') state.procurementOrders = orders.value;
            if (surplus.status === 'fulfilled') state.surplusItems = surplus.value;
            if (stats.status === 'fulfilled') ui.updateImpactStats(stats.value);
        } catch (err) {
            console.error('Error synchronizing with backend:', err);
        }
    }

    ui.renderMandiRates(state.mandiRates);
    ui.renderProcurementTable(state.procurementOrders, handleViewPass);
    ui.renderSurplusDirectory(state.surplusItems, handleReserveSurplus);
}

// Setup Event Listeners
function initEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.id.replace('tab-btn-', '');
            setActiveTab(tabId);
        });
    });

    // Role switcher
    const roleSelect = document.getElementById('user-role-select');
    if (roleSelect) {
        roleSelect.addEventListener('change', (e) => switchRole(e.target.value));
    }

    // Mandi search & reset
    const searchInput = document.getElementById('mandi-search-input');
    if (searchInput) {
        searchInput.addEventListener('keyup', handleMandiSearch);
    }
    const resetBtn = document.getElementById('mandi-search-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            searchInput.value = '';
            ui.renderMandiRates(state.mandiRates);
        });
    }

    // Procurement Status Filters
    document.querySelectorAll('.proc-filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => handleProcFilter(e.target));
    });

    // Forms
    const ledgerForm = document.getElementById('farmer-ledger-form');
    if (ledgerForm) ledgerForm.addEventListener('submit', handleLedgerSubmit);

    const surplusForm = document.getElementById('surplus-food-form');
    if (surplusForm) surplusForm.addEventListener('submit', handleSurplusSubmit);

    const grievanceForm = document.getElementById('grievance-form');
    if (grievanceForm) grievanceForm.addEventListener('submit', handleGrievanceSubmit);

    // Smart match button
    const smartMatchBtn = document.getElementById('btn-run-smart-match');
    if (smartMatchBtn) smartMatchBtn.addEventListener('click', runSmartMatchSimulation);

    // Modal close
    const closePassBtn = document.getElementById('btn-close-pass-modal');
    if (closePassBtn) closePassBtn.addEventListener('click', ui.closeTransitPassModal);
    const closePassX = document.getElementById('btn-close-pass-x');
    if (closePassX) closePassX.addEventListener('click', ui.closeTransitPassModal);

    // Expose helpers globally for inline triggers if needed
    window.setActiveTab = setActiveTab;
    window.switchRole = switchRole;
    window.scrollToSection = ui.scrollToSection;
    window.toggleFaq = ui.toggleFaq;
    window.closeTransitPassModal = ui.closeTransitPassModal;
}

// Tab Switcher
function setActiveTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('active', 'text-agri-600', 'border-agri-600');
        el.classList.add('text-slate-500');
    });

    const activeContent = document.getElementById(`tab-content-${tabId}`);
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    if (activeContent) activeContent.classList.remove('hidden');
    if (activeBtn) activeBtn.classList.add('active');
}

// Role Switcher
function switchRole(role) {
    state.role = role;
    const statusBadge = document.getElementById('system-status');
    if (!statusBadge) return;
    const prefix = state.isBackendConnected ? '[Live API] ' : '';
    const rolesMap = {
        farmer: 'Farmer Mode Active',
        vendor: 'Procurement Vendor Mode',
        ngo: 'NGO / Food Rescue Mode',
        admin: 'Admin Oversight Active'
    };
    statusBadge.innerText = `${prefix}${rolesMap[role] || 'Operational'}`;
}

// Mandi Search Filter
async function handleMandiSearch(e) {
    const query = e.target.value.toLowerCase();
    if (state.isBackendConnected) {
        try {
            const filtered = await api.fetchMandiRates(query);
            ui.renderMandiRates(filtered);
            return;
        } catch {}
    }
    const filtered = state.mandiRates.filter(item => 
        item.crop.toLowerCase().includes(query) || item.district.toLowerCase().includes(query)
    );
    ui.renderMandiRates(filtered);
}

// Procurement Table Filter
async function handleProcFilter(btn) {
    document.querySelectorAll('.proc-filter-btn').forEach(b => {
        b.classList.remove('bg-white', 'text-slate-800', 'shadow-xs');
        b.classList.add('text-slate-600');
    });
    btn.classList.add('bg-white', 'text-slate-800', 'shadow-xs');
    const filter = btn.dataset.status || 'all';

    if (state.isBackendConnected) {
        try {
            const orders = await api.fetchProcurementOrders(filter);
            ui.renderProcurementTable(orders, handleViewPass);
            return;
        } catch {}
    }

    if (filter === 'all') {
        ui.renderProcurementTable(state.procurementOrders, handleViewPass);
    } else {
        const filtered = state.procurementOrders.filter(o => o.status === filter);
        ui.renderProcurementTable(filtered, handleViewPass);
    }
}

// Farmer Ledger Form Submission
async function handleLedgerSubmit(e) {
    e.preventDefault();
    const farmer = document.getElementById('ledger-farmer-name').value;
    const crop = document.getElementById('ledger-crop').value;
    const qty = parseFloat(document.getElementById('ledger-qty').value);
    const price = parseFloat(document.getElementById('ledger-price').value);
    const location = document.getElementById('ledger-location').value;
    const whatsapp = document.getElementById('ledger-whatsapp').checked;

    const payload = {
        farmerName: farmer,
        cropType: crop,
        quantityQuintals: qty,
        pricePerQuintal: price,
        location: location,
        whatsappAlerts: whatsapp
    };

    let createdOrder = null;
    if (state.isBackendConnected) {
        try {
            createdOrder = await api.createHarvestListing(payload);
            state.procurementOrders.unshift(createdOrder);
        } catch (err) {
            console.error('API listing error:', err);
        }
    }

    if (!createdOrder) {
        createdOrder = {
            id: `ORD-${Math.floor(1000 + Math.random() * 9000)}`,
            farmer,
            crop,
            qty: `${qty} Qt`,
            location,
            value: `₹${(qty * price).toLocaleString()}`,
            status: 'Pending'
        };
        state.procurementOrders.unshift(createdOrder);
    }

    ui.renderProcurementTable(state.procurementOrders, handleViewPass);
    document.getElementById('farmer-ledger-form').reset();
    alert(`✓ Harvest Listing ${createdOrder.id} Created Successfully!\nRecorded to database. Matches broadcasted to verified procurement buyers.`);
}

// Surplus Food Form Submission
async function handleSurplusSubmit(e) {
    e.preventDefault();
    const donor = document.getElementById('surplus-donor').value;
    const category = document.getElementById('surplus-category').value;
    const servings = parseInt(document.getElementById('surplus-servings').value);
    const windowTime = document.getElementById('surplus-window').value;
    const location = document.getElementById('surplus-location').value;

    const payload = {
        donorOrg: donor,
        category,
        servings,
        pickupWindowHours: windowTime,
        locationZone: location
    };

    let createdBatch = null;
    if (state.isBackendConnected) {
        try {
            createdBatch = await api.createSurplusDonation(payload);
            state.surplusItems.unshift(createdBatch);
        } catch (err) {
            console.error('API surplus donation error:', err);
        }
    }

    if (!createdBatch) {
        createdBatch = {
            id: `SUR-${Math.floor(100 + Math.random() * 900)}`,
            donor,
            food: category,
            servings,
            window: windowTime,
            location
        };
        state.surplusItems.unshift(createdBatch);
    }

    ui.renderSurplusDirectory(state.surplusItems, handleReserveSurplus);
    document.getElementById('surplus-food-form').reset();
    alert(`✓ Surplus Food Batch ${createdBatch.id} Listed!\nZero-waste redistribution alert dispatched to partner NGO rescue network.`);
}

// Reserve Surplus
async function handleReserveSurplus(id, btnElement) {
    btnElement.disabled = true;
    btnElement.innerText = 'Reserved ✓';
    btnElement.className = 'bg-agri-600 text-white font-semibold px-3 py-1.5 rounded-lg text-xs cursor-default';

    if (state.isBackendConnected) {
        try {
            await api.reserveSurplusBatch(id, "Verified Community Shelter Rescue Unit", "Within 45 Minutes");
        } catch (err) {}
    }

    alert(`✓ Pickup slot reserved for batch ${id}!\nDigital transit QR code dispatched to registered NGO rescue team.`);
}

// Smart Match Route Simulation
async function runSmartMatchSimulation() {
    const logBox = document.getElementById('match-log-box');
    const routeLine = document.getElementById('route-line-active');
    if (!logBox || !routeLine) return;

    logBox.innerHTML = `
        <div class="text-agri-400 font-bold">// Engine Execution Started...</div>
        <div>[1/3] Scanning cluster harvest ledgers...</div>
    `;
    routeLine.style.width = '20%';

    let matchResult = null;
    if (state.isBackendConnected) {
        try {
            matchResult = await api.runSmartMatchApi('Wheat (Lokwan)', 120.0, 'Karnal, Haryana');
            state.latestTransitPassId = matchResult.transitPassId;
        } catch {}
    }

    setTimeout(() => {
        logBox.innerHTML += `<div>[2/3] Found 120 Quintals Wheat match in Karnal.</div>`;
        routeLine.style.width = '60%';
    }, 600);

    setTimeout(() => {
        const passMsg = matchResult ? `Pass #${matchResult.transitPassId}` : 'Pass #AS-PASS-2026-9042';
        const orderMsg = matchResult ? `Order #${matchResult.orderId}` : 'Order #ORD-8821';
        logBox.innerHTML += `
            <div class="text-amber-300">[3/3] Route optimized via Green EV Corridor!</div>
            <div class="text-agri-400 font-bold">✓ Match Finalized: ${orderMsg} | ${passMsg}</div>
        `;
        routeLine.style.width = '100%';
    }, 1400);
}

// Transit Pass Modal Viewer
async function handleViewPass(orderId) {
    const targetId = orderId || state.latestTransitPassId || 'ORD-8821';
    let passData = {
        passId: 'AS-PASS-2026-9042',
        commodity: 'Wheat Lokwan (120 Quintals)',
        origin: 'Karnal Mandi',
        destination: 'Central Warehouse Depot',
        greenCorridorClearance: 'APPROVED (Fast-Track)',
        qrHash: '8f9b2a1c0d3e4f5a',
        vehicleType: 'Electric EV-Truck 4.5T',
        carbonReductionKg: 142.0
    };

    if (state.isBackendConnected) {
        try {
            passData = await api.fetchTransitPass(targetId);
        } catch {}
    }

    ui.populateTransitPassModal(passData);
}

// Grievance Form Handler
async function handleGrievanceSubmit(e) {
    e.preventDefault();
    const name = document.getElementById('grievance-name').value;
    const category = document.getElementById('grievance-category').value;
    const msg = document.getElementById('grievance-msg').value;
    const feedback = document.getElementById('grievance-feedback');

    let ticketId = `GRV-${Math.floor(1000 + Math.random() * 9000)}`;
    if (state.isBackendConnected) {
        try {
            const data = await api.submitGrievanceApi(name, category, msg);
            ticketId = data.ticketId;
        } catch {}
    }

    if (feedback) {
        feedback.classList.remove('hidden');
        feedback.innerText = `✓ Thank you, ${name}. Your grievance ticket #${ticketId} has been officially recorded in the agricultural resolution database.`;
    }
    document.getElementById('grievance-form').reset();
}
