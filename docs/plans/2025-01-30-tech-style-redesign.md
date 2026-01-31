# Tech Style Redesign - Design Document

**Date:** 2025-01-30
**Project:** Databricks Metric View Builder
**Goal:** Redesign UI with professional analytics/visualization platform styling

## Design Overview

Transform the current Streamlit app from basic functional UI to a professional analytics platform interface with:
- Corporate analytics color scheme (slate grays, blues, orange/green accents)
- Minimal flat design (no shadows, gradients, or heavy effects)
- Mixed layout approach (cards for important content, open layout for forms)
- Clean typography and generous whitespace
- Data-focused, enterprise-grade aesthetic

## Design System

### Color Palette

**Backgrounds:**
- Primary (main content): `#ffffff` (white)
- Secondary: `#f8fafc` (very light slate)
- Tertiary: `#f1f5f9` (light gray)

**Text:**
- Headings: `#0f172a` (near black)
- Body: `#475569` (slate gray)
- Hints/Metadata: `#94a3b8` (light slate)

**Primary Colors:**
- Primary action: `#2563eb` (professional blue)
- Primary hover: `#1d4ed8` (darker blue)

**Status Colors:**
- Success: `#10b981` (green)
- Warning: `#f59e0b` (orange)
- Error: `#ef4444` (red)
- Pending: `#94a3b8` (gray)

**Borders:**
- Default border: `#e2e8f0` (subtle slate)

### Typography

**Font Family:**
- System font stack (San Francisco, Inter, Segoe UI, Roboto)

**Scale:**
- H1 (page titles): 28px, weight 600
- H2 (section titles): 24px, weight 600
- H3 (card titles): 20px, weight 600
- Body: 16px, weight 400
- Small: 14px, weight 400
- XSmall: 12px, weight 400

**Line Heights:**
- Headings: 1.2
- Body: 1.5-1.6

### Spacing System

Base unit: 4px
- XS: 4px
- SM: 8px
- MD: 16px
- LG: 24px
- XL: 32px
- XXL: 48px

### Visual Effects

**Design Philosophy:** Minimal flat design
- No shadows
- No gradients
- Subtle borders only (1px, solid #e2e8f0)
- Minimal hover states (light background changes)
- Clean, crisp edges
- Border radius: 4-6px (slightly rounded)

## Layout Structure

### Sidebar (Left Navigation)

**Header:**
- Logo area with "Metric View Builder" title
- Subtle bottom border (1px, #e2e8f0)
- 24px padding

**Connection Status Card:**
- Light gray background (#f8fafc)
- 1px border (#e2e8f0)
- Colored dot (8px circle) + status text
- 16px padding

**Navigation Section:**
- "Workflows" label (14px, uppercase, light gray)
- Text-based links (no icons for cleaner look)
- Active state: left blue border bar (3px, #2563eb) + darker background
- Hover state: light gray background

**Form Areas:**
- Grouped in subtle cards with light backgrounds
- Clear labels above inputs
- 8px spacing between elements

### Main Content Area

**Page Headers:**
- Large title (28px, weight 600)
- Subtitle in lighter gray (16px)
- Optional breadcrumb navigation
- 24px bottom margin

**Content Sections:**

**Card Style (for important content):**
```css
background: white
border: 1px solid #e2e8f0
border-radius: 6px
padding: 16px
margin-bottom: 16px
```

**Open Layout (for forms):**
- No borders
- Use spacing and labels to separate sections
- Inputs have 1px border that darkens on focus
- 24px vertical spacing between sections

## Component Specifications

### Buttons

**Primary (CTA):**
- Background: `#2563eb` (blue)
- Text: White
- Border: None
- Height: 40px
- Padding: 0 16px
- Border radius: 4px
- Hover: Background `#1d4ed8`
- Active: Same as hover

**Secondary:**
- Background: White
- Border: 1px solid `#e2e8f0`
- Text: `#475569` (slate)
- Hover: Background `#f8fafc`
- Same dimensions as primary

**Status Buttons:**
- Success: Green background (`#10b981`), white text
- Warning: Orange background (`#f59e0b`), white text
- Error: Red background (`#ef4444`), white text

### Form Inputs

**Text Fields:**
- Background: White
- Border: 1px solid `#e2e8f0`
- Height: 40px
- Padding: 0 12px
- Border radius: 4px
- Focus: Border `#2563eb` (blue)

**Labels:**
- Color: `#475569` (slate gray)
- Size: 14px
- Position: Above input (8px spacing)
- Weight: 500

**Select/Dropdowns:**
- Same styling as text fields
- Simple down arrow indicator

**Checkboxes/Radios:**
- Clean squares/circles (16px)
- Blue checkmark when selected (`#2563eb`)

### Cards

**Standard Card:**
```css
background: white
border: 1px solid #e2e8f0
border-radius: 6px
padding: 16px
margin-bottom: 16px
```

**Card with Header:**
- Header bar: Light gray background (`#f8fafc`)
- Header text: 18px, weight 600, color `#0f172a`
- Header padding: 12px 16px
- Content padding: 16px

### Status Indicators

**Inline Status:**
- Colored dot (8px circle)
- Text label (14px)
- No background box
- Colors: Green (success), Orange (warning), Red (error), Gray (pending)

### Code/YAML Preview

- Background: `#f8fafc` (light gray)
- Monospace font (14px)
- No border
- Syntax highlighting with subtle colors
- Padding: 16px
- Border radius: 4px

## Page Designs

### Welcome Page (app.py)

**Layout:**
- Hero section with title and description
- Connection status banner at top
- Three action cards in horizontal row
- Footer with version info

**Hero:**
- Title: "Databricks Metric View Builder" (28px, bold)
- Subtitle: "Create metric views without writing YAML or SQL" (16px, gray)
- 32px bottom margin

**Connection Banner:**
- Orange warning dot + "Not connected to Databricks" (if disconnected)
- Green success dot + "Connected to [workspace]" (if connected)

**Action Cards:**
- Three equal-width cards (32% width each)
- Each card:
  - White background, 1px border
  - Action name (20px, bold)
  - One-line description (14px, gray)
  - Clean button (no icon)
  - 24px padding

**Footer:**
- "v1.0.0 | Production Ready" (12px, gray)
- Centered at bottom

### Wizard Page (1_wizard.py)

**Layout:**
- Progress indicator at top
- Main content card for current step
- Right panel with live YAML preview

**Progress Indicator:**
- Horizontal bar with numbered steps
- Current step: blue background circle + blue bar
- Completed steps: checkmark in circle
- Pending steps: gray circle
- 40px height

**Step Card:**
- Header: "Step X: [Step Name]" (light gray background bar)
- Form inputs in open layout
- Buttons at bottom: "Next" (primary, right), "Back" (secondary)

**YAML Preview Panel:**
- Sticky on right
- Light gray background
- Syntax highlighted code
- Updates in real-time

### Editor Page (2_editor.py)

**Layout:**
- Top bar: File selection dropdown + "Load" button
- Two-column layout (70/30 split)

**Top Bar:**
- Left: Dropdown for saved files
- Right: "Load" button (primary)

**Left Column (70%):**
- Edit form sections in cards:
  - Source Configuration
  - Dimensions
  - Measures
  - Joins
- Each card: Expandable with subtle arrow
- Clicking expands to show form fields

**Right Column (30%):**
- YAML preview card (sticky)
- Action buttons:
  - Save
  - Export (Download/Copy)
  - Deploy
- Status messages

### Deploy Page (3_deploy.py)

**Layout:**
- Three deployment method cards
- Deployment configuration section
- Progress/status section

**Method Cards:**
- Horizontal row of three cards
- Each card: Method name, description, "Select" button
- Selected card: Blue border

**Configuration Section:**
- Form inputs for selected method
- Card style with header

**Progress Section:**
- Text status + loading spinner (if in progress)
- Success: Green card with white text
- Error: Red card with white text

## Implementation Plan

### Phase 1: Theme System
- Create `src/ui/theme.py` with CSS generation functions
- Define color constants
- Build helper functions for common styles

### Phase 2: Component Library
- Create `src/ui/components.py`
- Build reusable components:
  - Card component
  - StatusBadge component
  - Button wrapper functions
  - Form input helpers

### Phase 3: Main App Update
- Update `app.py` with new styling
- Apply new theme system
- Replace inline CSS with theme functions

### Phase 4: Page Updates
- Update welcome page (app.py)
- Update wizard page (1_wizard.py)
- Update editor page (2_editor.py)
- Update deploy page (3_deploy.py)

### Phase 5: Polish
- Review consistency across all pages
- Verify spacing alignment
- Test responsive behavior
- Ensure accessibility (contrast ratios)

## Technical Implementation

### File Structure
```
src/
├── ui/
│   ├── __init__.py
│   ├── theme.py          # CSS generation, color constants
│   └── components.py     # Reusable UI components
```

### Theme Module (src/ui/theme.py)
```python
# Color constants
COLORS = {
    'background': '#ffffff',
    'background_secondary': '#f8fafc',
    'background_tertiary': '#f1f5f9',
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_muted': '#94a3b8',
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'border': '#e2e8f0',
}

def get_custom_css() -> str:
    # Generate all CSS for the app
    pass

def card_style() -> str:
    # Return card CSS class
    pass

# More helper functions...
```

### Component Module (src/ui/components.py)
```python
import streamlit as st
from .theme import COLORS

def card(title=None, content=None):
    # Render a card component
    pass

def status_badge(status, text):
    # Render a status indicator
    pass

def primary_button(label, on_click, key=None):
    # Render a primary button
    pass

# More components...
```

## Success Criteria

✓ All pages use consistent color palette
✓ Minimal flat design (no shadows/gradients)
✓ Clean typography with proper hierarchy
✓ Generous whitespace (8px grid)
✓ Cards for important content, open layout for forms
✓ Responsive design works on different screen sizes
✓ No breaking changes to functionality
✓ All existing features work exactly the same

## Notes

- Focus on visual transformation only
- Keep all existing functionality intact
- Maintain accessibility standards
- Test on common screen resolutions
- Ensure color contrast meets WCAG AA standards
