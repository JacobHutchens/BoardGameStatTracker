# Stat Set Details Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Standard Set            [⚙️] [❌]   │
├─────────────────────────────────────────┤
│                                         │
│  Standard Set                           │
│                                         │
│  Stats                                  │
│  ┌─────────────────────────────────┐  │
│  │ Points                           │  │
│  │ Description: Player's score      │  │
│  │ Type: Integer                    │  │
│  │ Scope: Player                    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Resources                        │  │
│  │ Description: Resource count      │  │
│  │ Type: Integer                    │  │
│  │ Scope: Player                    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Cities                           │  │
│  │ Description: Number of cities    │  │
│  │ Type: Integer                    │  │
│  │ Scope: Player                    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Use This Stat Set             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Create New Based On...         │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [Delete] (if owner)                    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible)
- **Title**: Stat set name (20sp Roboto Medium)
- **Actions**: Settings icon (24dp) if owner, Close button (24dp)

### Stat Set Name
- **Text**: Stat set name (24sp Roboto Medium)
- **Position**: 16dp below app bar
- **Read-only**: Cannot be edited (immutable)

### Stats Section
- **Title**: "Stats" (18sp Roboto Medium)
- **Position**: 24dp below stat set name

### Stat Detail Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat name (16sp Roboto Medium)
  - Description (14sp Roboto Regular, secondary color)
  - Type: "Type: [Integer/String/Bool/Float]" (14sp Roboto Regular, secondary color)
  - Scope: "Scope: [Player/Table]" (14sp Roboto Regular, secondary color)
- **Spacing**: 8dp vertical between cards
- **Read-only**: Stats cannot be edited (immutable)

### Use This Stat Set Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Use This Stat Set" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below stats list
- **Navigation**: → Create Session Flow (with stat set pre-selected) or current session

### Build On Existing Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Create New Based On..." (14sp Roboto Medium, primary color)
- **Subtext**: "(Copy and modify existing)" (12sp Roboto Regular, secondary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below use button
- **Navigation**: → Build On Stat Set Screen

### Delete Button (If Owner)
- **Type**: Text Button
- **Height**: 40dp
- **Text**: "Delete" (14sp Roboto Medium, error color)
- **Position**: 16dp below build on button
- **Alignment**: Left-aligned
- **Confirmation**: Shows confirmation dialog before deletion
- **Visibility**: Only shown if user is owner of stat set

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Stat Set Name**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between stat cards
- **Button Spacing**: 8dp vertical between buttons

---

## States & Interactions

### Default State
- Stat set name displayed
- All stats listed
- Use and Build On buttons enabled
- Delete button visible (if owner)

### Empty State (No Stats)
- Message: "This stat set has no stats" (should not occur, but handled)
- Use button disabled

### Delete Confirmation State
- Confirmation dialog appears
- "Are you sure you want to delete this stat set? This action cannot be undone."
- Actions: "Cancel" or "Delete"

---

## Interactions

- **Tap Use This Stat Set**: Use for new session or current session
- **Tap Build On Existing**: Navigate to Build On Stat Set screen
- **Tap Delete**: Show confirmation dialog
- **Long-press Stat Card**: Show stat details (optional)
- **Back Button**: Return to previous screen

---

## Accessibility

- **Screen Reader**: "Stat set details. [Stat set name]. Stats: [list]. Use this stat set button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all buttons

---

## Navigation

- **Back Button**: → Previous screen (Game Details or Create Session)
- **Use This Stat Set Button**: → Create Session Flow or Live Session Room
- **Build On Existing Button**: → Build On Stat Set Screen
- **Delete Button**: → Confirmation dialog, then → Previous screen (if confirmed)

---

**Wireframe Description Complete**
