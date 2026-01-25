# Followers/Following List Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Followers            [Followers] [Following] │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search users...               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 @bob_player                   │  │
│  │    Bob Gamer                      │  │
│  │    [Follow] [Following]          │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 👤 @charlie_designer            │  │
│  │    Charlie Designer              │  │
│  │    [Follow] [Following]          │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Followers" or "Following" (20sp Roboto Medium)
- **Tabs**: "Followers" and "Following" tabs (if viewing own profile)
- **Back Button**: 24dp

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search users..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Position**: 16dp below app bar

### User List Item
- **Type**: List Item (Two-Line)
- **Height**: 72dp
- **Padding**: 16dp horizontal
- **Content**:
  - Avatar (40dp) on left
  - Username (16sp Roboto Medium)
  - Display name (14sp Roboto Regular, secondary color)
  - Follow/Following button (Text button, 14sp Roboto Medium) on right
- **Spacing**: 8dp vertical between items
- **States**: Default, Pressed

### Follow/Following Button
- **Type**: Text Button
- **Height**: 32dp
- **Text**: "Follow" or "Following" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: Right side of list item
- **States**: 
  - Follow: Primary color text
  - Following: Primary color text with checkmark icon

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Search Bar**: 16dp below app bar
- **List Item Spacing**: 8dp vertical between items
- **Content Padding**: 16dp from screen edges

---

## States & Interactions

### Default State
- Search bar empty
- User list displayed
- Follow/Following buttons visible

### Search State
- Search results filtered
- Clear button visible
- Results update as user types

### Empty State
- Illustration/icon (120dp)
- Title: "No followers yet" or "Not following anyone" (20sp Roboto Medium)
- Description: "Start following users to see them here" (16sp Roboto Regular)
- Action Button: "Find Users to Follow" (Primary button)

### Loading State
- Skeleton user items (3-4 placeholders)
- Shimmer animation
- Search disabled

---

## Interactions

- **Type in Search**: Filter users in real-time
- **Tap User Item**: Navigate to View Profile Screen
- **Tap Follow/Following**: Toggle follow status
- **Back Button**: Return to Profile Screen

---

## Accessibility

- **Screen Reader**: "Followers list. [User name], [display name]. Follow button."
- **Touch Targets**: All list items minimum 72dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on list items

---

## Navigation

- **Back Button**: → Profile Screen
- **User Item**: → View Profile Screen (Other User)
- **Follow/Following Button**: Toggle follow status (stays on screen)

---

**Wireframe Description Complete**
