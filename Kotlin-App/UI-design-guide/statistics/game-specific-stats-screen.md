# Game-Specific Stats Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Catan Stats            [⚙️] [📤]    │
├─────────────────────────────────────────┤
│                                         │
│  🎲 Settlers of Catan                   │
│                                         │
│  Overview                               │
│  ┌──────────┐  ┌──────────┐           │
│  │ Played   │  │ Win Rate │           │
│  │   15     │  │   60%    │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Avg      │  │ Best     │           │
│  │ Score    │  │ Score    │           │
│  │   8.5    │  │   12     │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  [Chart/Table Toggle]                   │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      [Chart Visualization]      │  │
│  │      Win Rate Over Time         │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Advanced Filters               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Recent Sessions                        │
│  ┌─────────────────────────────────┐  │
│  │ Won • Jan 15, 2024              │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Lost • Jan 12, 2024             │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible)
- **Title**: "[Game Name] Stats" (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Share icon (24dp)

### Game Header
- **Game Name**: 24sp Roboto Medium
- **Icon**: Game icon/emoji (32dp) on left
- **Position**: 16dp below app bar

### Overview Section
- **Title**: "Overview" (18sp Roboto Medium)
- **Position**: 24dp below header

### Overview Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Played (count), Win Rate (percentage), Avg Score, Best Score

### Chart/Table Toggle
- **Type**: Segmented Control
- **Height**: 40dp
- **Options**: "Chart" and "Table"
- **Selected**: Primary color background, white text
- **Unselected**: Outlined, primary color text
- **Position**: 16dp below overview

### Chart Visualization Area
- **Type**: Chart Container
- **Height**: 300dp (minimum, expands)
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: Game-specific stat visualization
- **Position**: 16dp below toggle

### Advanced Filters Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Advanced Filters" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below chart
- **Navigation**: → Advanced Stats Filter Screen (pre-filtered for this game)

### Recent Sessions Section
- **Title**: "Recent Sessions" (18sp Roboto Medium)
- **Position**: 24dp below filters button

### Recent Session Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Result badge (Won/Lost) (12sp Roboto Medium, badge style)
  - Date (16sp Roboto Medium)
- **Spacing**: 8dp vertical between items
- **Navigation**: → Session Details

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Header**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Button Spacing**: 16dp from adjacent elements

---

## States & Interactions

### Default State
- Game info displayed
- Overview stats shown
- Chart displayed
- Recent sessions listed
- All buttons enabled

### Table View State
- Data table displayed
- Chart hidden
- Same data in table format

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Buttons disabled

### Empty State (No Sessions)
- Message: "No sessions for this game yet" (20sp Roboto Medium)
- Description: "Play this game to see your stats" (16sp Roboto Regular)
- Action Button: "Create Session" (Primary button)

---

## Interactions

- **Toggle Chart/Table**: Switch between views
- **Tap Overview Card**: Show detailed stat view
- **Tap Advanced Filters**: Navigate to Advanced Filters (pre-filtered)
- **Tap Recent Session**: Navigate to Session Details
- **Tap Chart Area**: Show tooltip with data point details

---

## Accessibility

- **Screen Reader**: "Game stats. [Game name]. Overview: [values]. Chart view."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all buttons

---

## Navigation

- **Back Button**: → Stats Dashboard or Game Details
- **Advanced Filters Button**: → Advanced Stats Filter Screen (game pre-selected)
- **Recent Session**: → Session Details
- **Share Icon**: → Share dialog

---

**Wireframe Description Complete**
