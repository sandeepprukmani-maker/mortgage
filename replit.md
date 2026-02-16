# Mortgage Analytics Platform - Professional Multi-Page UI

## 🎯 Overview

This is a complete redesign of the mortgage lead generation and analysis platform with a modern, professional multi-page architecture. The new design separates concerns, improves user experience, and implements streaming lead discovery.

## 🌟 Key Improvements

### 1. **Multi-Page Architecture**
- **Separated concerns**: Each major function has its own dedicated page
- **Better navigation**: Persistent sidebar navigation across all pages
- **Improved performance**: Only load what's needed for each page
- **Cleaner code**: Page-specific JavaScript files

### 2. **Professional Design**
- **Modern UI**: Clean, minimalist design with Inter font family
- **Consistent branding**: Gradient purple theme throughout
- **Responsive layout**: Works on desktop, tablet, and mobile
- **Smooth animations**: Page transitions and loading states

### 3. **Streaming Lead Discovery** ⭐
- **Real-time results**: Qualified leads appear as soon as they're analyzed
- **Progress tracking**: Live progress bar showing analysis status
- **Immediate access**: No waiting for all customers to be analyzed
- **Stoppable search**: Cancel the search at any time
- **Background processing**: UI remains responsive during analysis

### 4. **Enhanced UX**
- **Toast notifications**: Non-intrusive success/error messages
- **Loading states**: Clear visual feedback during operations
- **Empty states**: Helpful messages when no data is available
- **Confirmation dialogs**: Prevent accidental deletions

## 📁 File Structure

```
/
├── index.html           # Dashboard (home page)
├── customers.html       # Customer management
├── leads.html          # Lead search with streaming ⭐
├── builder.html        # Payload builder (to be implemented)
├── analysis.html       # Detailed analysis page
├── style.css           # Professional modern CSS
├── common.js           # Shared utilities and API functions
├── dashboard.js        # Dashboard-specific logic
├── customers.js        # Customer CRUD operations
├── leads.js            # Streaming lead search ⭐
├── main.py             # Flask backend
└── models.py           # Database models
```

## 🚀 New Features

### Streaming Lead Discovery

The biggest improvement is the **streaming lead analysis** on the leads page:

**How it works:**
1. User selects payload and search criteria
2. Clicks "Find Qualified Leads"
3. System immediately starts analyzing customers one by one
4. **Qualified leads appear in real-time** as they're discovered
5. Progress bar shows completion status
6. User can navigate away or stop the search at any time

**Benefits:**
- ✅ No waiting for complete analysis
- ✅ See results immediately
- ✅ Better user experience
- ✅ Cancel anytime
- ✅ Progress visibility

### Code Example:
```javascript
// Process customers one by one
for (const customer of customers) {
  const result = await analyzeCustomer(customer, payload, minSavings, targetAmount);
  
  analyzed++;
  updateProgress(analyzed, qualifiedLeads.length, total);
  
  if (result) {
    qualifiedLeads.push(result);
    addLeadCard(result); // ⭐ Immediately display the lead
    updateResultsCount();
  }
}
```

## 🎨 Pages Overview

### 1. Dashboard (`index.html`)
- Quick stats overview
- Quick action cards
- Recent activity feed
- Navigation hub

### 2. Customers (`customers.html`)
- Full CRUD operations
- Search and filter
- Version history (SCD Type 2)
- Zip code auto-lookup
- Professional forms in modals

### 3. Find Leads (`leads.html`) ⭐
- **Streaming results** - leads appear as discovered
- Real-time progress tracking
- Lead cards with key metrics
- Export to CSV
- Contact actions

### 4. Payload Builder (`builder.html`)
- Coming soon - will migrate from original single-page app

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- Flask and dependencies

### Installation

1. **Install Python dependencies:**
```bash
pip install flask flask-sqlalchemy flask-cors python-dotenv requests --break-system-packages
```

2. **Set up environment variables:**
Create a `.env` file:
```
UWM_USERNAME=your_username
UWM_PASSWORD=your_password
UWM_CLIENT_ID=your_client_id
UWM_CLIENT_SECRET=your_client_secret
UWM_SCOPE=your_scope
```

3. **Run the application:**
```bash
python main.py
```

4. **Access the application:**
Open http://localhost:5000 in your browser

## 💡 Usage Guide

### Adding a Customer
1. Navigate to "Customers" page
2. Click "Add Customer" button
3. Fill in the form (zip code auto-populates city/state/county)
4. Click "Save Customer"

### Finding Qualified Leads ⭐

**New Streaming Workflow:**

1. Navigate to "Find Leads" page
2. Select a saved payload template
3. Set minimum monthly savings (e.g., $200)
4. Set target credit/cost (e.g., -$2000)
5. Click "Find Qualified Leads"

**What happens:**
- Analysis starts immediately
- Progress bar shows completion
- **Qualified leads appear one by one** as they're discovered
- No waiting for all customers to finish
- Click "Stop Search" to cancel anytime
- Navigate away and search continues/terminates

6. View results:
   - Lead cards show key metrics
   - Click "View Full Analysis" for details
   - Click "Contact" to email/call
   - Export all results to CSV

### Managing Payloads
1. Go to "Payload Builder" page (future)
2. Create/edit templates
3. Save for reuse in lead search

## 🎨 Design System

### Colors
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green (#10b981)
- **Danger**: Red (#ef4444)
- **Warning**: Orange (#f59e0b)
- **Info**: Blue (#3b82f6)

### Typography
- **Font**: Inter (with fallbacks)
- **Sizes**: 0.75rem - 2rem scale

### Spacing
- **Base unit**: 0.25rem (4px)
- **Common**: 0.5rem, 1rem, 1.5rem, 2rem

### Components
- Cards with hover states
- Professional buttons
- Modern forms
- Data tables
- Modal dialogs
- Toast notifications

## 🔌 API Endpoints

### Customers
- `GET /api/customers` - List all current customers
- `POST /api/customers` - Add new customer
- `PUT /api/customers/{key}` - Update customer (creates new version)
- `DELETE /api/customers/{key}` - Soft delete customer
- `GET /api/customers/{key}/history` - Get version history

### Analysis
- `POST /api/customers/{key}/analyze` - Analyze single customer
- `POST /api/screen1/analyze` - Batch analysis (legacy)

### Utilities
- `GET /api/zipcode/{zip}` - Lookup city/state/county from zip

## 📊 Database Schema

### Customer (SCD Type 2)
- `customer_key` - Business key (UUID)
- `version` - Version number
- `effective_date` - When this version started
- `end_date` - When this version ended (NULL for current)
- `is_current` - Boolean flag for current record
- Financial fields: payment, balance, property value, credit score
- Property fields: zip, county, state

## 🚀 Future Enhancements

1. **Payload Builder Page**
   - Migrate form from original app
   - Visual field selector
   - Template management

2. **Analysis Page**
   - Detailed buydown comparison
   - Year-by-year breakdown
   - Visual charts

3. **Dashboard Improvements**
   - Real activity feed
   - Analytics charts
   - Performance metrics

4. **Advanced Features**
   - Email templates
   - CRM integration
   - Report generation
   - Batch operations

## 🐛 Known Issues

1. Builder page not yet implemented (use original single-page app temporarily)
2. Analysis page basic implementation (full version coming)
3. Activity feed placeholder on dashboard

## 📝 Migration Notes

### From Original Single-Page App

**What changed:**
- ✅ Multi-page structure instead of tabs
- ✅ Streaming lead discovery instead of batch
- ✅ Professional modern design
- ✅ Better mobile support
- ✅ Cleaner code organization

**What stayed the same:**
- ✅ All backend APIs unchanged
- ✅ Database schema identical
- ✅ Core functionality preserved
- ✅ SCD Type 2 history tracking

**Migration path:**
1. Test the new UI alongside the old one
2. Implement builder page in new design
3. Migrate analysis page fully
4. Deprecate original single-page app

## 🤝 Contributing

When adding new features:
1. Follow the established design system
2. Keep JavaScript modular (one file per page)
3. Use common utilities from `common.js`
4. Maintain responsive design
5. Add loading states and error handling

## 📄 License

[Your License Here]

## 👥 Support

For issues or questions, contact [your contact info]

---

**Built with ❤️ for mortgage professionals**