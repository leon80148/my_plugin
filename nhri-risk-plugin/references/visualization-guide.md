# Visualization Guide

This guide covers standard chart types, color coding, and embedding strategies for rendering NHRI risk assessment results in web dashboards and PDF reports.

## Risk Score Gauge Chart

A semicircular gauge showing the patient's risk percentage with color zones.

### SVG/HTML Implementation

The gauge uses three SVG arc segments colored by risk zone:

- Green arc (0% to <10%): Low risk
- Yellow arc (10% to <20%): Moderate risk
- Red arc (>=20%): High risk

A needle rotates based on the risk percentage. The angle formula is:

    angle = (risk / 100) * 180 - 90

Where risk 0% maps to -90 degrees (far left) and risk 100% maps to +90 degrees (far right).

Example SVG structure:

    <svg viewBox="0 0 200 120">
      <!-- Green arc -->
      <path d="M 20 100 A 80 80 0 0 1 100 20" stroke="#22c55e" stroke-width="12" fill="none"/>
      <!-- Yellow arc -->
      <path d="M 100 20 A 80 80 0 0 1 140 34" stroke="#eab308" stroke-width="12" fill="none"/>
      <!-- Red arc -->
      <path d="M 140 34 A 80 80 0 0 1 180 100" stroke="#ef4444" stroke-width="12" fill="none"/>
      <!-- Needle: rotate(ANGLE, 100, 100) -->
      <line x1="100" y1="100" x2="100" y2="30" stroke="#1e293b" stroke-width="2"/>
      <!-- Labels -->
      <text x="100" y="95" text-anchor="middle" font-size="18">RISK%</text>
    </svg>

## Risk Comparison Bar Chart

Side-by-side horizontal bars comparing the patient's risk against the population average for their age and gender.

### Chart.js Configuration

Use a horizontal bar chart (`indexAxis: 'y'`) with two bars:

- Patient bar: colored by risk level (#22c55e / #eab308 / #ef4444)
- Population average bar: neutral gray (#94a3b8)

Key options:
- `scales.x.min`: 0
- `scales.x.max`: 130% of the larger value
- Hide legend, show percentage in tooltip

### Multiple Models Comparison

When displaying all five models (CHD, Stroke, Hypertension, Diabetes, MACE) simultaneously, use grouped bars with:
- Patient data in blue (#3b82f6)
- Population average in gray (#94a3b8)

## Risk Trend Line Chart

For repeated assessments over time, display risk scores as a line chart to show trajectory.

### Chart.js Configuration

Use a line chart with:
- Patient risk scores as a filled line (blue #3b82f6, with light fill)
- Population average as a dashed gray line
- Horizontal annotation lines at 10% (yellow, moderate threshold) and 20% (red, high threshold)
- Use chartjs-plugin-annotation for threshold lines

## Color Coding Standards

All risk visualizations must use the following consistent color scheme:

| Risk Level | Type Value | Color Name | Hex Code | RGB |
|---|---|---|---|---|
| Low | 0 | Green | #22c55e | rgb(34, 197, 94) |
| Moderate | 1 | Yellow | #eab308 | rgb(234, 179, 8) |
| High | 2 | Red | #ef4444 | rgb(239, 68, 68) |

### Supporting Colors

| Purpose | Hex Code | Usage |
|---|---|---|
| Population average | #94a3b8 | Neutral comparison baseline |
| Patient primary | #3b82f6 | Default patient data color |
| Background | #f8fafc | Chart background |
| Text primary | #1e293b | Labels and titles |
| Text secondary | #64748b | Subtitles and annotations |

### CSS Utility Classes

    .risk-low      { color: #22c55e; }
    .risk-moderate { color: #eab308; }
    .risk-high     { color: #ef4444; }
    .risk-bg-low      { background-color: #dcfce7; }
    .risk-bg-moderate { background-color: #fef9c3; }
    .risk-bg-high     { background-color: #fee2e2; }

## Report Embedding

### Chart.js (Recommended for Simplicity)

Include Chart.js v4 via CDN. Render charts into canvas elements. Use chartjs-plugin-annotation for threshold lines.

CDN URLs:
- https://cdn.jsdelivr.net/npm/chart.js@4
- https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3

### D3.js (Recommended for Custom Visualizations)

D3 provides maximum flexibility for custom gauge and arc charts. Use `d3.arc()` with `innerRadius`/`outerRadius` to create gauge arcs. Map risk percentage to arc `endAngle` using the formula:

    endAngle = (risk / 100) * Math.PI - Math.PI / 2

Color the foreground arc based on risk thresholds.

### ECharts (Recommended for Dashboard Integration)

ECharts provides built-in gauge chart types with minimal configuration. Use the `gauge` series type with custom `axisLine.lineStyle.color` breakpoints:

    color: [[0.2, '#22c55e'], [0.4, '#eab308'], [1, '#ef4444']]

This maps 0-20% of the gauge to green, 20-40% to yellow, and 40-100% to red. Adjust breakpoints based on the actual risk scale of each model.

## PDF Report Generation

Use headless browser automation to convert the HTML report into a PDF.

### Puppeteer (Node.js)

1. Launch headless Chromium with `puppeteer.launch()`
2. Navigate to the HTML report file
3. Wait for `networkidle0` plus additional timeout for chart rendering
4. Call `page.pdf()` with A4 format, margins (20mm top/bottom, 15mm left/right), and `printBackground: true`

### Playwright (Python)

1. Launch Chromium with `sync_playwright().chromium.launch()`
2. Navigate to the HTML report file
3. Wait for `networkidle` load state plus additional timeout
4. Call `page.pdf()` with the same A4 format and margin settings

### Integration with Report Module

Generate the HTML report first, then convert:

    python scripts/run_module.py --module report -- --input result.json --format html --output report.html

Then use Puppeteer or Playwright to convert report.html to PDF.

## Accessibility

### Color-Blind Friendly Alternatives

The default green/yellow/red scheme may be difficult for users with red-green color blindness (deuteranopia/protanopia). Provide an alternative palette:

| Risk Level | Default | Color-Blind Safe | Pattern |
|---|---|---|---|
| Low | #22c55e (Green) | #0ea5e9 (Blue) | No pattern |
| Moderate | #eab308 (Yellow) | #f59e0b (Amber) | Diagonal stripes |
| High | #ef4444 (Red) | #e11d48 (Rose) | Cross-hatch |

Implementation tips:
- Always pair colors with text labels ("Low", "Moderate", "High")
- Use distinct patterns (solid, striped, cross-hatched) in addition to color
- Provide a toggle for color-blind mode in the dashboard UI
- Test with color blindness simulators (e.g., Chrome DevTools > Rendering > Emulate vision deficiencies)

### ARIA Labels

Ensure all chart elements are accessible to screen readers:

- Wrap each chart canvas in a div with `role="img"` and a descriptive `aria-label`
- Example: `aria-label="CHD 10-year risk: 15.3%, moderate risk level"`
- Use `role="status"` and `aria-live="polite"` for dynamic risk level badges
- Provide a hidden data table (`class="sr-only"`) as a fallback for screen readers

Screen-reader-only CSS:

    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border-width: 0;
    }
