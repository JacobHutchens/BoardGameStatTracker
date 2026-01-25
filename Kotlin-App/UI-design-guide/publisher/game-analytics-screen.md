# Game Analytics Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Catan Analytics        [⚙️] [📤] [📊] │
├─────────────────────────────────────────┤
│                                         │
│  🎲 Settlers of Catan                   │
│                                         │
│  Overview                               │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Active   │           │
│  │ Sessions │  │ Players  │           │
│  │   2,345  │  │   456    │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Avg      │  │ Rating   │           │
│  │ Rating   │  │ Trend    │           │
│  │   4.8⭐  │  │   ↑ 0.2  │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  [Time Range: Last 30 Days ▼]          │
│                                         │
│  [Chart/Table Toggle]                   │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      [Chart: Sessions Over Time] │  │
│  │      Line Chart                   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Player Statistics                      │
│  ┌─────────────────────────────────┐  │
│  │      [Chart: Player Distribution]│  │
│  │      Pie Chart                    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Stat Set Performance                   │
│  ┌─────────────────────────────────┐  │
│  │ Standard Set                      │  │
│  │   1,234 sessions (52.6%)         │  │
│  │   [View Details]                  │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Custom Set                       │  │
│  │   890 sessions (38.0%)          │  │
│  │   [View Details]                 │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Export Analytics               │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible)
- **Title**: "[Game Name] Analytics" (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Share icon (24dp), Format selector icon (24dp)

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
- **Cards**: Total Sessions, Active Players, Average Rating, Rating Trend

### Time Range Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 40dp
- **Label**: "Time Range"
- **Options**: "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "All Time", "Custom Range"
- **Position**: 16dp below overview cards
- **Default**: "Last 30 Days"

### Chart/Table Toggle
- **Type**: Segmented Control
- **Height**: 40dp
- **Options**: "Chart" and "Table"
- **Selected**: Primary color background, white text
- **Unselected**: Outlined, primary color text
- **Position**: 16dp below time range selector
- **Default**: Chart view

### Sessions Over Time Chart
- **Type**: Chart Container
- **Height**: 300dp (minimum, expands)
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: Line chart showing session count over time
- **Position**: 16dp below toggle
- **Interactive**: Zoom, pan, tooltips

### Player Statistics Section
- **Title**: "Player Statistics" (18sp Roboto Medium)
- **Position**: 24dp below sessions chart

### Player Distribution Chart
- **Type**: Chart Container
- **Height**: 250dp
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: Pie chart or bar chart showing player distribution
- **Position**: 16dp below section title

### Stat Set Performance Section
- **Title**: "Stat Set Performance" (18sp Roboto Medium)
- **Position**: 24dp below player statistics

### Stat Set Performance Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat set name (16sp Roboto Medium)
  - Session count and percentage (14sp Roboto Regular, secondary color)
  - "View Details" button (Text button, 14sp Roboto Medium, primary color) on right
- **Spacing**: 8dp vertical between cards

### Export Analytics Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Export Analytics" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Download icon (18dp) on left
- **Position**: 24dp below stat set performance, 16dp from bottom
- **Navigation**: → Export Analytics Data

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Header**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Chart Spacing**: 16dp from adjacent sections

---

## States & Interactions

### Default State
- Game info displayed
- Overview stats shown
- Charts rendered
- Stat set performance listed
- All buttons enabled

### Table View State
- Data table displayed
- Charts hidden
- Same data in table format

### Time Range Changed State
- Charts update to reflect selected time range
- Overview stats recalculate
- Loading indicator during update

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Charts show loading placeholder
- Buttons disabled

---

## Interactions

- **Select Time Range**: Update all charts and stats
- **Toggle Chart/Table**: Switch between views
- **Tap Chart Area**: Show tooltip with data point details
- **Pinch/Zoom**: Zoom in/out on charts
- **Pan**: Move around charts
- **Tap Stat Set Card**: Show detailed stat set analytics
- **Tap View Details**: Show stat set analytics
- **Tap Export**: Export analytics data

---

## Chart Types

### Sessions Over Time
- **Type**: Line Chart
- **X-axis**: Date/Time
- **Y-axis**: Session Count
- **Multiple Series**: Optional (by stat set, by player count)

### Player Distribution
- **Type**: Pie Chart or Bar Chart
- **Content**: Distribution of players by various metrics
- **Metrics**: New vs returning, player count distribution, geographic distribution (if available)

---

## Accessibility

- **Screen Reader**: "Game analytics. [Game name]. Overview: [values]. [Chart description]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Chart Accessibility**: Alt text for charts, data table alternative

---

## Navigation

- **Back Button**: → Publisher Analytics Dashboard or Designer Portfolio
- **Stat Set Card**: → Stat Set Analytics (detailed view)
- **View Details Button**: → Stat Set Analytics
- **Export Button**: → Export Analytics Data
- **Settings Icon**: → Game Analytics Settings (if applicable)
- **Share Icon**: → Share Analytics

---

**Wireframe Description Complete**
