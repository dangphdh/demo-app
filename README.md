# Databricks Metric View Builder

A Streamlit application that allows business users to visually create Databricks Metric Views without writing YAML or SQL.

## Status

- ✅ **Phase 1: Foundation** - Complete
- ✅ **Phase 2: Core Components** - Complete
- ✅ **Phase 3: User Experience** - Complete
- ✅ **Phase 4: Deployment & Tutorial** - Complete
- 🎉 **Production Ready** - All phases complete!

## Features

### All Features Implemented ✅

**Core Functionality:**
- 📹 **Visual Query Builder** - Create metric views without writing YAML/SQL
- 🔗 **Smart Join Configuration** - Canvas + form interface for table joins
- 🎯 **Dimension Builder** - Column-based and custom SQL expression dimensions
- 📈 **Measure Builder** - Simple presets and advanced SQL expressions
- 📊 **Live YAML Preview** - Syntax-highlighted YAML with validation
- ✅ **Validation** - Comprehensive error checking with suggestions

**User Experience:**
- 🧙‍♂️ **6-Step Wizard** - Guided workflow for first-time users
- 📝 **Editor Page** - Load, edit, and save metric views
- 💾 **Auto-save** - Session recovery for accidental closes
- 🎨 **Templates** - 3 pre-built templates to get started fast

**Deployment:**
- 🚀 **Deploy to Databricks** - Direct deployment via SQL Warehouse
- 📥 **Export Options** - Download YAML, copy to clipboard, save locally
- 📖 **Manual Deployment Guide** - Step-by-step instructions
- 🧪 **Test Queries** - Validate deployed metric views

**Learning:**
- 🎓 **Interactive Tutorial** - 6-step guided walkthrough
- 📚 **Help Center** - Comprehensive documentation
- 💡 **In-App Help** - Contextual help throughout the app
- 📖 **Best Practices** - Tips and examples

## Setup

### Option 1: Docker (Recommended)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Databricks credentials
# nano .env

# Build and run
docker-compose up --build
```

The app will be available at http://localhost:8501

### Option 2: Local Python

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Environment Variables

Create a `.env` file with the following:

```env
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your_access_token
DATABRICKS_WAREHOUSE_ID=your_warehouse_id
```

### Getting Databricks Credentials

1. **Host URL**: Your Databricks workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)

2. **Access Token**:
   - Go to your Databricks workspace
   - Click Settings → User Settings
   - Generate a new personal access token

3. **Warehouse ID**:
   - Go to SQL → SQL Warehouses
   - Click on your warehouse
   - Copy the Warehouse ID from the URL or details panel

## Project Structure

```
demo-app/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker orchestration
├── src/
│   ├── models/                 # Pydantic data models
│   │   ├── metric_view.py      # Main MetricView model
│   │   ├── dimension.py        # Dimension model
│   │   ├── measure.py          # Measure model
│   │   ├── join.py             # Join model
│   │   └── source.py           # Source model
│   ├── services/               # Business logic
│   │   ├── auth_manager.py     # Authentication handling
│   │   └── databricks_client.py # Databricks SDK wrapper
│   └── pages/                  # Multi-page structure
│       ├── 0_welcome.py        # Landing page
│       ├── 1_wizard.py         # Wizard flow
│       ├── 2_editor.py         # Edit metric views
│       └── 3_deploy.py         # Deploy/export
└── tests/                      # Test suite
    └── test_phase1.py          # Phase 1 tests
```

## Development Phases

### ✅ Phase 1: Foundation (Complete)

- [x] Project structure
- [x] Pydantic data models
- [x] Authentication manager
- [x] Databricks client wrapper
- [x] Basic Streamlit app
- [x] Docker configuration

**Deliverable**: Working app that can connect to Databricks and list tables

### ✅ Phase 2: Core Components (Complete)

- [x] Schema Browser component
- [x] Dimension Builder (column + custom)
- [x] Measure Builder (simple + advanced)
- [x] Join Visualizer (canvas + form)
- [x] YAML generator
- [x] Validation logic

**Deliverable**: Complete wizard flow that generates valid YAML

### ✅ Phase 3: User Experience (Complete)

- [x] Template system (3 templates)
- [x] Editor page with YAML preview
- [x] Save/load functionality
- [x] Auto-save and session recovery
- [x] Professional styling

**Deliverable**: Polished app with templates, editing, and persistence

### ✅ Phase 4: Deployment & Tutorial (Complete)

- [x] Deploy to Databricks functionality
- [x] Interactive tutorial (6 steps with checkpoints)
- [x] Educational content library (7 help topics)
- [x] Comprehensive test suite (all phases)

**Deliverable**: Production-ready app with deployment and learning resources

## Testing

Run the comprehensive test suite:

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python tests/test_all_phases.py
```

The test suite covers:
- Phase 1: Models (Pydantic validation)
- Phase 1: Services (Auth, Databricks client)
- Phase 2: YAML generator
- Phase 2: Validator
- Phase 3: Templates
- Phase 3: Storage (save/load/import/export)
- Phase 4: Deployment methods
- All import structure

## Documentation

- [Implementation Plan](/home/dangpdh/.claude/plans/jiggly-orbiting-newt.md)
- [Databricks Metric Views Documentation](https://docs.databricks.com/aws/en/metric-views/)

## License

MIT

## Contributing

This is a development project. Contributions welcome in Phase 2+.
