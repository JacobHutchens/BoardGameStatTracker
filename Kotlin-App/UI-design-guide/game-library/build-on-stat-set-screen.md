# Build On Stat Set Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Build On Stat Set    [Save] [❌]     │
├─────────────────────────────────────────┤
│                                         │
│  Based On: Standard Set                 │
│  (This will create a new stat set)      │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ New Stat Set Name            │    │
│    │ ──────────────────────────── │    │
│    │ My Custom Set                │    │
│    └─────────────────────────────┘    │
│                                         │
│  Stats (from Standard Set)              │
│  ┌─────────────────────────────────┐  │
│  │ Points                           │  │
│  │ Description: Player's score      │  │
│  │ Type: Integer  Scope: Player    │  │
│  │                          [✕]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Resources                        │  │
│  │ Description: Resource count      │  │
│  │ Type: Integer  Scope: Player    │  │
│  │                          [✕]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      + Add Stat                  │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Preview                     │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Build On Stat Set" (20sp Roboto Medium)
- **Actions**: Save button (14sp Roboto Medium, primary color), Close button (24dp)

### Source Stat Set Display
- **Type**: Info banner
- **Background**: Secondary color at 10% opacity
- **Border**: 1dp solid secondary color
- **Corner Radius**: 8dp
- **Padding**: 12dp
- **Content**:
  - Label: "Based On:" (14sp Roboto Regular, secondary color)
  - Source stat set name (16sp Roboto Medium)
  - Note: "(This will create a new stat set)" (12sp Roboto Regular, secondary color)
- **Position**: 16dp below app bar
- **Read-only**: Cannot be edited

### New Stat Set Name Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "New Stat Set Name"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Enter new stat set name"
- **Validation**: Required, min 1 character, max 45 characters, must be different from source
- **Position**: 16dp below source display
- **Helper Text**: "Must be different from source set name"

### Stats Section
- **Title**: "Stats (from [Source Set Name])" (18sp Roboto Medium)
- **Position**: 24dp below name input
- **Note**: Shows stats are from source set

### Stat Item Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat name (16sp Roboto Medium) - **Editable**
  - Description (14sp Roboto Regular, secondary color) - **Editable**
  - Type and Scope (14sp Roboto Regular, secondary color) - **Editable**
  - Remove button (X icon, 24dp) on right
- **Spacing**: 8dp vertical between cards
- **Note**: All stats from source are pre-populated and can be modified

### Add Stat Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "+ Add Stat" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Plus icon (18dp) on left
- **Position**: 16dp below stats list
- **Navigation**: → Add Stat Modal/Dialog

### Preview Button
- **Type**: Text Button
- **Height**: 40dp
- **Text**: "Preview" (14sp Roboto Medium, primary color)
- **Position**: 16dp below add stat button
- **Navigation**: → Stat Set Preview (modal)

### Save Button (App Bar)
- **Type**: Text Button
- **Text**: "Save" (14sp Roboto Medium, primary color)
- **Position**: App bar, right side
- **State**: Disabled until name entered (different from source) and at least one stat remains

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Source Display**: 16dp below app bar
- **Input Spacing**: 16dp vertical between inputs
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between stat cards

---

## States & Interactions

### Default State
- Source stat set displayed (read-only)
- New stat set name empty
- All source stats pre-populated and editable
- Save button disabled

### Name Entered State
- New name entered (different from source)
- Save button enabled (if name valid and stats present)

### Stat Modified State
- Stats can be edited, added, or removed
- Changes tracked
- Preview shows updated stat set

### Validation States
- **Name Required**: "New stat set name is required"
- **Name Same as Source**: "New name must be different from source set"
- **Name Too Long**: "Stat set name must be 45 characters or less"
- **At Least One Stat**: "Add at least one stat to the set"

### Loading State
- Save button shows loading spinner
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Message: "New stat set 'X' created based on 'Y'"
- Navigate to Stat Set Details (new set) or Game Details

---

## Interactions

- **Edit Stat Name**: Tap stat name to edit inline
- **Edit Stat Description**: Tap description to edit inline
- **Edit Stat Type/Scope**: Tap to open selector
- **Tap Remove (X)**: Remove stat from list
- **Tap Add Stat**: Open Add Stat modal
- **Tap Preview**: Show stat set preview
- **Tap Save**: Create new stat set, navigate back
- **Back Button**: Cancel creation, return to previous screen

---

## Tooltip/Help

**On Long-press Source Display or Info Icon**:
- **Title**: "Building On Existing Stat Set"
- **Content**: "This will create a new stat set with a new name based on 'Standard Set'. The original 'Standard Set' will not be modified. Stat sets are immutable to preserve data integrity for filtering."

---

## Accessibility

- **Screen Reader**: "Build on stat set. Based on: [source name]. New stat set name input. Stats: [list]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all inputs

---

## Navigation

- **Back Button**: → Previous screen (Game Details or Create Session)
- **Save Button**: → Stat Set Details (new set) or Game Details
- **Close Button (X)**: → Cancel creation, return to previous screen
- **Add Stat Button**: → Add Stat Modal
- **Preview Button**: → Stat Set Preview (modal)

---

**Wireframe Description Complete**
