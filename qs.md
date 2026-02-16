# 🚀 Quick Start Guide

## What's New?

### ⭐ Streaming Lead Discovery (The Big Feature!)

**Old Way:**
1. Click "Find Leads"
2. Wait... ⏳
3. Wait more... ⏳⏳
4. Finally see all results at once

**New Way:**
1. Click "Find Qualified Leads"
2. See first qualified lead immediately! ✨
3. See second lead... ✨
4. See third lead... ✨
5. Keep seeing leads as they're discovered
6. Stop anytime or navigate away

**Why This Matters:**
- No more waiting for complete analysis
- Start contacting leads immediately
- Better user experience
- Can stop if you find enough leads
- Progress visibility

## 📁 New Structure

```
Multi-Page App (Instead of Single Page with Tabs)

index.html       → Dashboard with stats
customers.html   → Manage customers
leads.html       → Find leads (with streaming!)
builder.html     → Create payloads (coming soon)
```

## 🎯 Key Features

### 1. Professional Design
- Modern purple gradient theme
- Clean, minimal interface
- Responsive (works on mobile)
- Smooth animations

### 2. Better Navigation
- Sidebar always visible
- Active page highlighted
- Quick action cards on dashboard

### 3. Improved Forms
- Modal dialogs (not inline)
- Auto-populate zip code data
- Better validation
- Clear field labels

### 4. Enhanced Tables
- Hover effects
- Action buttons
- Badge indicators
- Empty states

## 📋 Common Tasks

### Add a Customer
```
1. Go to Customers page
2. Click "Add Customer"
3. Fill form (zip auto-populates!)
4. Save
```

### Find Qualified Leads (NEW!)
```
1. Go to Find Leads page
2. Select payload template
3. Set criteria:
   - Min savings: $200
   - Target amount: -$2000
4. Click "Find Qualified Leads"
5. Watch leads appear in real-time! ⭐
6. Export to CSV when done
```

### View Customer History
```
1. Go to Customers page
2. Find customer
3. Click "History" button
4. See all versions (SCD Type 2)
```

## 🔧 Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-cors python-dotenv requests --break-system-packages
```

### Step 2: Create .env File
```
UWM_USERNAME=your_username
UWM_PASSWORD=your_password
UWM_CLIENT_ID=your_client_id
UWM_CLIENT_SECRET=your_client_secret
UWM_SCOPE=your_scope
```

### Step 3: Run
```bash
python main.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

## 🎨 UI Highlights

### Dashboard
- Stats cards with icons
- Quick action tiles
- Recent activity feed

### Customers
- Search and filter
- Professional data table
- Modal forms
- History tracking

### Find Leads ⭐
- Streaming results
- Progress tracking
- Lead cards
- Export functionality

## 💾 Files to Deploy

Core files needed:
```
index.html
customers.html
leads.html
style.css
common.js
dashboard.js
customers.js
leads.js
main.py
models.py
```

Static file structure:
```
/static/
  index.html
  customers.html
  leads.html
  style.css
  common.js
  dashboard.js
  customers.js
  leads.js
```

## 🔄 Migration from Old UI

The old single-page app still works! You can use both:

**New UI:** Modern, multi-page, streaming leads
**Old UI:** Single page with tabs, batch processing

Gradually migrate to new UI as features are completed.

## 📊 Performance

### Streaming Leads vs Batch

**Scenario:** 100 customers, 10 qualify

**Old (Batch):**
- Wait time: 100 seconds
- First result: After 100 seconds
- Total time: 100 seconds

**New (Streaming):**
- Wait time: 0 seconds
- First result: ~10 seconds
- Last result: 100 seconds
- But you see results as they come! ⭐

## 🎯 Best Practices

### When Using Streaming Leads

1. **Set realistic criteria**
   - Don't make it too restrictive
   - You'll see if no one qualifies quickly

2. **Start reaching out immediately**
   - Don't wait for search to finish
   - Contact first few qualified leads right away

3. **Use the stop button**
   - Found enough leads? Stop the search
   - Saves processing time

4. **Export regularly**
   - Export results periodically
   - Don't lose your work

## 🐛 Troubleshooting

### No customers showing?
- Add some customers first on Customers page

### No payloads available?
- Create a payload template (use builder page or import JSON)

### Search not working?
- Check browser console for errors
- Verify backend is running
- Check .env credentials

### Leads not appearing?
- Check if customers meet criteria
- Verify customer data is complete
- Lower minimum savings threshold

## 📞 Support

Need help? Check the full README.md for detailed documentation.

---

**Happy analyzing! 🎉**