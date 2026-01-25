# Export Stats Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Export Stats            [Preview]    │
├─────────────────────────────────────────┤
│                                         │
│  Game Selection                         │
│  ┌─────────────────────────────────┐  │
│  │ All Games                  [▼] │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Time Range                             │
│  ┌─────────────────────────────────┐  │
│  │ All Time                   [▼] │  │
│  └─────────────────────────────────┘  │
│  ┌──────────┐  ┌──────────┐          │
│  │ From Date│  │ To Date  │          │
│  │ [01/01]  │  │ [12/31]  │          │
│  └──────────┘  └──────────┘          │
│                                         │
│  Stat Type                              │
│  ┌─────────────────────────────────┐  │
│  │ All Stats                  [▼] │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Session Selection                      │
│  ┌─────────────────────────────────┐  │
│  │ All Sessions              [▼] │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Stat Set                               │
│  ┌─────────────────────────────────┐  │
│  │ All Sets                   [▼] │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Preview                                │
│  ┌─────────────────────────────────┐  │
│  │ ~150 sessions                    │  │
│  │ ~2,500 stat values               │  │
│  │ Estimated size: ~500 KB          │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Export to JSON              │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Export Stats" (20sp Roboto Medium)
- **Actions**: Preview button (14sp Roboto Medium, primary color)
- **Back Button**: 24dp

### Game Selection
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Game Selection"
- **Options**: "All Games", "Specific Game", "Multiple Games"
- **Multi-select**: Supported for "Multiple Games"
- **Position**: 16dp below app bar

### Time Range
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Time Range"
- **Options**: "All Time", "Last Week", "Last Month", "Last Year", "Custom Range"
- **Position**: 16dp below game selection

### Date Pickers (Custom Range)
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: "From Date" and "To Date"
- **Input Type**: Date picker
- **Visibility**: Shown when "Custom Range" selected
- **Position**: 8dp below time range selector
- **Layout**: Side by side, equal width

### Stat Type Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Stat Type"
- **Options**: "All Stats", "Specific Stat", "Multiple Stats"
- **Multi-select**: Supported for "Multiple Stats"
- **Position**: 16dp below date pickers

### Session Selection
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Session Selection"
- **Options**: "All Sessions", "Specific Sessions", "Multiple Sessions"
- **Multi-select**: Supported for "Multiple Sessions"
- **Position**: 16dp below stat type selector

### Stat Set Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Stat Set"
- **Options**: "All Sets", "Specific Set", "Multiple Sets"
- **Multi-select**: Supported for "Multiple Sets"
- **Position**: 16dp below session selection

### Preview Card
- **Type**: Info Card
- **Background**: Secondary color at 10% opacity
- **Border**: 1dp solid secondary color
- **Corner Radius**: 8dp
- **Padding**: 16dp
- **Content**:
  - "~X sessions" (16sp Roboto Medium)
  - "~Y stat values" (14sp Roboto Regular, secondary color)
  - "Estimated size: ~Z KB" (14sp Roboto Regular, secondary color)
- **Position**: 16dp below stat set selector
- **Update**: Updates when filters change

### Export to JSON Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Export to JSON" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Icon**: Download icon (18dp) on left
- **Position**: 16dp below preview, 16dp from bottom
- **Navigation**: → File system (save JSON)

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Selector Spacing**: 16dp vertical between selectors
- **Date Picker Spacing**: 8dp horizontal between pickers
- **Preview Spacing**: 16dp from stat set selector
- **Button Spacing**: 16dp from preview, 16dp from bottom

---

## States & Interactions

### Default State
- All selectors show default values
- Preview shows estimated data size
- Export button enabled

### Custom Range Selected
- Date pickers appear
- From and To dates can be selected
- Preview updates

### Multi-select States
- Game, Stat Type, Session, Stat Set support multi-select
- Selected items shown as chips
- Preview updates with selection

### Export State
- Export button shows loading spinner
- "Exporting..." text
- File save dialog appears
- Progress indicator during export

---

## Interactions

- **Select Filters**: Update preview in real-time
- **Tap Preview Button**: Show detailed preview (modal)
- **Tap Export to JSON**: Open file save dialog
- **Select Save Location**: Save JSON file

---

## File Save Dialog

### Layout
```
┌─────────────────────────────────────────┐
│            ═══                          │
│                                         │
│  Save Export                            │
├─────────────────────────────────────────┤
│                                         │
│  File Name                              │
│  ┌─────────────────────────────────┐  │
│  │ stats_export_2024-01-15.json    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Location                               │
│  [Downloads]                            │
│                                         │
│  ┌──────────┐  ┌──────────┐          │
│  │  Cancel  │  │   Save    │          │
│  └──────────┘  └──────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Accessibility

- **Screen Reader**: "Export stats. Game selection. Time range. [Selected options]. Export to JSON button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all selectors

---

## Navigation

- **Back Button**: → Settings Main Screen or Drawer Menu
- **Preview Button**: → Preview Modal
- **Export to JSON Button**: → File Save Dialog, then → Success state

---

**Wireframe Description Complete**
