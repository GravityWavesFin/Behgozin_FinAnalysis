# 🚀 Behgozin v2.0 - Flask Web App Architecture

**Target Release**: Q1 2026 (فروردین 1405)  
**Code Name**: "Interactive Phoenix"  
**Status**: 🔧 In Planning

---

## 🎯 هدف اصلی

تبدیل سیستم تحلیل بنیادی به یک **وب اپلیکیشن تعاملی** با قابلیت:
1. **Sensitivity Analysis**: تحلیل حساسیت با تغییر مفروضات
2. **Real-time Recalculation**: محاسبه مجدد فوری
3. **Stock-Specific Value Drivers**: ولودرایورهای خاص هر سهم
4. **Interactive Dashboard**: داشبورد تعاملی

---

## 🏗️ معماری

### **Tech Stack:**

```
Backend:
├── Flask 3.0+                  # Web framework
├── Flask-SQLAlchemy           # ORM
├── Flask-Migrate              # Database migrations
├── Flask-Login                # Authentication
├── Flask-CORS                 # CORS handling
├── Celery                     # Background tasks
├── Redis                      # Cache & message broker
└── PostgreSQL / SQLite        # Database

Frontend:
├── HTML5, CSS3, JavaScript
├── Bootstrap 5 / Tailwind CSS
├── Chart.js 4.4+ 
├── Alpine.js / Vue.js         # Reactivity
├── Socket.IO                  # Real-time updates
└── HTMX                       # AJAX interactions

Deployment:
├── Docker + Docker Compose
├── Gunicorn (WSGI)
├── Nginx (Reverse proxy)
└── GitHub Actions (CI/CD)
```

---

## 📐 Project Structure

```
Behgozin_Flask/
│
├── app/
│   ├── __init__.py                # App factory
│   ├── config.py                  # Configuration classes
│   ├── extensions.py              # Flask extensions
│   │
│   ├── models/                    # Database models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   ├── stock.py               # Stock model
│   │   ├── valuation.py           # Valuation model
│   │   ├── assumptions.py         # Assumptions model
│   │   └── analysis.py            # Analysis history model
│   │
│   ├── controllers/               # Business logic
│   │   ├── __init__.py
│   │   ├── valuation_controller.py
│   │   ├── sensitivity_controller.py
│   │   ├── comparison_controller.py
│   │   └── report_controller.py
│   │
│   ├── services/                  # Core services (from v1.0 src/)
│   │   ├── __init__.py
│   │   ├── financial_parser.py    # MHTML parsing
│   │   ├── data_extractor.py      # Data extraction
│   │   ├── valuation.py           # 6 valuation methods
│   │   ├── comprehensive_financial_ratios.py
│   │   ├── fundamental_analysis.py
│   │   ├── visualization.py       # Chart generation
│   │   └── price_data_extractor.py
│   │
│   ├── api/                       # REST API endpoints
│   │   ├── __init__.py
│   │   ├── valuation.py           # /api/valuation
│   │   ├── sensitivity.py         # /api/sensitivity
│   │   ├── stocks.py              # /api/stocks
│   │   └── analysis.py            # /api/analysis
│   │
│   ├── views/                     # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py                # Home, about, etc.
│   │   ├── auth.py                # Login, register
│   │   ├── analysis.py            # Analysis pages
│   │   ├── sensitivity.py         # Sensitivity analysis
│   │   └── dashboard.py           # User dashboard
│   │
│   ├── templates/                 # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── analysis/
│   │   │   ├── stock_detail.html
│   │   │   ├── sensitivity.html
│   │   │   └── comparison.html
│   │   ├── dashboard/
│   │   │   ├── dashboard.html
│   │   │   └── history.html
│   │   └── components/
│   │       ├── navbar.html
│   │       ├── sidebar.html
│   │       ├── chart.html
│   │       ├── assumptions_panel.html
│   │       └── value_drivers.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── dashboard.css
│   │   │   └── sensitivity.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── sensitivity.js     # Real-time updates
│   │   │   ├── charts.js
│   │   │   └── api_client.js
│   │   ├── images/
│   │   └── fonts/
│   │       └── IRANSans/
│   │
│   └── utils/
│       ├── __init__.py
│       ├── persian_utils.py
│       ├── validators.py
│       └── helpers.py
│
├── migrations/                    # Alembic migrations
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_valuation.py
│   └── test_sensitivity.py
│
├── tasks/                         # Celery tasks
│   ├── __init__.py
│   ├── data_refresh.py           # Auto-update from CODAL
│   └── report_generation.py
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── run.py                         # Development server
├── wsgi.py                        # Production WSGI
├── celery_worker.py              # Celery worker
└── README.md
```

---

## 🎨 Key Features

### 1️⃣ **Interactive Sensitivity Analysis**

#### **Assumptions Panel (سمت راست صفحه):**
```html
<div class="assumptions-panel">
  <h3>مفروضات ارزشگذاری - زفجر</h3>
  
  <!-- DCF Assumptions -->
  <div class="assumption-group">
    <h4>DCF Model</h4>
    
    <label>نرخ رشد درآمد (%)</label>
    <input type="range" id="revenue_growth" 
           min="0" max="30" value="10" step="1"
           oninput="updateValuation()">
    <span id="revenue_growth_val">10%</span>
    
    <label>WACC (%)</label>
    <input type="range" id="wacc" 
           min="8" max="20" value="12" step="0.5"
           oninput="updateValuation()">
    <span id="wacc_val">12%</span>
    
    <label>Terminal Growth Rate (%)</label>
    <input type="range" id="terminal_growth" 
           min="1" max="5" value="3" step="0.5"
           oninput="updateValuation()">
    <span id="terminal_growth_val">3%</span>
  </div>
  
  <!-- Stock-Specific Value Drivers -->
  <div class="value-drivers">
    <h4>⚡ ولودرایورهای خاص</h4>
    
    <label>قیمت دلار (تومان)</label>
    <input type="number" id="usd_price" 
           value="60000" step="1000"
           oninput="updateValuation()">
    
    <label>قیمت گندم جهانی ($/تن)</label>
    <input type="number" id="wheat_price" 
           value="250" step="10"
           oninput="updateValuation()">
  </div>
  
  <button onclick="resetDefaults()">بازگشت به پیش‌فرض</button>
</div>
```

#### **Real-time Chart Update:**
```javascript
// sensitivity.js
function updateValuation() {
    // Get all assumption values
    const assumptions = {
        revenue_growth: $('#revenue_growth').val(),
        wacc: $('#wacc').val(),
        terminal_growth: $('#terminal_growth').val(),
        usd_price: $('#usd_price').val(),
        wheat_price: $('#wheat_price').val()
    };
    
    // Call API
    $.ajax({
        url: '/api/sensitivity/calculate',
        method: 'POST',
        data: JSON.stringify(assumptions),
        contentType: 'application/json',
        success: function(response) {
            // Update chart with new valuation levels
            updateChart(response.valuation_levels);
            
            // Update summary table
            updateSummaryTable(response.summary);
            
            // Show change indicators
            showChanges(response.changes);
        }
    });
}

// Debounce for performance
const debouncedUpdate = debounce(updateValuation, 300);
```

### 2️⃣ **Stock-Specific Value Drivers**

#### **Database Model:**
```python
# app/models/value_driver.py
class ValueDriver(db.Model):
    __tablename__ = 'value_drivers'
    
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    driver_name = db.Column(db.String(100))  # 'usd_price', 'wheat_price', etc.
    driver_label = db.Column(db.String(100))  # 'قیمت دلار', 'قیمت گندم'
    driver_unit = db.Column(db.String(50))    # 'تومان', '$/تن'
    default_value = db.Column(db.Float)
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    sensitivity_score = db.Column(db.Float)   # 0-100 (میزان حساسیت)
    
    stock = db.relationship('Stock', backref='value_drivers')
```

#### **Value Drivers Configuration:**
```python
# config/value_drivers.py
VALUE_DRIVERS_CONFIG = {
    'زفجر': [
        {
            'name': 'usd_price',
            'label': 'قیمت دلار',
            'unit': 'تومان',
            'default': 60000,
            'min': 40000,
            'max': 80000,
            'sensitivity': 95,  # High sensitivity
            'impact': 'revenue'  # Affects revenue
        },
        {
            'name': 'wheat_price',
            'label': 'قیمت گندم جهانی',
            'unit': '$/تن',
            'default': 250,
            'min': 180,
            'max': 350,
            'sensitivity': 85,
            'impact': 'revenue'
        },
        {
            'name': 'subsidy',
            'label': 'یارانه دولتی',
            'unit': 'میلیارد ریال',
            'default': 500,
            'min': 0,
            'max': 1000,
            'sensitivity': 60,
            'impact': 'operating_cost'
        }
    ],
    
    'کاوه': [
        {
            'name': 'aluminum_price',
            'label': 'قیمت آلومینیوم جهانی',
            'unit': '$/تن',
            'default': 2500,
            'min': 2000,
            'max': 3500,
            'sensitivity': 90,
            'impact': 'revenue'
        },
        {
            'name': 'electricity_price',
            'label': 'قیمت برق',
            'unit': 'ریال/کیلووات',
            'default': 1500,
            'min': 1000,
            'max': 2500,
            'sensitivity': 75,
            'impact': 'operating_cost'
        }
    ],
    
    'رنیک': [
        {
            'name': 'copper_price',
            'label': 'قیمت مس جهانی',
            'unit': '$/تن',
            'default': 9000,
            'min': 7000,
            'max': 12000,
            'sensitivity': 95,
            'impact': 'revenue'
        },
        {
            'name': 'extraction_cost',
            'label': 'هزینه استخراج',
            'unit': 'میلیون ریال/تن',
            'default': 250,
            'min': 200,
            'max': 350,
            'sensitivity': 70,
            'impact': 'operating_cost'
        }
    ]
}
```

### 3️⃣ **Sensitivity API Endpoint**

```python
# app/api/sensitivity.py
from flask import Blueprint, request, jsonify
from app.services.valuation import ValuationService
from app.controllers.sensitivity_controller import SensitivityController

bp = Blueprint('sensitivity_api', __name__, url_prefix='/api/sensitivity')

@bp.route('/calculate', methods=['POST'])
def calculate_sensitivity():
    """
    محاسبه ارزشگذاری با مفروضات جدید
    
    Request Body:
    {
        "stock_symbol": "زفجر",
        "assumptions": {
            "revenue_growth": 15,
            "wacc": 12,
            "terminal_growth": 3,
            "usd_price": 65000,
            "wheat_price": 280
        }
    }
    
    Response:
    {
        "valuation_levels": {
            "dcf_optimistic": 25000,
            "dcf_neutral": 22000,
            "dcf_pessimistic": 19000,
            ...
        },
        "summary": {
            "weighted_average": 21500,
            "current_price": 21550,
            "upside": -0.23
        },
        "changes": {
            "dcf_neutral": {
                "old": 20000,
                "new": 22000,
                "change_pct": 10.0
            }
        }
    }
    """
    data = request.get_json()
    
    stock_symbol = data['stock_symbol']
    assumptions = data['assumptions']
    
    # Calculate with new assumptions
    controller = SensitivityController()
    result = controller.calculate_with_assumptions(stock_symbol, assumptions)
    
    return jsonify(result)

@bp.route('/value-drivers/<stock_symbol>', methods=['GET'])
def get_value_drivers(stock_symbol):
    """
    دریافت لیست ولودرایورهای خاص یک سهم
    
    Response:
    {
        "drivers": [
            {
                "name": "usd_price",
                "label": "قیمت دلار",
                "unit": "تومان",
                "default": 60000,
                "min": 40000,
                "max": 80000,
                "sensitivity": 95
            },
            ...
        ]
    }
    """
    controller = SensitivityController()
    drivers = controller.get_value_drivers(stock_symbol)
    
    return jsonify({'drivers': drivers})
```

### 4️⃣ **Sensitivity Controller**

```python
# app/controllers/sensitivity_controller.py
from app.services.valuation import ValuationService
from config.value_drivers import VALUE_DRIVERS_CONFIG

class SensitivityController:
    
    def __init__(self):
        self.valuation_service = ValuationService()
    
    def calculate_with_assumptions(self, stock_symbol, assumptions):
        """محاسبه ارزشگذاری با مفروضات جدید"""
        
        # 1. Load stock data
        stock_data = self.load_stock_data(stock_symbol)
        
        # 2. Apply value drivers to financial data
        adjusted_data = self.apply_value_drivers(stock_data, assumptions)
        
        # 3. Recalculate valuation with new assumptions
        valuation_result = self.valuation_service.calculate_all_methods(
            stock_data=adjusted_data,
            dcf_assumptions={
                'revenue_growth': assumptions.get('revenue_growth', 10),
                'wacc': assumptions.get('wacc', 12) / 100,
                'terminal_growth': assumptions.get('terminal_growth', 3) / 100
            },
            pe_assumptions={...},
            pb_assumptions={...}
        )
        
        # 4. Calculate changes from baseline
        baseline = self.get_baseline_valuation(stock_symbol)
        changes = self.calculate_changes(baseline, valuation_result)
        
        # 5. Return results
        return {
            'valuation_levels': valuation_result['levels'],
            'summary': valuation_result['summary'],
            'changes': changes
        }
    
    def apply_value_drivers(self, stock_data, assumptions):
        """اعمال تغییرات ولودرایورها به داده‌های مالی"""
        
        adjusted = stock_data.copy()
        
        # مثال: قیمت دلار
        if 'usd_price' in assumptions:
            usd_change = assumptions['usd_price'] / 60000  # baseline
            adjusted['revenue'] *= usd_change
        
        # مثال: قیمت گندم
        if 'wheat_price' in assumptions:
            wheat_change = assumptions['wheat_price'] / 250  # baseline
            adjusted['revenue'] *= wheat_change
        
        return adjusted
    
    def get_value_drivers(self, stock_symbol):
        """دریافت لیست ولودرایورهای خاص سهم"""
        return VALUE_DRIVERS_CONFIG.get(stock_symbol, [])
```

---

## 📊 Database Schema

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stocks
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial Data
CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    period_end_date DATE NOT NULL,
    revenue BIGINT,
    net_income BIGINT,
    total_assets BIGINT,
    total_equity BIGINT,
    operating_cash_flow BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Valuations
CREATE TABLE valuations (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    user_id INTEGER REFERENCES users(id),
    valuation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Assumptions (JSON)
    assumptions JSONB,
    
    -- Results
    dcf_optimistic DECIMAL,
    dcf_neutral DECIMAL,
    dcf_pessimistic DECIMAL,
    pe_optimistic DECIMAL,
    pe_neutral DECIMAL,
    pe_pessimistic DECIMAL,
    pb_optimistic DECIMAL,
    pb_neutral DECIMAL,
    pb_pessimistic DECIMAL,
    ev_ebitda_optimistic DECIMAL,
    ev_ebitda_neutral DECIMAL,
    ev_ebitda_pessimistic DECIMAL,
    ps_optimistic DECIMAL,
    ps_neutral DECIMAL,
    ps_pessimistic DECIMAL,
    rim_optimistic DECIMAL,
    rim_neutral DECIMAL,
    rim_pessimistic DECIMAL,
    
    weighted_average DECIMAL,
    current_price DECIMAL,
    upside_pct DECIMAL
);

-- Value Drivers
CREATE TABLE value_drivers (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    driver_name VARCHAR(50),
    driver_label VARCHAR(100),
    driver_unit VARCHAR(20),
    default_value DECIMAL,
    min_value DECIMAL,
    max_value DECIMAL,
    sensitivity_score INTEGER  -- 0-100
);

-- Analysis History
CREATE TABLE analysis_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    stock_id INTEGER REFERENCES stocks(id),
    valuation_id INTEGER REFERENCES valuations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Development Roadmap

### **Phase 1: Setup & Migration (1 هفته)**
- [ ] ایجاد ساختار پروژه Flask
- [ ] تنظیم Docker & Docker Compose
- [ ] Migration کدهای v1.0 به services/
- [ ] تنظیم Database (PostgreSQL/SQLite)
- [ ] ایجاد models و migrations

### **Phase 2: Core API (2 هفته)**
- [ ] REST API برای ارزشگذاری
- [ ] Sensitivity Analysis API
- [ ] Stock data API
- [ ] تست API endpoints

### **Phase 3: Frontend - Basic (2 هفته)**
- [ ] صفحه اصلی و navigation
- [ ] صفحه جزئیات سهم
- [ ] نمایش گزارش بنیادی
- [ ] Chart.js integration

### **Phase 4: Sensitivity Analysis UI (3 هفته)**
- [ ] Assumptions panel
- [ ] Real-time slider updates
- [ ] Value drivers interface
- [ ] WebSocket/AJAX integration
- [ ] Change indicators

### **Phase 5: User System (1 هفته)**
- [ ] Authentication (register, login)
- [ ] User dashboard
- [ ] Analysis history
- [ ] Save/load analysis

### **Phase 6: Background Tasks (1 هفته)**
- [ ] Celery setup
- [ ] Auto-refresh data from CODAL
- [ ] Scheduled report generation
- [ ] Email notifications

### **Phase 7: Testing & QA (2 هفته)**
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Load testing
- [ ] Bug fixes

### **Phase 8: Deployment (1 هفته)**
- [ ] Production setup
- [ ] CI/CD pipeline
- [ ] Monitoring & logging
- [ ] Documentation

**Total: ~13 هفته (3 ماه)**

---

## 📝 Git Workflow

```bash
# Main branches
main          # Production
develop       # Development
feature/*     # Features
bugfix/*      # Bug fixes
hotfix/*      # Hot fixes

# Release process
git checkout -b release/v2.0
# Testing & final changes
git checkout main
git merge release/v2.0
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin main --tags
```

---

## 🎯 Success Metrics

### **Performance:**
- API response time < 500ms
- Real-time update latency < 100ms
- Page load time < 2s

### **Quality:**
- Test coverage > 80%
- Zero critical bugs
- All features working

### **User Experience:**
- Intuitive UI
- Mobile responsive
- Fast interactions

---

**تاریخ ایجاد**: 15 نوامبر 2025  
**وضعیت**: 📋 Planning Phase  
**Target Release**: Q1 2026 (فروردین 1405)
