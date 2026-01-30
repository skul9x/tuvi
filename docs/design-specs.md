# Design Specifications: Mystical Luxury (Tu Vi Huyen Bi)

## 🎨 Creative Direction
- **Vibe**: "Cosmic Wisdom meets Digital Luxury". A balance between ancient mystery (astrology charts, stars) and modern digital product design (clean inputs, fast interactions).
- **Metaphor**: The screen is a portal to the stars.

## 🎨 Color Palette
| Role | Name | Tailwind Class | Hex Code | Usage |
|------|------|----------------|----------|-------|
| **Background** | `void` | `bg-slate-950` | `#020617` | Main app background (Deepest space) |
| **Surface** | `nebula` | `bg-slate-900/50` | `#0f172a` | Cards, Glassmorphism base |
| **Primary** | `gold` | `text-amber-400` | `#fbbf24` | Headings, Icons, Borders (Gradient start) |
| **Primary Alt** | `gold-light` | `text-amber-200` | `#fde68a` | Gradient end, subtle highlights |
| **Accent** | `mystic` | `bg-violet-600` | `#7c3aed` | Primary Actions (Buttons) |
| **Accent Glow**| `mystic-glow` | `shadow-violet-500/50` | -- | Button Shadows |
| **Text Main** | `starlight` | `text-slate-50` | `#f8fafc` | Primary Content |
| **Text Muted** | `star-dust` | `text-slate-400` | `#94a3b8` | Labels, Explanations |

## 📝 Typography
| Element | Font Family | Size (Desktop/Mobile) | Weight | Tracking |
|---------|-------------|-----------------------|--------|----------|
| **Headings** | `Cinzel` / `Playfair Display` | 4xl / 3xl | Bold | Wide (`tracking-wider`) |
| **Subheads** | `Cinzel Decorative` | 2xl / xl | Semibold | Normal |
| **Body** | `Inter` / `Outfit` | base / sm | Regular | Normal |
| **Data/Nums** | `JetBrains Mono` | sm / xs | Medium | Tight |

## 🌫️ Effects & Materials
- **Glassmorphism**: `bg-slate-900/40 backdrop-blur-xl border border-white/10`
- **Golden Border**: `border-amber-500/30`
- **Cosmic Gradient (Button)**: `bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500`
- **Text Gradient (Gold)**: `bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-amber-400 to-amber-200`

## 📱 Responsive Strategy (Mobile First)
- **Mobile**: Single column, fixed bottom action bar for "Xem Ngay", large touch targets (48px+).
- **Desktop**: Split layout (Left: Data Input, Right: Visualization/Explanation), expansive background art.

## ✨ Animations
- **Fade In**: `animate-fade-in-up` (for cards appearing)
- **Pulse**: `animate-pulse-slow` (for stars in background)
- **Shimmer**: `animate-shimmer` (on gold borders)

## 🖼️ Assets Needed
- Background: `stars-bg.png` (Seamless tile or CSS generated stars)
- Icons: `Lucide React` (Thin stroke) or `Heroicons`
