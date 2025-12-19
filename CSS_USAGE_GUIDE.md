# Barlery CSS Usage Guide

## Quick Reference

### Color Scheme
Your site uses Barlery's actual brand colors from the signage:

- **Burgundy Red**: `--color-burgundy` (#8B1F2F) - Main brand color from signage
- **Warm Gold**: `--color-gold` (#E8B84A) - Logo text color
- **Brick/Brown**: `--color-brick` & `--color-primary` - Warm wood/brick tones
- **Dark Background**: `--color-dark` (#1a1a1a)
- **Light Background**: `--color-light` (#f5f5f0)

## Layout Patterns

### Full-Width Sections (Like Squarespace)
Sections extend edge-to-edge while content stays centered:

```html
<section class="section">
  <div class="container">
    <!-- Your content here -->
  </div>
</section>
```

### Section Background Colors

```html
<!-- Burgundy section (brand color from signage) -->
<section class="section section-burgundy section-textured">
  <div class="container">
    <!-- Content -->
  </div>
</section>

<!-- Dark section with texture -->
<section class="section-lg section-dark section-textured">
  <div class="container">
    <!-- Content -->
  </div>
</section>

<!-- Light section -->
<section class="section section-light">
  <!-- Content -->
</section>

<!-- Brown section (wood/brick tones) -->
<section class="section section-primary section-textured">
  <!-- Content -->
</section>
```

### Section Sizes
- `section` - Standard padding (96px top/bottom on desktop)
- `section-lg` - Large padding (128px top/bottom)
- `section-sm` - Small padding (64px top/bottom)

## Container Widths

```html
<!-- Standard width (1200px max) -->
<div class="container">...</div>

<!-- Narrow width (800px max) - good for text-heavy content -->
<div class="container-narrow">...</div>

<!-- Wide width (1400px max) -->
<div class="container-wide">...</div>
```

## Grid Layouts

```html
<!-- 3-column grid (responsive) -->
<div class="grid grid-3">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>

<!-- 2-column grid -->
<div class="grid grid-2">...</div>

<!-- 4-column grid -->
<div class="grid grid-4">...</div>
```

Grids automatically become single column on mobile.

## Buttons

```html
<!-- Primary button (brown) -->
<a href="#" class="btn btn-primary">Click Me</a>

<!-- Accent button (gold) -->
<a href="#" class="btn btn-accent">Click Me</a>

<!-- Secondary button (outline) -->
<a href="#" class="btn btn-secondary">Click Me</a>

<!-- Light button (for dark backgrounds) -->
<a href="#" class="btn btn-light">Click Me</a>

<!-- Button group (horizontal, centered) -->
<div class="btn-group">
  <a href="#" class="btn btn-primary">Button 1</a>
  <a href="#" class="btn btn-secondary">Button 2</a>
</div>
```

## Cards

```html
<div class="card">
  <div class="card-image">
    <img src="..." alt="...">
  </div>
  <div class="card-body">
    <h3 class="card-title">Card Title</h3>
    <p class="card-text">Card description goes here.</p>
    <div class="card-footer">
      <span>Left content</span>
      <a href="#" class="btn btn-primary">Action</a>
    </div>
  </div>
</div>
```

## Typography

Headers automatically use Georgia (serif) for that classic feel:
```html
<h1>Main Heading</h1>  <!-- 3rem / 48px -->
<h2>Section Heading</h2>  <!-- 2.5rem / 40px -->
<h3>Subsection</h3>  <!-- 2rem / 32px -->
```

## Utility Classes

### Spacing
```html
<!-- Margin top -->
<div class="mt-sm">Small margin top</div>
<div class="mt-md">Medium margin top</div>
<div class="mt-lg">Large margin top</div>

<!-- Margin bottom -->
<div class="mb-sm">Small margin bottom</div>
<div class="mb-md">Medium margin bottom</div>
<div class="mb-lg">Large margin bottom</div>
```

### Text Alignment
```html
<div class="text-center">Centered text</div>
<div class="text-left">Left aligned</div>
<div class="text-right">Right aligned</div>
```

## Hero Section

```html
<section class="hero section-textured">
  <div class="hero-content">
    <h1>Main Headline</h1>
    <p class="hero-tagline">Tagline in gold italic</p>
    <p>Supporting text</p>
    <div class="btn-group">
      <a href="#" class="btn btn-accent">Primary Action</a>
      <a href="#" class="btn btn-light">Secondary Action</a>
    </div>
  </div>
</section>
```

## Section Headers (Centered)

```html
<div class="section-header">
  <h2>Section Title</h2>
  <p class="section-subtitle">Optional subtitle or description</p>
</div>
```

Or use the reusable component:
```django
{% include "barlery/_section_header.html" with title="Section Title" subtitle="Optional subtitle" %}
```

## Forms

Forms are automatically styled. Just use semantic HTML:

```html
<form method="post">
  {% csrf_token %}
  
  <fieldset>
    <legend>Section Name</legend>
    
    <div>
      <label for="id_name">Name</label>
      {{ form.name }}
      {{ form.name.errors }}
    </div>
    
    <!-- More fields -->
  </fieldset>
  
  <button type="submit">Submit</button>
</form>
```

## Reusable Components

### Event Card
```django
{% include "barlery/_event_card.html" with event=event_object %}
```

### Menu Item
```django
{% include "barlery/_menu_item.html" with item=menu_item_object %}
```

### Section Header
```django
{% include "barlery/_section_header.html" with title="Title" subtitle="Subtitle" %}
```

## Common Patterns

### Feature Grid (Icons + Text)
```html
<div class="grid grid-3">
  <div class="card">
    <div class="card-body text-center">
      <div style="font-size: 4rem; margin-bottom: var(--space-sm);">🍺</div>
      <h3 class="card-title">Feature Title</h3>
      <p class="card-text">Feature description</p>
    </div>
  </div>
  <!-- Repeat for other features -->
</div>
```

### Call-to-Action Section
```html
<section class="section section-primary section-textured">
  <div class="container-narrow text-center">
    <h2>Compelling Headline</h2>
    <p style="font-size: 1.2rem; margin-bottom: var(--space-lg);">
      Supporting text
    </p>
    <a href="#" class="btn btn-accent">Take Action</a>
  </div>
</section>
```

### Two-Column Content
```html
<div class="grid grid-2">
  <div>
    <h2>Left Column</h2>
    <p>Content</p>
  </div>
  <div>
    <h2>Right Column</h2>
    <p>Content</p>
  </div>
</div>
```

## Tips

1. **Texture overlay**: Add `section-textured` class to any section for subtle texture
2. **Consistent spacing**: Use the spacing utilities (mt-*, mb-*) instead of custom margins
3. **Mobile-first**: All grids and layouts are responsive by default
4. **Hover effects**: Cards and buttons have built-in hover animations
5. **Color customization**: Change CSS variables in `:root` to adjust the entire color scheme

## Need More?

The CSS is heavily commented and organized into sections. Look for these sections in `site.css`:
- CSS Variables
- Typography
- Layout
- Components (Buttons, Cards, Forms)
- Utilities
- Responsive Design