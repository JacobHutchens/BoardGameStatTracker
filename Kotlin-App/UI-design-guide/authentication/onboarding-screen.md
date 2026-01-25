# Onboarding/Tutorial Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│                            [Skip]       │
├─────────────────────────────────────────┤
│                                         │
│         [Illustration/Icon]              │
│                                         │
│    Track Your Games                     │
│                                         │
│    Record stats during live game        │
│    sessions and view your progress     │
│    over time.                           │
│                                         │
│    ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│    │  ●  │ │  ○  │ │  ○  │ │  ○  │   │
│    └─────┘ └─────┘ └─────┘ └─────┘   │
│                                         │
│    [Previous]        [Next]             │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Skip Button
- **Type**: Text Button
- **Text**: "Skip" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: Top-right, 16dp from edges
- **Size**: 48dp x 48dp touch target

### Illustration/Icon
- **Size**: 120dp x 120dp
- **Position**: Centered, 24dp below skip button
- **Content**: Feature-specific illustration or icon

### Title
- **Text**: Feature title (24sp Roboto Medium)
- **Position**: 24dp below illustration
- **Alignment**: Centered
- **Examples**: "Track Your Games", "Live Sessions", "View Stats", "Follow Friends"

### Description
- **Text**: Feature description (16sp Roboto Regular, secondary color)
- **Position**: 16dp below title
- **Alignment**: Centered
- **Max Width**: 280dp
- **Line Height**: 24dp
- **Lines**: 2-3 lines

### Progress Indicators
- **Type**: Dots or step indicators
- **Count**: 4 dots (for 4-step onboarding)
- **Active Dot**: Filled circle (8dp diameter, primary color)
- **Inactive Dots**: Outlined circle (8dp diameter, secondary color)
- **Spacing**: 8dp between dots
- **Position**: 24dp below description
- **Alignment**: Centered

### Navigation Buttons
- **Previous Button**: 
  - Type: Text Button
  - Text: "Previous" (14sp Roboto Medium)
  - Position: Bottom-left, 16dp from edges
  - Visibility: Hidden on first step
- **Next Button**:
  - Type: Primary Action Button
  - Text: "Next" (14sp Roboto Medium, white)
  - Position: Bottom-right, 16dp from edges
  - Width: 120dp
  - On Last Step: Text changes to "Get Started"

---

## Onboarding Steps

### Step 1: Track Your Games
- **Illustration**: Game board or stat tracking icon
- **Title**: "Track Your Games"
- **Description**: "Record stats during live game sessions and view your progress over time."

### Step 2: Live Sessions
- **Illustration**: Multiple users or session icon
- **Title**: "Live Sessions"
- **Description**: "Create or join sessions to track stats in real-time with other players."

### Step 3: View Stats
- **Illustration**: Chart or analytics icon
- **Title**: "View Stats"
- **Description**: "Analyze your performance with flexible filtering and visualizations."

### Step 4: Follow Friends
- **Illustration**: Social or follow icon
- **Title**: "Follow Friends"
- **Description**: "Follow other players and see their public stats and game sessions."

---

## Spacing & Layout

- **Screen Margins**: 16dp on all sides
- **Skip Button**: 16dp from top-right
- **Illustration**: 24dp from skip button
- **Title**: 24dp from illustration
- **Description**: 16dp from title
- **Progress Dots**: 24dp from description
- **Navigation Buttons**: 24dp from progress dots, 16dp from bottom

---

## States & Interactions

### Default State
- Current step content displayed
- Progress indicators show current step
- Next button enabled
- Previous button visible (except first step)

### First Step State
- Previous button hidden
- Skip button visible
- Next button enabled

### Last Step State
- Next button text: "Get Started"
- Skip button visible
- Previous button visible

### Swipe Interaction
- **Swipe Left**: Next step
- **Swipe Right**: Previous step
- **Animation**: Slide transition (300ms)

---

## Accessibility

- **Screen Reader**: "Onboarding step [X] of 4. [Title]. [Description]."
- **Touch Targets**: All buttons minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Swipe Alternative**: Buttons provide alternative to swipe gestures

---

## Navigation

- **Skip Button**: → Home Dashboard (skips all steps)
- **Next Button**: → Next step, or → Home Dashboard (on last step)
- **Previous Button**: → Previous step
- **Swipe Left**: → Next step
- **Swipe Right**: → Previous step

---

**Wireframe Description Complete**
