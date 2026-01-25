# Session Details (From Following Feed) Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Session Details                      │
├─────────────────────────────────────────┤
│                                         │
│  🎲 Settlers of Catan                   │
│  @alice_gamer                           │
│  [Public Profile]                       │
│                                         │
│  Date: January 15, 2024                │
│  Duration: 2 hours 15 minutes           │
│  Round: 10                              │
│                                         │
│  Final Results                          │
│  ┌─────────────────────────────────┐  │
│  │ 🥇 Alice - Winner               │  │
│  │    Points: 10                   │  │
│  │    Resources: 12                │  │
│  │    Cities: 2                    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🥈 Bob                           │  │
│  │    Points: 8                    │  │
│  │    Resources: 15                │  │
│  │    Cities: 1                    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  All Stats                              │
│  [Round-by-round breakdown]            │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View Designer Profile         │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible)
- **Title**: "Session Details" (20sp Roboto Medium)
- **Back Button**: 24dp

### Game Header
- **Game Name**: 24sp Roboto Medium
- **Designer Handle**: 16sp Roboto Medium, primary color (tappable)
- **Privacy Badge**: "Public Profile" badge (if applicable)
- **Position**: 16dp below app bar

### Session Info
- **Date**: "Date: [formatted date]" (16sp Roboto Regular)
- **Duration**: "Duration: [time]" (16sp Roboto Regular, secondary color)
- **Round**: "Round: [number]" (16sp Roboto Regular, secondary color)
- **Position**: 16dp below header
- **Spacing**: 8dp between info items

### Final Results Section
- **Title**: "Final Results" (18sp Roboto Medium)
- **Position**: 24dp below session info

### Player Result Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Medal icon (🥇🥈🥉) or rank (24dp)
  - Player name (16sp Roboto Medium)
  - Winner badge (if applicable)
  - Final stat values (14sp Roboto Regular)
- **Spacing**: 8dp vertical between cards

### All Stats Section
- **Title**: "All Stats" (18sp Roboto Medium)
- **Position**: 24dp below results
- **Content**: Round-by-round breakdown or stat timeline
- **Format**: Expandable sections or timeline view

### View Designer Profile Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "View Designer Profile" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 24dp below all stats, 16dp from bottom
- **Navigation**: → View Profile Screen (Other User)

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Header**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between result cards
- **Button Spacing**: 24dp from last section, 16dp from bottom

---

## States & Interactions

### Default State
- Session details displayed
- Final results shown
- All stats available
- View Profile button enabled

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Button disabled

### Private Session State
- Message: "This session is private" (if user doesn't have access)
- Limited information shown
- View Profile button still available

---

## Interactions

- **Tap Designer Handle**: Navigate to Designer Profile
- **Tap View Designer Profile**: Navigate to Designer Profile
- **Tap Player Card**: Show player's detailed stats (optional)
- **Expand Stats Section**: Show round-by-round breakdown

---

## Accessibility

- **Screen Reader**: "Session details. [Game name]. [Designer]. Final results. [Player name], [score]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all buttons

---

## Navigation

- **Back Button**: → Following Feed
- **Designer Handle**: → View Profile Screen (Other User)
- **View Designer Profile Button**: → View Profile Screen (Other User)

---

## Note

This is a **read-only** view. No export options or editing capabilities (only available for own stats).

---

**Wireframe Description Complete**
