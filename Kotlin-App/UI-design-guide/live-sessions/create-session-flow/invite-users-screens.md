# Create Session - Invite App Users Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Invite Users      Step 3 of 7  [❌] │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search users...               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Selected Users                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Alice              [✕]       │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Search Results                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Bob                          │  │
│  │    @bob_gamer                   │  │
│  │    [Add]                        │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Charlie                      │  │
│  │    @charlie_player              │  │
│  │    [Add]                        │  │
│  └─────────────────────────────────┘  │
│                                         │
│              [Continue]                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Progress Indicator
- **Type**: Multi-step progress indicator
- **Height**: 48dp
- **Content**: "Step 3 of 7" (14sp Roboto Medium)
- **Visual**: Progress bar with step indicators
- **Position**: Top of screen, below app bar

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search users..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Position**: 16dp below progress indicator

### Selected Users Section
- **Title**: "Selected Users" (16sp Roboto Medium)
- **Position**: 16dp below search bar
- **Visibility**: Only shown if users selected

### Selected User Chip
- **Type**: Action Chip
- **Height**: 32dp
- **Content**:
  - Avatar (24dp) on left
  - Username (14sp Roboto Medium)
  - Remove button (X icon, 18dp) on right
- **Spacing**: 8dp horizontal between chips
- **Layout**: Horizontal scrollable row

### Search Results Section
- **Title**: "Search Results" (16sp Roboto Medium)
- **Position**: 24dp below selected users section
- **Visibility**: Shown when search has results

### User Result Item
- **Type**: List Item (Two-Line)
- **Height**: 72dp
- **Padding**: 16dp horizontal
- **Content**:
  - Avatar (40dp) on left
  - Username (16sp Roboto Medium)
  - Handle/email (14sp Roboto Regular, secondary color)
  - Add button (Text button, 14sp Roboto Medium) on right
- **Spacing**: 8dp vertical between items
- **States**: Default, Pressed

### Continue Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Continue" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: Bottom of screen, 16dp padding
- **State**: Enabled (users optional, can skip)

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Progress Indicator**: 16dp from app bar
- **Search Bar**: 16dp from progress indicator
- **Section Spacing**: 24dp vertical between sections
- **List Item Spacing**: 8dp vertical
- **Continue Button**: 16dp from last item, 16dp from bottom

---

## States & Interactions

### Default State
- Search bar empty
- No users selected
- No search results
- Continue button enabled

### Search State
- Search results displayed as user types
- Results update in real-time
- Clear button visible when text entered

### Selected State
- User appears in Selected Users section
- Add button changes to "Added" or checkmark
- User removed from search results (or marked as added)

### Empty Search Results
- Message: "No users found" (16sp Roboto Regular, secondary color)
- Suggestion: "Try a different search term"

### Loading State
- Skeleton user items (2-3 placeholders)
- Shimmer animation
- Search disabled

---

## Interactions

- **Type in Search**: Filter users in real-time
- **Tap Add Button**: Add user to selected list
- **Tap Remove (X)**: Remove user from selected list
- **Tap User Item**: Show user profile (optional)
- **Tap Continue**: Proceed to next step (Add Non-App Players)
- **Back Button**: Return to previous step (Select Game)

---

## Accessibility

- **Screen Reader**: "Invite users, step 3 of 7. Search users. [User name], [handle]. Add button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on search and list items

---

## Navigation

- **Back Button**: → Step 2 (Select Game)
- **Continue Button**: → Step 4 (Add Non-App Players)
- **Close Button (X)**: → Cancel creation, return to Live Sessions
- **User Profile**: → View Profile Screen (if tapped)

---

**Wireframe Description Complete**
