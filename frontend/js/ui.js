// AnnaSetu UI & DOM Rendering Layer

export function renderMandiRates(data) {
    const container = document.getElementById('mandi-rates-grid');
    if (!container) return;
    container.innerHTML = '';

    data.forEach(item => {
        const isUp = item.trend === 'up';
        const card = document.createElement('div');
        card.className = 'bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between hover:border-agri-300 transition';
        card.innerHTML = `
            <div>
                <div class="flex justify-between items-start">
                    <span class="text-xs font-semibold text-slate-500">${item.district}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isUp ? 'bg-agri-100 text-agri-800' : 'bg-red-100 text-red-800'}">
                        ${isUp ? '↑ Market High' : '↓ Below MSP'}
                    </span>
                </div>
                <h4 class="font-bold text-slate-900 text-base mt-1">${item.crop}</h4>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <div>
                    <div class="text-[10px] text-slate-400 uppercase">Govt MSP Rate</div>
                    <div class="text-sm font-semibold text-slate-700">₹${item.msp} <span class="text-[10px] font-normal">/Qt</span></div>
                </div>
                <div class="text-right">
                    <div class="text-[10px] text-slate-400 uppercase">Current Market Rate</div>
                    <div class="text-base font-extrabold ${isUp ? 'text-agri-700' : 'text-red-600'}">₹${item.marketRate} <span class="text-[10px] font-normal">/Qt</span></div>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

export function renderProcurementTable(data, onPassClick) {
    const tbody = document.getElementById('procurement-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    data.forEach(row => {
        let statusBadgeClass = 'bg-amber-100 text-amber-800';
        if (row.status === 'Matched') statusBadgeClass = 'bg-agri-100 text-agri-800';
        if (row.status === 'In-Transit') statusBadgeClass = 'bg-blue-100 text-blue-800';
        if (row.status === 'Completed') statusBadgeClass = 'bg-slate-200 text-slate-800';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition';
        tr.innerHTML = `
            <td class="p-3">
                <div class="font-bold text-slate-800">${row.id}</div>
                <div class="text-slate-500 text-xs">${row.farmer}</div>
            </td>
            <td class="p-3">
                <div class="font-medium text-slate-800">${row.crop}</div>
                <div class="text-slate-500 text-xs">${row.qty}</div>
            </td>
            <td class="p-3 text-slate-600">${row.location}</td>
            <td class="p-3 font-semibold text-slate-900">${row.value}</td>
            <td class="p-3">
                <span class="px-2.5 py-1 rounded-full text-[11px] font-bold ${statusBadgeClass}">
                    ${row.status}
                </span>
            </td>
            <td class="p-3 text-right">
                <button data-order-id="${row.id}" class="btn-view-pass text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-2.5 py-1 rounded border border-slate-300 font-medium transition">
                    View Pass
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    if (onPassClick) {
        tbody.querySelectorAll('.btn-view-pass').forEach(btn => {
            btn.addEventListener('click', () => onPassClick(btn.dataset.orderId));
        });
    }
}

export function renderSurplusDirectory(items, onReserveClick) {
    const container = document.getElementById('surplus-directory-grid');
    if (!container) return;
    container.innerHTML = '';

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between space-y-3 hover:bg-white transition shadow-xs';
        card.innerHTML = `
            <div>
                <div class="flex justify-between items-start">
                    <span class="text-xs font-semibold text-amber-700 bg-amber-100 px-2 py-0.5 rounded">${item.food}</span>
                    <span class="text-[11px] text-slate-500 font-medium flex items-center gap-1"><i data-lucide="clock" class="w-3 h-3"></i> ${item.window}</span>
                </div>
                <h4 class="font-bold text-slate-900 text-sm mt-2">${item.donor}</h4>
                <p class="text-xs text-slate-500 mt-0.5">Location Zone: ${item.location}</p>
            </div>
            <div class="pt-2 border-t border-slate-200 flex items-center justify-between">
                <div>
                    <span class="text-xs text-slate-400">Available:</span>
                    <span class="text-sm font-bold text-slate-800 ml-1">${item.servings} Servings</span>
                </div>
                <button data-surplus-id="${item.id}" class="btn-reserve-surplus bg-amber-500 hover:bg-amber-600 text-slate-950 font-semibold px-3 py-1.5 rounded-lg text-xs transition">
                    Reserve Pickup
                </button>
            </div>
        `;
        container.appendChild(card);
    });

    if (window.lucide) window.lucide.createIcons();
    const badge = document.getElementById('surplus-count-badge');
    if (badge) badge.innerText = `${items.length} Batches Active`;

    if (onReserveClick) {
        container.querySelectorAll('.btn-reserve-surplus').forEach(btn => {
            btn.addEventListener('click', (e) => onReserveClick(btn.dataset.surplusId, e.target));
        });
    }
}

export function updateImpactStats(stats) {
    const statFarmers = document.getElementById('stat-farmers');
    const statProcured = document.getElementById('stat-procured');
    const statMeals = document.getElementById('stat-meals');
    if (statFarmers) statFarmers.innerText = `${stats.connectedFarmers.toLocaleString()}+`;
    if (statProcured) statProcured.innerText = `${Math.round(stats.tonsProcured).toLocaleString()}`;
    if (statMeals) statMeals.innerText = `${stats.mealsSaved.toLocaleString()}`;
}

export function populateTransitPassModal(pass) {
    const idEl = document.getElementById('transit-pass-id');
    const comEl = document.getElementById('transit-pass-commodity');
    const routeEl = document.getElementById('transit-pass-route');
    const clearEl = document.getElementById('transit-pass-clearance');
    const hashEl = document.getElementById('transit-pass-hash');
    const vehEl = document.getElementById('transit-pass-vehicle');

    if (idEl) idEl.innerText = pass.passId;
    if (comEl) comEl.innerText = pass.commodity;
    if (routeEl) routeEl.innerText = `${pass.origin} → ${pass.destination}`;
    if (clearEl) clearEl.innerText = pass.greenCorridorClearance;
    if (hashEl) hashEl.innerText = `HASH: ${pass.qrHash}`;
    if (vehEl) vehEl.innerText = `${pass.vehicleType} (-${pass.carbonReductionKg}kg CO₂)`;

    document.getElementById('modal-transit-pass')?.classList.remove('hidden');
}

export function closeTransitPassModal() {
    document.getElementById('modal-transit-pass')?.classList.add('hidden');
}

export function toggleFaq(id) {
    const ans = document.getElementById(`faq-answer-${id}`);
    const icon = document.getElementById(`faq-icon-${id}`);
    if (!ans) return;

    if (ans.classList.contains('hidden')) {
        ans.classList.remove('hidden');
        if (icon) icon.style.transform = 'rotate(180deg)';
    } else {
        ans.classList.add('hidden');
        if (icon) icon.style.transform = 'rotate(0deg)';
    }
}

export function scrollToSection(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
}
