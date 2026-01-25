# Publisher Analytics Dashboard Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Analytics Dashboard      [⚙️] [📤]   │
├─────────────────────────────────────────┤
│                                         │
│  Overview                               │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Active   │           │
│  │ Games    │  │ Players  │           │
│  │   12     │  │   1,234  │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Avg      │           │
│  │ Sessions │  │ Rating   │           │
│  │   5,678  │  │   4.5⭐   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  [Time Range: Last 30 Days ▼]          │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      [Chart: Sessions Over Time] │  │
│  │      Line Chart                   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Top Games                              │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    2,345 sessions • 4.8⭐       │  │
│  │    [View Analytics]              │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    1,890 sessions • 4.6⭐       │  │
│  │    [View Analytics]              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Player Engagement                      │
│  ┌─────────────────────────────────┐  │
│  │      [Chart: Player Growth]      │  │
│  │      Bar Chart                    │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Analytics Dashboard" (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Export icon (24dp)

### Overview Section
- **Title**: "Overview" (18sp Roboto Medium)
- **Position**: 16dp below app bar

### Overview Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Total Games, Active Players, Total Sessions, Average Rating

### Time Range Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 40dp
- **Label**: "Time Range"
- **Options**: "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "All Time", "Custom Range"
- **Position**: 16dp below overview cards
- **Default**: "Last 30 Days"

### Sessions Over Time Chart
- **Type**: Chart Container
- **Height**: 250dp
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: Line chart showing session count over time
- **Position**: 16dp below time range selector
- **Interactive**: Zoom, pan, tooltips

### Top Games Section
- **Title**: "Top Games" (18sp Roboto Medium)
- **Position**: 24dp below chart

### Top Game Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Session count and rating (14sp Roboto Regular, secondary color)
  - "View Analytics" button (Text button, 14sp Roboto Medium, primary color) on right
- **Spacing**: 8dp vertical between cards
- **Navigation**: → Game Analytics Screen

### Player Engagement Chart
- **Type**: Chart Container
- **Height**: 250dp
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: Bar chart showing player growth or engagement metrics
- **Position**: 24dp below top games section

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Overview**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Chart Spacing**: 16dp from adjacent sections

---

## States & Interactions

### Default State
- Overview stats displayed
- Charts rendered
- Top games listed
- All interactive elements enabled

### Time Range Changed State
- Charts update to reflect selected time range
- Overview stats recalculate
- Loading indicator during update

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Charts show loading placeholder
- Buttons disabled

### Empty State (No Games)
- Illustration/icon (120dp)
- Title: "No games yet" (20sp Roboto Medium)
- Description: "Create your first game to see analytics" (16sp Roboto Regular)
- Action Button: "Create Game" (Primary button)

---

## Interactions

- **Select Time Range**: Update all charts and stats
- **Tap Top Game Card**: Navigate to Game Analytics
- **Tap View Analytics**: Navigate to Game Analytics
- **Tap Chart Area**: Show tooltip with data point details
- **Pinch/Zoom**: Zoom in/out on charts
- **Pan**: Move around charts
- **Tap Export**: Export analytics data

---

## Chart Types

### Sessions Over Time
- **Type**: Line Chart
- **X-axis**: Date/Time
- **Y-axis**: Session Count
- **Multiple Series**: Optional (by game, by stat set)

### Player Engagement
- **Type**: Bar Chart or Line Chart
- **X-axis**: Date/Time or Category
- **Y-axis**: Player Count or Engagement Metric
- **Metrics**: New players, active players, returning players

---

## Accessibility

- **Screen Reader**: "Analytics dashboard. Overview: [values]. [Chart description]. Top games: [list]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Chart Accessibility**: Alt text for charts, data table alternative

---

## Navigation

- **Back Button**: → Profile or Settings
- **Top Game Card**: → Game Analytics Screen
- **View Analytics Button**: → Game Analytics Screen
- **Settings Icon**: → Analytics Settings (if applicable)
- **Export Icon**: → Export Analytics Data

---

**Wireframe Description Complete**
