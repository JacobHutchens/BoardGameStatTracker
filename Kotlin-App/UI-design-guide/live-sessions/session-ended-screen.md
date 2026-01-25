# Session Ended Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Session Ended                        │
├─────────────────────────────────────────┤
│                                         │
│         [Trophy/Check Icon]            │
│                                         │
│    Session Ended                        │
│    Duration: 2 hours 15 minutes        │
│                                         │
│  Final Results                          │
│  ┌─────────────────────────────────┐  │
│  │ 🥇 Charlie - Winner             │  │
│  │    10 points                    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🥈 Alice                         │  │
│  │    8 points                      │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🥉 Bob                           │  │
│  │    6 points                      │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View Full Details             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Return to Sessions           │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Trophy/Check Icon
- **Size**: 80dp x 80dp
- **Icon**: Trophy or checkmark icon
- **Color**: Success color (green #4CAF50) or primary color
- **Position**: Centered, 24dp below app bar

### Title
- **Text**: "Session Ended" (24sp Roboto Medium)
- **Position**: 16dp below icon
- **Alignment**: Centered

### Duration Text
- **Text**: "Duration: X hours Y minutes" (16sp Roboto Regular, secondary color)
- **Position**: 8dp below title
- **Alignment**: Centered

### Final Results Section
- **Title**: "Final Results" (18sp Roboto Medium)
- **Position**: 24dp below duration
- **Alignment**: Left-aligned

### Player Result Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Medal icon (🥇🥈🥉) or rank number (24dp)
  - Player name (16sp Roboto Medium)
  - Winner badge (if applicable)
  - Final stat values (14sp Roboto Regular)
- **Spacing**: 8dp vertical between cards
- **Order**: Ranked by final score/result

### View Full Details Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "View Full Details" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below results, 16dp from bottom
- **Navigation**: → Session Details Screen

### Return to Sessions Button
- **Type**: Secondary Action Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Return to Sessions" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below view details button
- **Navigation**: → Live Sessions List

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Icon Spacing**: 24dp from app bar
- **Text Spacing**: 16dp between title and duration
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between result cards
- **Button Spacing**: 8dp vertical between buttons

---

## States & Interactions

### Default State
- Session results displayed
- Players ranked by final score
- Winner highlighted
- Both buttons enabled

### Loading State
- Skeleton result cards (3-4 placeholders)
- Shimmer animation
- Buttons disabled

### No Winner State
- No winner badge shown
- Players ranked by score
- Message: "No winner (cooperative game)" if applicable

---

## Interactions

- **Tap View Full Details**: Navigate to Session Details
- **Tap Return to Sessions**: Navigate to Live Sessions List
- **Tap Player Card**: Show player's detailed stats (optional)

---

## Accessibility

- **Screen Reader**: "Session ended. Duration: [time]. Final results. Winner: [name], [score]."
- **Touch Targets**: All cards and buttons minimum 48dp height
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all interactive elements

---

## Navigation

- **Back Button**: → Live Sessions List
- **View Full Details Button**: → Session Details Screen
- **Return to Sessions Button**: → Live Sessions List

---

**Wireframe Description Complete**
