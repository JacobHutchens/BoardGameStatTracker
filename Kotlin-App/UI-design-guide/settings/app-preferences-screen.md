# App Preferences Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← App Preferences                     │
├─────────────────────────────────────────┤
│                                         │
│  Appearance                             │
│  ┌─────────────────────────────────┐  │
│  │ Theme                            │  │
│  │ ────────────────────────────────│  │
│  │ Light                    [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Language                               │
│  ┌─────────────────────────────────┐  │
│  │ Language                        │  │
│  │ ────────────────────────────────│  │
│  │ English                  [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Data Usage                             │
│  ┌─────────────────────────────────┐  │
│  │ Auto-sync stats          [Toggle]│  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Sync over Wi-Fi only     [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Cache                                  │
│  ┌─────────────────────────────────┐  │
│  │ Clear Cache                      │  │
│  │ Free up storage space            │  │
│  │                          [Clear] │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "App Preferences" (20sp Roboto Medium)
- **Back Button**: 24dp

### Settings Section
- **Title**: Section name (16sp Roboto Medium)
- **Position**: 16dp below previous section
- **Spacing**: 24dp between sections

### Theme Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Theme"
- **Options**: "Light", "Dark", "System Default"
- **Position**: 16dp below section title

### Language Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Language"
- **Options**: "English", "Spanish", "French", etc.
- **Position**: 16dp below theme selector

### Data Usage Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Toggle switch (40dp track width) on right
- **Spacing**: 1dp divider between items

### Clear Cache Item
- **Type**: List Item (Two-Line)
- **Height**: 72dp
- **Padding**: 16dp horizontal
- **Content**:
  - "Clear Cache" (16sp Roboto Medium)
  - "Free up storage space" (14sp Roboto Regular, secondary color)
  - "Clear" button (Text button, 14sp Roboto Medium, primary color) on right
- **Confirmation**: Shows confirmation dialog before clearing

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items

---

## States & Interactions

### Default State
- All preferences displayed
- Current settings shown
- All toggles enabled

### Clear Cache Confirmation State
- Confirmation dialog appears
- "Clear cache? This will free up storage space." (16sp Roboto Regular)
- Actions: "Cancel" or "Clear"

---

## Interactions

- **Select Theme**: Change app theme immediately
- **Select Language**: Change app language (requires restart)
- **Toggle Auto-sync**: Enable/disable automatic stat syncing
- **Toggle Wi-Fi Only**: Restrict syncing to Wi-Fi only
- **Tap Clear Cache**: Show confirmation dialog

---

## Accessibility

- **Screen Reader**: "App preferences. Theme: [value]. Language: [value]."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all selectors

---

## Navigation

- **Back Button**: → Settings Main Screen

---

**Wireframe Description Complete**
