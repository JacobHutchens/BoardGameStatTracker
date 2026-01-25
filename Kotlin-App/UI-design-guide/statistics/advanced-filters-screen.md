# Advanced Stats Filter Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Advanced Filters        [Reset] [Save] │
├─────────────────────────────────────────┤
│                                         │
│  Game                                   │
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
│  Scope                                  │
│  ☑ Player Stats                         │
│  ☑ Table Stats                          │
│                                         │
│  Comparison                              │
│  ☐ Compare Games                        │
│  ☐ Compare Time Periods                 │
│  ☐ Compare Players                      │
│                                         │
│  Visualization                          │
│  ┌─────────────────────────────────┐  │
│  │ Chart                    [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Stat Set                               │
│  ┌─────────────────────────────────┐  │
│  │ All Sets                   [▼] │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Apply Filters              │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Advanced Filters" (20sp Roboto Medium)
- **Actions**: Reset button (14sp Roboto Medium, primary color), Save preset button (14sp Roboto Medium, primary color)

### Game Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Game"
- **Options**: "All Games", "Specific Game", "Multiple Games"
- **Multi-select**: Supported for "Multiple Games"
- **Position**: 16dp below app bar

### Time Range Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Time Range"
- **Options**: "All Time", "Last Week", "Last Month", "Last Year", "Custom Range"
- **Position**: 16dp below game selector

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

### Scope Checkboxes
- **Type**: Checkbox
- **Size**: 20dp x 20dp
- **Labels**: "Player Stats" and "Table Stats"
- **Position**: 16dp below stat type selector
- **Default**: Both checked
- **Layout**: Vertical list

### Comparison Options
- **Type**: Checkbox
- **Size**: 20dp x 20dp
- **Labels**: "Compare Games", "Compare Time Periods", "Compare Players"
- **Position**: 16dp below scope checkboxes
- **Default**: All unchecked
- **Layout**: Vertical list
- **Note**: Enables comparison mode in visualization

### Visualization Type Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Visualization"
- **Options**: "Chart", "Table", "Both"
- **Position**: 16dp below comparison options

### Stat Set Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Stat Set"
- **Options**: "All Sets", "Specific Set", "Multiple Sets"
- **Multi-select**: Supported for "Multiple Sets"
- **Position**: 16dp below visualization selector
- **Note**: Filter by stat sets used in sessions

### Apply Filters Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Apply Filters" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below stat set selector, 16dp from bottom
- **Navigation**: → Stat Visualization Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Selector Spacing**: 16dp vertical between selectors
- **Checkbox Spacing**: 8dp vertical between checkboxes
- **Date Picker Spacing**: 8dp horizontal between pickers
- **Button Spacing**: 24dp from last selector, 16dp from bottom

---

## States & Interactions

### Default State
- All selectors show default values
- Date pickers hidden (unless custom range selected)
- Both scope checkboxes checked
- All comparison options unchecked
- Apply Filters button enabled

### Custom Range Selected
- Date pickers appear
- From and To dates can be selected
- Validation: To date must be >= From date

### Multi-select States
- Game, Stat Type, Stat Set support multi-select
- Selected items shown as chips
- Remove chips to deselect

### Save Preset State
- Save button opens dialog
- Preset name input
- Save to user's filter presets

### Reset State
- All filters reset to defaults
- Confirmation dialog: "Reset all filters?"

---

## Interactions

- **Select Game**: Single or multi-select
- **Select Time Range**: Show/hide date pickers
- **Select Dates**: Open date picker dialogs
- **Select Stat Type**: Single or multi-select
- **Toggle Scope**: Check/uncheck player/table stats
- **Toggle Comparison**: Enable comparison modes
- **Select Visualization**: Choose chart/table/both
- **Select Stat Set**: Single or multi-select
- **Tap Apply Filters**: Navigate to visualization
- **Tap Reset**: Reset all filters
- **Tap Save**: Save filter preset

---

## Accessibility

- **Screen Reader**: "Advanced filters. Game selector. Time range selector. [Selected options]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all selectors

---

## Navigation

- **Back Button**: → Stats Dashboard
- **Apply Filters Button**: → Stat Visualization Screen
- **Reset Button**: Reset filters (stays on screen)
- **Save Button**: Save filter preset (stays on screen)

---

**Wireframe Description Complete**
