# Registration Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Create Account                      │
├─────────────────────────────────────────┤
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Username                     │    │
│    │ ──────────────────────────── │    │
│    │ ✓ Available                 │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Email                        │    │
│    │ ──────────────────────────── │    │
│    │ ✓ Valid format               │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Password              [👁]    │    │
│    │ ──────────────────────────── │    │
│    │ ●●●●●●●●                    │    │
│    │ Medium strength              │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Confirm Password     [👁]    │    │
│    │ ──────────────────────────── │    │
│    │ ●●●●●●●●                    │    │
│    │ ✓ Passwords match           │    │
│    └─────────────────────────────┘    │
│                                         │
│    ☐ I agree to Terms of Service       │
│                                         │
│    ┌─────────────────────────────┐    │
│    │      CREATE ACCOUNT         │    │
│    └─────────────────────────────┘    │
│                                         │
│    Already have an account?             │
│    [Login]                             │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Username Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Username"
- **Text**: 16sp Roboto Regular
- **Validation**: Real-time duplicate check
- **Helper Text**: "✓ Available" (green) or "✗ Username taken" (red)
- **States**: Default, Focused, Filled, Error, Valid

### Email Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Email"
- **Text**: 16sp Roboto Regular
- **Validation**: Real-time format validation
- **Helper Text**: "✓ Valid format" or "✗ Invalid email"
- **States**: Default, Focused, Filled, Error, Valid

### Password Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Password"
- **Text**: 16sp Roboto Regular (masked)
- **Show/Hide Toggle**: Eye icon (24dp) on right
- **Password Strength Indicator**: Below field
  - Weak: Red bar (0-33%)
  - Medium: Orange bar (34-66%)
  - Strong: Green bar (67-100%)
- **Helper Text**: Strength indicator text
- **States**: Default, Focused, Filled, Error

### Confirm Password Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Confirm Password"
- **Text**: 16sp Roboto Regular (masked)
- **Show/Hide Toggle**: Eye icon (24dp) on right
- **Validation**: Real-time match check
- **Helper Text**: "✓ Passwords match" or "✗ Passwords don't match"
- **States**: Default, Focused, Filled, Error, Valid

### Terms of Service Checkbox
- **Size**: 20dp x 20dp
- **Label**: "I agree to Terms of Service" (16sp Roboto Regular)
- **Link**: "Terms of Service" (underlined, primary color)
- **Position**: Below confirm password
- **Spacing**: 16dp from confirm password
- **Required**: Must be checked to submit

### Create Account Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "CREATE ACCOUNT" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below checkbox
- **States**: Default, Pressed, Disabled (if validation fails), Loading

### Login Link
- **Type**: Text Button
- **Text**: "Login" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: Below create account button
- **Spacing**: 16dp from button
- **Context**: "Already have an account?" (14sp Roboto Regular, secondary color)

---

## Spacing & Layout

- **Screen Margins**: 16dp on all sides
- **Input Field Spacing**: 16dp vertical between fields
- **Section Spacing**: 24dp between major sections
- **Button Spacing**: 16dp from adjacent elements
- **Content Centering**: Vertically centered on screen

---

## States & Interactions

### Default State
- Empty input fields
- Create Account button disabled
- Terms checkbox unchecked
- No error messages

### Focused State
- Input field shows focused border (primary color, 2dp)
- Label animates to top position
- Keyboard appears
- Real-time validation begins

### Validation States
- **Username**: Shows "✓ Available" or "✗ Username taken" as user types
- **Email**: Shows "✓ Valid format" or "✗ Invalid email" as user types
- **Password**: Shows strength indicator as user types
- **Confirm Password**: Shows "✓ Passwords match" or "✗ Passwords don't match"

### Error State
- Red border on input field (1dp)
- Error icon (24dp) on right side of input
- Error message below input (12sp Roboto Regular, red)
- Create Account button disabled
- Examples:
  - "Username must be 3-20 characters"
  - "Email already registered"
  - "Password must be at least 8 characters"

### Loading State
- Create Account button shows loading spinner
- Button text changes to "Creating Account..."
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to Home screen or Onboarding

---

## Accessibility

- **Screen Reader**: "Registration screen. Username input. Email input. Password input."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: Text meets WCAG AA (4.5:1 minimum)
- **Focus Indicators**: Clear focus rings on all inputs
- **Error Announcements**: Screen reader announces errors

---

## Navigation

- **Back Button**: → Login Screen
- **Create Account Button**: → Home (on success) or → Onboarding (first-time)
- **Login Link**: → Login Screen
- **Terms of Service Link**: → Terms of Service screen (modal or web)

---

**Wireframe Description Complete**
