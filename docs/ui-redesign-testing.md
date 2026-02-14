# UI Redesign Testing Guide

## Automated Tests

Run smoke tests:
```bash
python tests/test_ui_redesign.py
```

## Manual Testing

### Start App
```bash
streamlit run app.py
```

### Visual Checklist

**Color Scheme:**
- [ ] Primary blue (#2563eb) used for CTAs
- [ ] Slate grays for text and backgrounds
- [ ] Green/orange/red for status indicators
- [ ] No vibrant or clashing colors

**Design Elements:**
- [ ] No drop shadows
- [ ] No gradients
- [ ] Subtle borders only (1px, #e2e8f0)
- [ ] Consistent border radius (4-6px)

**Typography:**
- [ ] Clean sans-serif font
- [ ] Proper heading hierarchy
- [ ] Readable line heights (1.5-1.6)
- [ ] No overly large or small text

**Spacing:**
- [ ] Consistent 8px grid spacing
- [ ] Generous whitespace
- [ ] No cramped sections

**Components:**
- [ ] Cards have proper borders and padding
- [ ] Status badges show correct colors
- [ ] Form inputs focus with blue border
- [ ] Buttons have proper hover states

**Pages:**
- [ ] Welcome: Action buttons display correctly
- [ ] Wizard: Progress bar styled properly
- [ ] Editor: YAML preview has code styling
- [ ] Deploy: Status displays work
- [ ] Sidebar: Connection status card works

**Functionality:**
- [ ] All existing features work unchanged
- [ ] Navigation between pages works
- [ ] Form submissions work
- [ ] Connection/auth flow works
- [ ] Save/load functionality works
