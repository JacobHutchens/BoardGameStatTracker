# Login Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│                                         │
│         [App Logo/Name]                 │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Email or Username            │    │
│    │ ──────────────────────────── │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Password              [👁]    │    │
│    │ ──────────────────────────── │    │
│    └─────────────────────────────┘    │
│                                         │
│    ☐ Remember me                       │
│                                         │
│    [Forgot Password?]                  │
│                                         │
│    ┌─────────────────────────────┐    │
│    │      LOGIN                  │    │
│    └─────────────────────────────┘    │
│                                         │
│    Don't have an account?               │
│    [Register]                          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Email/Username Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Label**: Floating label "Email or Username"
- **Text Size**: 16sp Roboto Regular
- **Placeholder**: "Enter your email or username"
- **States**: Default, Focused, Filled, Error

### Password Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Label**: Floating label "Password"
- **Text Size**: 16sp Roboto Regular
- **Show/Hide Toggle**: Eye icon (24dp) on right
- **States**: Default, Focused, Filled, Error

### Remember Me Checkbox
- **Size**: 20dp x 20dp
- **Label**: "Remember me" (16sp Roboto Regular)
- **Position**: Below password field
- **Spacing**: 8dp from password field

### Forgot Password Link
- **Type**: Text Button
- **Text**: "Forgot Password?" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: Below checkbox
- **Spacing**: 16dp from checkbox

### Login Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "LOGIN" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: Centered, 24dp below forgot password link
- **States**: Default, Pressed, Disabled, Loading

### Register Link
- **Type**: Text Button
- **Text**: "Register" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: Below login button
- **Spacing**: 16dp from login button
- **Context**: "Don't have an account?" (14sp Roboto Regular, secondary color)

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
- Login button enabled
- No error messages

### Focused State
- Input field shows focused border (primary color, 2dp)
- Label animates to top position
- Keyboard appears

### Error State
- Red border on input field (1dp)
- Error icon (24dp) on right side of input
- Error message below input (12sp Roboto Regular, red)
- Example: "Invalid email format" or "User not found"

### Loading State
- Login button shows loading spinner
- Button text changes to "Logging in..."
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to Home screen

---

## Accessibility

- **Screen Reader**: "Login screen. Email or username input. Password input."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: Text meets WCAG AA (4.5:1 minimum)
- **Focus Indicators**: Clear focus rings on all inputs

---

## Navigation

- **On Success**: → Home Dashboard
- **Register Button**: → Registration Screen
- **Forgot Password**: → Forgot Password Screen
- **Back Button**: Not applicable (entry screen)

---

**Wireframe Description Complete**
