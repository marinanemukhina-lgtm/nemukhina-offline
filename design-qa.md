# Design QA — 2026-11-10

final result: passed

## Evidence and normalization

- Source visual truth: `docs/images/design-reference.png`, 1487 × 1058 px.
- Implementation: `docs/images/assistant.jpg`, 1440 × 1024 px; CSS viewport 1440 × 1024, density 1. No browser frame.
- Same state: Russian, new conversation, empty input, no configured model. Source and live screenshot were opened together in one comparison input. Aspect ratios differ by less than 0.1%; compare the source at width 1440 (scale 0.9684, height approximately 1025) against the 1440 × 1024 capture.
- Earlier iteration evidence: `../redesign-review/reference-build-before.jpg`; final settled render: `../redesign-review/reference-build-after.jpg`, copied to the published screenshot path above. These working-review files remain outside the public repository.
- Additional live evidence: `docs/images/mobile.jpg` (390 × 844 viewport, RU); `docs/images/result.jpg` (1440 × 1024, a real saved two-turn conversation).
- The full-view images make the title, controls, illustration and margins readable at this resolution; a separate cropped comparison was unnecessary. Input, settings, sources, history and mobile controls were also inspected live at normal browser scale.

## Comparison history and findings

1. **P2, initial welcome hierarchy:** the two-line headline made the text block too short, while the right-hand footer overflowed the target viewport. Corrected the intended three-line Russian phrasing, increased the optical display scale and reduced the illustration section's minimum spacing. Re-captured the same empty state: entire 1440 × 1024 composition fits, including the model action and footer.
2. **P2, mobile navigation to results:** after changing the layout, the old scroll target pointed to the whole app instead of the result. Updated generation, history, answer selection and source-search transitions to the result element. Re-tested source search at 390 px: the quote, line reference and checksum are visible, with no horizontal overflow.
3. **Capture state:** an immediate screenshot caught the art's entrance fade. The final published image uses the settled capture, not that intermediate frame.

No remaining actionable P0/P1/P2 visual findings in the tested states.

## Required fidelity surfaces

- **Typography:** locally supplied Lora for display text, system sans for body and controls. Large title follows the source's three-line hierarchy. Model setup and footer text are deliberately smaller than the illustrative mock, within normal supporting UI scale. Chinese uses installed system glyph fallbacks; no downloadable CJK font dependency.
- **Layout:** 58.4% / 41.6% welcome split, consistent gutter, large input, compact suggestions. Working view uses a 380 px conversation column and a readable result region. At 390/320 px the composition becomes a single column; controls remain visible and input precedes decorative art.
- **Colors:** cream, charcoal and coral retained. The send icon is dark for contrast rather than the mock's white. Visible keyboard focus styles and standard native dialog behavior remain.
- **Images:** original generated 1024 × 1536 paper sculpture, used as an image asset, with no broken assets in the final checked state. The exact ribbon geometry differs from the concept because the artwork was reconstructed as a standalone asset; its material, subject, palette and placement remain consistent. Icons are supplied Tabler SVG files with MIT notice, not hand-drawn substitutes.
- **Copy:** broad user task promise preserved in RU/EN/ZH. No invented working model, stars, awards or testimonials. Real model requirements and limitations are present at the relevant action.

## Functional checks

- Real model answer without documents; follow-up preserved the synthetic project name; result copied successfully.
- Saved two-turn conversation reopened after page reload; existing earlier conversation survived the server restart.
- No-model submission opens settings and retains the typed question; closing the dialog returns focus to the triggering control.
- Exact source search without a model returns the matching line; original synthetic document opens in a dialog.
- RU/EN/ZH localization; 1440 px desktop and 390/320 px mobile widths. At 320 px EN and ZH: `scrollWidth = clientWidth = 320`.
- No console error/warn entries in the final observed app states. All images loaded.
- Markdown download contents were checked earlier in this implementation cycle; the export handler was preserved. Automated suite: 33 tests passed.

## Limits and follow-up

This is visual and functional review of the implemented surface, not an Awwwards score or proof of universal accessibility. Physical phones, screen readers, all browser engines, and reduced-motion preference switching were not manually tested. Reduced-motion CSS is present. The app requires separately prepared model files; model quality remains limited as documented in `docs/VALIDATION.md`.

P3: optional future platform installers, richer model selection and additional accessible CJK typography evaluation. These are not represented as implemented features.
