# Accessibility Checklist

> Accessibility reference. Pulled in by /review and frontend work.

## Keyboard navigation
- [ ] All interactive elements reachable via Tab.
- [ ] Logical tab order (matches visual order).
- [ ] No keyboard traps (can Tab out of every component).
- [ ] Skip-to-content link present.
- [ ] Focus visible on all interactive elements.
- [ ] Focus management on route changes and modals.

## Screen readers
- [ ] Semantic HTML used (`nav`, `main`, `article`, `section`, `aside`).
- [ ] ARIA roles where semantic HTML is insufficient.
- [ ] All images have `alt` text (or `alt=""` for decorative).
- [ ] Form inputs have associated `<label>` elements.
- [ ] Error messages associated with inputs (`aria-describedby`).
- [ ] Page has `<h1>` and logical heading hierarchy (h1 -> h2 -> h3).
- [ ] Dynamic content changes announced (`aria-live`).

## Contrast and color
- [ ] Text contrast ratio >= 4.5:1 (normal text).
- [ ] Large text contrast ratio >= 3:1 (18pt+ or 14pt bold).
- [ ] Non-text contrast >= 3:1 (UI components, borders).
- [ ] Color is not the sole indicator of information (add text/icons).
- [ ] Focus indicator has >= 3:1 contrast.

## Forms
- [ ] All inputs have labels.
- [ ] Required fields marked (`aria-required` or HTML5 `required`).
- [ ] Error messages are descriptive and actionable.
- [ ] Error messages associated with the field (`aria-describedby`).
- [ ] Submission errors announced (`role="alert"`).
- [ ] Autocomplete attributes set where appropriate.

## Motion and timing
- [ ] `prefers-reduced-motion` respected.
- [ ] No content flashing more than 3 times per second.
- [ ] Auto-updating content can be paused/stopped.
- [ ] Time limits can be extended or disabled.

## Mobile and touch
- [ ] Touch targets >= 44x44px.
- [ ] No pinch-to-zoom disabled (`user-scalable=yes`).
- [ ] Responsive layout works at 320px width.

## Testing tools
```bash
# Automated scanning
npx @axe-core/cli <url>           # axe-core CLI
npx pa11y <url>                   # Pa11y CLI
npx lighthouse <url> --only-categories=accessibility

# Browser DevTools
# Chrome: Lighthouse tab, Accessibility panel
# Firefox: Accessibility tab (devtools)

# Screen readers
# macOS: VoiceOver (Cmd+F5)
# Windows: NVDA (free), JAWS
# iOS: VoiceOver (Settings > Accessibility)
```

## Common issues
- **Missing alt text**: `<img src="logo.png">` without alt.
- **Div button**: `<div onclick="...">` instead of `<button>`.
- **No label**: `<input type="text">` without associated `<label>`.
- **Color-only errors**: Red border with no text explanation.
- **Heading skip**: h1 -> h4 (skipping h2, h3).
- **Inaccessible modal**: Focus not trapped, no Escape to close.
- **No skip link**: User must Tab through the entire nav every page.

## Red Flags
- `onclick` on non-interactive elements (div, span).
- Missing `alt` on images.
- No `<label>` on form inputs.
- Heading levels skipped.
- Focus indicator removed (`outline: none` with no replacement).
- `user-scalable=no` in viewport meta.
- Flashing content without pause control.
