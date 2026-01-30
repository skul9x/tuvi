# Design Specifications: AI Tu Vi (Light/Traditional)

## 🎨 Color Palette (Warm/Paper)
| Name | Hex | Usage |
|------|-----|-------|
| **Background** | `#fdfbf7` | App background (Cream/Paper) |
| **Panel BG** | `#faebd7` | Input Panel Background (AntiqueWhite) or Lighter `#fff8f0` |
| **Surface** | `#ffffff` | Cards/Cells background (White) |
| **Primary** | `#f59e0b` | Main Buttons (Orange/Amber) |
| **Text Primary** | `#333333` | Main content text |
| **Text Red** | `#d32f2f` | Bad stars / Elements (Hỏa) |
| **Text Green** | `#2e7d32` | Good stars / Elements (Mộc) |
| **Text Blue** | `#1976d2` | Elements (Thủy) |
| **Text Yellow** | `#fbc02d` | Elements (Thổ/Kim - Darker for readability) |
| **Border** | `#e0e0e0` | Dividers |

## 🖼️ Layout Structure (Traditional Grid)
### Right Panel: Lá Số View
Uses a **4x4 Grid Layout** to mimic the traditional square chart.

| Tỵ | Ngọ | Mùi | Thân |
|----|-----|-----|------|
| Thìn| **Center** | **Center** | Dậu |
| Mão | **Center** | **Center** | Tuất |
| Dần | Sửu | Tý | Hợi |

- **Center (2x2 merged):** Displays User Info (Name, Date, Year, An Quang/Thai Tue info).
- **12 Cells:** Each cell displays:
    - **Header:** Cung Name (e.g., Mệnh/Phụ Mẫu) + Dia Chi (Tý/Sửu).
    - **Body:** List of Stars (Chinh Tinh in Bold/Uppper, Phu Tinh smaller).
    - **Footer:** Truong Sinh, Vong Thai Tue (if applicable).

### Left Panel: Input Form
- Background: Light Beige/Gradient.
- Style: Clean, rounded "Pill" inputs (border-radius: 20px).
- Button: Large, Orange, Rounded, Shadowed.

## 📝 Typography
- **Font:** `Roboto` or `Segoe UI`.
- **Cung Header:** Bold, Uppercase, 11-12px.
- **Star Text:** 10px or 11px. Main stars Bold.

## 🔲 Qt Stylesheet Logic
- Use `QFrame` for cells with `background-color: white; border: 1px solid #ddd;`.
- Input fields: `border: 1px solid #ccc; border-radius: 15px; padding: 5px 10px;`.
