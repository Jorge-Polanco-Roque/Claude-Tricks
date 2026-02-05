# Modern Page Builder - Skill

Create modern, beautiful web pages with excellent UX following industry best practices.

## Usage

```
/modern-page <page-type> [options]
```

## Invocation Examples

- `/modern-page landing-page --product="SaaS App" --style="minimalist"`
- `/modern-page hero-section --theme="dark" --cta="Get Started"`
- `/modern-page pricing --tiers=3 --style="elegant"`
- `/modern-page about --company="Tech Startup"`

## Instructions for Claude

When this skill is invoked, follow this comprehensive process:

### 1. DISCOVERY & ANALYSIS (Required First Step)

Ask the user clarifying questions using AskUserQuestion:

**Page Purpose & Goals:**
- What is the primary goal of this page? (conversion, information, engagement)
- Who is the target audience?
- What action should users take? (CTA goal)
- What emotion/feeling should the page evoke?

**Content & Branding:**
- What is the main message/value proposition?
- Any specific brand colors or style guide?
- Tone of voice? (professional, playful, elegant, tech-savvy)
- Any existing content or copy to include?

**Technical Requirements:**
- Framework preference? (Next.js, React, Vue, etc.)
- Any specific components needed? (forms, modals, galleries)
- Mobile-first or desktop-first priority?
- Performance requirements?

### 2. UX PRINCIPLES TO APPLY

Automatically implement these UX best practices:

**Visual Hierarchy:**
- Clear heading structure (h1 > h2 > h3)
- Strategic use of size, weight, and color
- Whitespace for breathing room
- F-pattern or Z-pattern layout where appropriate

**Progressive Disclosure:**
- Show most important information first
- Use sections to organize content logically
- Reveal details progressively as user scrolls
- Avoid information overload

**Trust & Credibility:**
- Trust indicators (testimonials, stats, badges)
- Social proof elements
- Clear value propositions
- Professional imagery and icons

**Call-to-Action Design:**
- Primary CTA stands out (size, color, position)
- Secondary CTAs clearly differentiated
- Action-oriented language ("Get Started", not "Submit")
- Strategic placement (above fold + end of sections)

**Responsive Design:**
- Mobile-first approach
- Touch-friendly targets (44px minimum)
- Readable typography on all devices
- Optimized images for different screen sizes

**Performance:**
- Lazy loading for images
- Code splitting
- Optimized assets
- Fast initial load time

### 3. DESIGN SYSTEM TO USE

Apply this modern design system:

**Typography:**
```css
/* Headings - Use elegant serif or modern sans */
--font-heading: 'Playfair Display', 'Inter', serif;
--font-body: 'Inter', -apple-system, sans-serif;

/* Scale (Major Third - 1.25) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.25rem;    /* 20px */
--text-xl: 1.5rem;     /* 24px */
--text-2xl: 1.875rem;  /* 30px */
--text-3xl: 2.25rem;   /* 36px */
--text-4xl: 3rem;      /* 48px */
--text-5xl: 4rem;      /* 64px */
```

**Spacing (8px base):**
```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-24: 6rem;    /* 96px */
```

**Colors:**
```css
/* Primary - Adapt to user's brand */
--primary-50: #light;
--primary-500: #main;
--primary-700: #dark;

/* Neutrals */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-500: #6B7280;
--gray-900: #111827;

/* Semantic */
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
--info: #3B82F6;
```

**Shadows:**
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

**Animations:**
```css
/* Durations */
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;

/* Easings */
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0.0, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### 4. COMPONENT PATTERNS TO USE

**Hero Section:**
```jsx
<section className="relative h-screen flex items-center">
  {/* Background with overlay */}
  <div className="absolute inset-0">
    <Image src="..." fill className="object-cover" />
    <div className="absolute inset-0 bg-gradient-to-br from-black/60 to-black/30" />
  </div>

  {/* Content */}
  <div className="relative z-10 container mx-auto px-4">
    {/* Badge/Tag */}
    <div className="inline-flex items-center gap-2 bg-primary/20 backdrop-blur-sm
                    border border-primary/30 rounded-full px-4 py-2 mb-6">
      <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
      <span>New Feature</span>
    </div>

    {/* Heading */}
    <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fade-in">
      Compelling Headline
    </h1>

    {/* Subheading */}
    <p className="text-xl md:text-2xl mb-8 opacity-90">
      Clear value proposition
    </p>

    {/* CTAs */}
    <div className="flex flex-col sm:flex-row gap-4">
      <button className="btn-primary">Primary Action</button>
      <button className="btn-secondary">Secondary Action</button>
    </div>

    {/* Trust Indicators */}
    <div className="flex gap-6 mt-8 text-sm opacity-75">
      <span>✓ Trust Signal 1</span>
      <span>✓ Trust Signal 2</span>
      <span>✓ Trust Signal 3</span>
    </div>
  </div>
</section>
```

**Feature Section:**
```jsx
<section className="py-20 bg-gradient-to-br from-gray-50 to-white">
  <div className="container mx-auto px-4">
    {/* Section Header */}
    <div className="text-center mb-16 max-w-3xl mx-auto">
      <span className="text-primary font-semibold mb-2 block">Features</span>
      <h2 className="text-4xl md:text-5xl font-bold mb-4">
        Why Choose Us
      </h2>
      <p className="text-lg text-gray-600">
        Compelling description of benefits
      </p>
    </div>

    {/* Feature Grid */}
    <div className="grid md:grid-cols-3 gap-8">
      {features.map((feature) => (
        <div key={feature.id}
             className="bg-white rounded-lg p-6 shadow-md hover:shadow-xl
                        transition-all hover:-translate-y-1">
          {/* Icon */}
          <div className="w-12 h-12 bg-primary/10 rounded-full
                          flex items-center justify-center mb-4">
            <Icon className="w-6 h-6 text-primary" />
          </div>

          {/* Content */}
          <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
          <p className="text-gray-600">{feature.description}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

**CTA Section:**
```jsx
<section className="py-20 bg-gradient-to-br from-primary to-primary-dark text-white">
  <div className="container mx-auto px-4 text-center max-w-4xl">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">
      Ready to Get Started?
    </h2>
    <p className="text-xl mb-8 opacity-90">
      Clear, compelling call to action message
    </p>
    <button className="bg-white text-primary px-8 py-4 rounded-lg
                       font-semibold hover:scale-105 transition-transform
                       shadow-xl">
      Start Your Journey
    </button>
    <p className="mt-4 text-sm opacity-75">
      No credit card required • Free 14-day trial
    </p>
  </div>
</section>
```

### 5. ANIMATIONS TO INCLUDE

**Fade In on Scroll:**
```jsx
// Using Framer Motion
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.6 }}
>
  {/* Content */}
</motion.div>
```

**Hover Effects:**
```css
.card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}
```

**Button Interactions:**
```css
.btn {
  transition: all 0.2s ease;
}

.btn:hover {
  transform: scale(1.05);
}

.btn:active {
  transform: scale(0.98);
}
```

### 6. ACCESSIBILITY CHECKLIST

Ensure these are implemented:

- [ ] Semantic HTML (header, nav, main, section, footer)
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation support (tab order, focus states)
- [ ] Alt text on all images
- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Focus indicators visible
- [ ] Skip to main content link
- [ ] Responsive text sizes (no fixed px for body text)

### 7. PERFORMANCE OPTIMIZATION

Automatically implement:

```jsx
// Image Optimization
<Image
  src="..."
  alt="..."
  width={1200}
  height={800}
  priority={isAboveFold}
  loading={isAboveFold ? "eager" : "lazy"}
  quality={85}
  placeholder="blur"
/>

// Code Splitting
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
  ssr: false
});

// Font Optimization
<link
  rel="preconnect"
  href="https://fonts.googleapis.com"
/>
```

### 8. MOBILE-FIRST BREAKPOINTS

Use this responsive strategy:

```css
/* Mobile First (default) */
.element { /* mobile styles */ }

/* Tablet */
@media (min-width: 768px) {
  .element { /* tablet styles */ }
}

/* Desktop */
@media (min-width: 1024px) {
  .element { /* desktop styles */ }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .element { /* large desktop styles */ }
}
```

### 9. PAGE TYPES & TEMPLATES

**Landing Page:**
- Hero with clear value prop
- Features/Benefits section
- Social proof (testimonials, logos)
- CTA section
- FAQ (optional)
- Footer

**Product Page:**
- Hero with product showcase
- Key features with visuals
- Pricing comparison
- Use cases
- Integration/Tech specs
- CTA
- Footer

**About Page:**
- Company story hero
- Mission/Vision
- Team section
- Timeline/Milestones
- Values
- CTA (Join us / Contact)
- Footer

**Pricing Page:**
- Hero with pricing intro
- Pricing tiers comparison
- FAQ
- Feature comparison table
- CTA (Try free / Contact sales)
- Trust indicators
- Footer

### 10. IMPLEMENTATION WORKFLOW

Follow this exact sequence:

1. **Create component structure** (folders, files)
2. **Implement design system** (colors, typography, spacing)
3. **Build sections** (from top to bottom)
4. **Add animations** (entrance, hover, transitions)
5. **Implement responsive** (mobile → tablet → desktop)
6. **Add interactivity** (forms, modals, navigation)
7. **Optimize performance** (images, code splitting, lazy loading)
8. **Test accessibility** (keyboard nav, screen reader, contrast)
9. **Add meta tags** (SEO, Open Graph, Twitter Card)
10. **Final polish** (micro-interactions, loading states, error states)

### 11. CODE QUALITY STANDARDS

Ensure:

- TypeScript strict mode enabled
- No unused variables or imports
- Consistent naming (camelCase for variables, PascalCase for components)
- Comments for complex logic
- Reusable components extracted
- Props interfaces well-defined
- Error boundaries implemented
- Loading states for async operations

### 12. DOCUMENTATION TO CREATE

After implementation, create:

```markdown
## [Page Name] - Documentation

### Overview
Brief description of the page purpose and key features.

### Components Used
- List of all components
- Props and configurations

### Design Tokens
- Colors used
- Typography scale
- Spacing system

### Interactions
- Hover states
- Click behaviors
- Animations

### Responsive Behavior
- Mobile layout
- Tablet adjustments
- Desktop experience

### Performance Metrics
- Lighthouse scores
- Load time targets
- Optimization techniques

### Accessibility Features
- ARIA implementation
- Keyboard navigation
- Screen reader support

### Future Improvements
- Potential enhancements
- A/B testing ideas
- Feature additions
```

## Examples of Excellence

When creating pages, reference these principles:

**Apple.com** - Minimal, elegant, focus on product
**Stripe.com** - Clear, technical, excellent animations
**Linear.app** - Modern, fast, beautiful interactions
**Vercel.com** - Performance-focused, clean design
**Airbnb.com** - User-friendly, trustworthy, visual-heavy

## Success Criteria

A page is considered "modern with excellent UX" when:

✅ Lighthouse score: 90+ (Performance, Accessibility, Best Practices, SEO)
✅ First Contentful Paint < 1.5s
✅ Largest Contentful Paint < 2.5s
✅ Cumulative Layout Shift < 0.1
✅ WCAG 2.1 AA compliant
✅ Works perfectly on mobile, tablet, desktop
✅ Smooth animations (60fps)
✅ Clear user journey (goal → action → conversion)
✅ Professional, polished appearance
✅ Fast, responsive interactions

## Final Notes

- Always prioritize UX over visual complexity
- Less is more - avoid clutter
- Every element should have a purpose
- Test on real devices
- Get user feedback early
- Iterate based on metrics and feedback

When implementing, explain your UX decisions and why they improve the user experience.
