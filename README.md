🌾 AnnaSetu - Smart Agricultural Procurement & Surplus Redistribution PlatformBackend Developer Specification & Technical Integration Guide📌 Project OverviewAnnaSetu is a dual-impact AgTech and social welfare web application designed to:Connect Smallholder Farmers to Procurement Buyers: Facilitate direct sales at transparent Government Minimum Support Prices (MSP) and Mandi rates, eliminating exploitative intermediaries.Bridge Commercial Food Surplus to Redistribution Networks: Provide commercial kitchens, event halls, and supermarkets a zero-waste portal to donate safe, edible surplus food to verified NGOs and community shelters in real-time.Smart Logistics Engine: Match harvest yields with transit corridors and generate digital transit passes (e-Way bills) for fast-track green corridor movement.🏗️ System Architecture & Tech StackCurrent Frontend StackHTML5 / JavaScript (ES6+): Dynamic client-side application logic.Tailwind CSS: Modern utility-first styling with custom palette branding.Lucide Icons: UI icon set.Recommended Backend Stack (Target Implementation)Runtime / Framework: Node.js + Express.js / Python FastApi / Django.Database: PostgreSQL (Spatial PostGIS support recommended for Mandi geographic routes) or MongoDB.ORM / ODM: Prisma / Sequelize / Mongoose.Authentication: JWT with Role-Based Access Control (RBAC).Integrations:WhatsApp Business API (Twilio / Meta Graph API) for SMS/WhatsApp harvest receipts.Payment Gateway (Razorpay / UPI Direct) for immediate payment processing.Govt Mandi API / Agmarknet API integration for live market price updates.🔑 Key Features & User RolesPersonaCore Responsibilities👨‍🌾 FarmerPost harvest listings, check real-time Mandi vs. MSP rates, receive order confirmations.🏭 Procurement / VendorBrowse live harvest listings, match bulk demand orders, clear payment settlements.🤝 NGO / Food RescuerBrowse available surplus meals nearby, reserve pickup batches before expiry.📊 Platform AdminMonitor district stats, resolve farmer grievances, oversee route optimization algorithms.🚀 Recommended Backend API Endpoint Specifications1. Mandi & Market PricesGET /api/v1/mandi/ratesQuery Params: ?crop={name}&district={district}Description: Fetch live MSP and Mandi market benchmarks.2. Farmer Harvest Listings & ProcurementPOST /api/v1/procurement/listingsPayload: { farmerName, cropType, quantityQuintals, pricePerQuintal, location, whatsappAlerts: boolean }Description: Record a new harvest entry from the Farmer Pocket Ledger.GET /api/v1/procurement/ordersQuery Params: ?status=Pending|Matched|In-TransitDescription: Retrieve orders filtered by procurement pipeline status.PATCH /api/v1/procurement/orders/:id/statusPayload: { status: "Matched" | "In-Transit" | "Completed" }3. Surplus Food Redistribution BridgePOST /api/v1/surplus/donationsPayload: { donorOrg, category, servings, pickupWindowHours, locationZone }Description: Broadcast a commercial food surplus batch.GET /api/v1/surplus/availableDescription: Get active, unreserved surplus batches within valid pickup timeframes.POST /api/v1/surplus/reserve/:idPayload: { ngoId, estimatedPickupTime }Description: Reserve a surplus batch and issue a pickup pass.4. Logistics & Smart Route EnginePOST /api/v1/logistics/smart-matchPayload: { cropType, quantity, originDistrict }Description: Run route optimization between harvest hubs and destination warehouses.GET /api/v1/logistics/pass/:orderIdDescription: Generate digital transit pass (QR & cryptographic hash).5. Support & GrievancesPOST /api/v1/support/grievancePayload: { name, category, issueDetails }Description: Create a tracked support ticket for district agricultural officers.🗄️ Database Schemas (Data Models)FarmerListing{
  "_id": "ObjectId",
  "farmerName": "String",
  "cropType": "String",
  "quantityQuintals": "Number",
  "expectedPriceQuintal": "Number",
  "district": "String",
  "status": "Pending | Matched | In-Transit | Completed",
  "createdAt": "Timestamp"
}
SurplusFood{
  "_id": "ObjectId",
  "donorName": "String",
  "category": "String",
  "servings": "Number",
  "pickupWindow": "String",
  "locationZone": "String",
  "isReserved": "Boolean",
  "reservedByNGO": "String (Optional)",
  "createdAt": "Timestamp"
}
🔧 Setup & DeploymentClone the repository.Open index.html in any web browser or serve via a static web server.Configure environment variables in the upcoming backend service:PORT=5000
DATABASE_URL=postgresql://user:pass@localhost:5432/annasetu
JWT_SECRET=your_jwt_secret_here
WHATSAPP_API_KEY=your_whatsapp_token
🤝 Contribution GuidelinesWhen integrating the backend APIs:Ensure all database actions send normalized responses matching the frontend payload expectations.Maintain strict CORS policies for production domains.Implement input validation (e.g., using Joi or Zod) on procurement quantities and pickup times.
