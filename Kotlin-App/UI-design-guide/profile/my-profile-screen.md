# My Profile Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  My Profile              [⚙️] [☰]      │
├─────────────────────────────────────────┤
│                                         │
│         [Avatar]                        │
│         [Edit]                          │
│                                         │
│    @username                            │
│    email@example.com                    │
│                                         │
│  Quick Stats                            │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Win Rate │           │
│  │ Games    │  │          │           │
│  │   42     │  │   65%    │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Sessions │  │ Favorite │           │
│  │ This Week│  │ Game     │           │
│  │    5     │  │  Catan   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View My Stats                 │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View Session History          │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Recent Activity                        │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Catan • Won • 2d ago        │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket • Lost • 5d ago     │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 152dp (expanded), 64dp (collapsed)
- **Title**: "My Profile" (24sp expanded, 20sp collapsed)
- **Actions**: Settings icon (24dp), Drawer menu icon (24dp)

### Avatar
- **Size**: 80dp x 80dp
- **Position**: Centered, 24dp below app bar
- **Border**: 2dp solid (primary color or divider)
- **Edit Button**: Small edit icon (20dp) bottom-right of avatar
- **Tap Avatar**: Navigate to Edit Profile

### Username
- **Text**: "@username" (20sp Roboto Medium)
- **Position**: 16dp below avatar
- **Alignment**: Centered

### Email
- **Text**: "email@example.com" (16sp Roboto Regular, secondary color)
- **Position**: 8dp below username
- **Alignment**: Centered

### Quick Stats Section
- **Title**: "Quick Stats" (18sp Roboto Medium)
- **Position**: 24dp below email

### Quick Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Total Games, Win Rate, Sessions This Week, Favorite Game

### View My Stats Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "View My Stats" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below quick stats

### View Session History Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "View Session History" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below view stats button

### Recent Activity Section
- **Title**: "Recent Activity" (18sp Roboto Medium)
- **Position**: 24dp below session history button

### Recent Activity Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Game icon/emoji (24dp) on left
  - Game name and result (16sp Roboto Medium)
  - Date (14sp Roboto Regular, secondary color, right-aligned)
- **Spacing**: 8dp vertical between items
- **Navigation**: → Session Details

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Avatar**: 24dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Button Spacing**: 8dp vertical between buttons

---

## States & Interactions

### Default State
- Profile information displayed
- Quick stats shown
- Recent activity listed
- All buttons enabled

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Buttons disabled

### Empty State (No Recent Activity)
- Recent Activity section shows "No recent activity"
- "View Session History" button prominent

---

## Interactions

- **Tap Avatar**: Navigate to Edit Profile
- **Tap Edit Button**: Navigate to Edit Profile
- **Tap Quick Stats Card**: Navigate to detailed stat view
- **Tap View My Stats**: Navigate to Stats Dashboard
- **Tap View Session History**: Navigate to Session History
- **Tap Recent Activity Item**: Navigate to Session Details
- **Tap Settings Icon**: Open Settings
- **Tap Drawer Menu**: Open Navigation Drawer

---

## Accessibility

- **Screen Reader**: "My profile. [Username]. [Email]. Quick stats: [values]. View my stats button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all buttons and cards

---

## Navigation

- **Edit Profile**: → Edit Profile Screen
- **View My Stats**: → Stats Dashboard
- **View Session History**: → Session History Screen
- **Recent Activity Item**: → Session Details
- **Settings Icon**: → Settings Main Screen
- **Drawer Menu**: → Navigation Drawer

---

**Wireframe Description Complete**
