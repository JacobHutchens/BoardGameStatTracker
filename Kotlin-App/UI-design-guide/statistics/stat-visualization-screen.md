# Stat Visualization Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Win Rate Over Time    [⚙️] [📤] [📊] │
├─────────────────────────────────────────┤
│                                         │
│  [Chart/Table Toggle]                   │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │                                 │  │
│  │      [Chart Visualization]     │  │
│  │                                 │  │
│  │      Line/Bar/Pie Chart        │  │
│  │                                 │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Filters Applied                        │
│  [Game: Catan] [Time: Last 6 months]   │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Adjust Filters               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Export Chart                 │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Export to JSON               │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: Filter description (e.g., "Win Rate Over Time") (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Share icon (24dp), Format selector icon (24dp)

### Chart/Table Toggle
- **Type**: Segmented Control
- **Height**: 40dp
- **Options**: "Chart" and "Table"
- **Selected**: Primary color background, white text
- **Unselected**: Outlined, primary color text
- **Position**: 16dp below app bar
- **Default**: Chart view

### Chart Visualization Area
- **Type**: Chart Container
- **Height**: 300dp (minimum, expands)
- **Width**: Full width minus 32dp margins
- **Background**: Surface color
- **Padding**: 16dp
- **Content**: 
  - Line chart (for time series)
  - Bar chart (for comparisons)
  - Pie chart (for distributions)
  - Scatter plot (for correlations)
- **Position**: 16dp below toggle
- **Interactive**: Zoom, pan, tooltips

### Data Table View
- **Type**: Data Table
- **Height**: 400dp (scrollable)
- **Width**: Full width minus 32dp margins
- **Content**: 
  - Headers: Stat name, Value, Date, Game, etc.
  - Rows: Data values
- **Visibility**: Shown when Table toggle selected
- **Position**: 16dp below toggle

### Filters Applied Section
- **Title**: "Filters Applied" (14sp Roboto Regular, secondary color)
- **Position**: 16dp below chart/table
- **Content**: Filter chips showing active filters
- **Chips**: 
  - Game name
  - Time range
  - Stat type
  - Scope
  - Comparison mode
- **Layout**: Horizontal scrollable row
- **Spacing**: 8dp between chips

### Adjust Filters Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Adjust Filters" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below filters applied
- **Navigation**: → Advanced Stats Filter Screen

### Export Chart Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Export Chart" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Download icon (18dp) on left
- **Position**: 8dp below adjust filters
- **Navigation**: → Export format selector (PNG/JPG)

### Export to JSON Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Export to JSON" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Download icon (18dp) on left
- **Position**: 8dp below export chart
- **Navigation**: → Export Stats Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Toggle**: 16dp below app bar
- **Chart/Table**: 16dp below toggle
- **Section Spacing**: 16dp vertical between sections
- **Button Spacing**: 8dp vertical between buttons

---

## States & Interactions

### Default State (Chart View)
- Chart displayed
- Filters applied shown
- All buttons enabled

### Table View State
- Data table displayed
- Chart hidden
- Export chart button disabled (or changes to "Export Table")

### Loading State
- Skeleton chart/table
- Shimmer animation
- Buttons disabled

### Empty State (No Data)
- Illustration/icon (120dp)
- Title: "No data matches your filters" (20sp Roboto Medium)
- Description: "Try adjusting your filters" (16sp Roboto Regular)
- Action Button: "Adjust Filters" (Primary button)

---

## Chart Types

### Line Chart
- **Use**: Time series data, trends over time
- **X-axis**: Time (date)
- **Y-axis**: Stat value
- **Multiple series**: Different games/players

### Bar Chart
- **Use**: Comparisons between categories
- **X-axis**: Category (game, player, etc.)
- **Y-axis**: Stat value
- **Grouped**: Multiple stats side by side

### Pie Chart
- **Use**: Distributions, proportions
- **Slices**: Categories (games, players)
- **Values**: Percentages or counts

### Scatter Plot
- **Use**: Correlations, relationships
- **X-axis**: One stat
- **Y-axis**: Another stat
- **Points**: Individual sessions

---

## Interactions

- **Toggle Chart/Table**: Switch between views
- **Tap Chart Area**: Show tooltip with data point details
- **Pinch/Zoom**: Zoom in/out on chart
- **Pan**: Move around chart
- **Tap Filter Chip**: Remove filter or adjust
- **Tap Adjust Filters**: Navigate to Advanced Filters
- **Tap Export Chart**: Open export format selector
- **Tap Export to JSON**: Navigate to Export Stats

---

## Export Format Selector (Modal)

### Layout
```
┌─────────────────────────────────────────┐
│            ═══                          │
│                                         │
│  Export Chart                           │
├─────────────────────────────────────────┤
│                                         │
│  Format                                 │
│  ☑ PNG                                 │
│  ☐ JPG                                 │
│                                         │
│  Quality                                │
│  ┌─────────────────────────────────┐  │
│  │ [────────────●──────────]       │  │
│  │ High                            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │  Cancel  │  │  Export  │            │
│  └──────────┘  └──────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

---

## Accessibility

- **Screen Reader**: "Stat visualization. Chart view. [Chart description]. Filters applied: [list]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Chart Accessibility**: Alt text for chart, data table alternative

---

## Navigation

- **Back Button**: → Stats Dashboard or Advanced Filters
- **Adjust Filters Button**: → Advanced Stats Filter Screen
- **Export Chart Button**: → Export format selector (modal)
- **Export to JSON Button**: → Export Stats Screen
- **Share Icon**: → Share dialog

---

**Wireframe Description Complete**
