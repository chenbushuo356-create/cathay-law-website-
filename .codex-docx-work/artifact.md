# Cathay Praxis letterhead formatting contract

- Reference: `/Users/mima0000/Desktop/CP律所/信纸/CP信纸模版V7.docx`
- SHA-256: `031c5582fb24f6863f625fff42826a340ec12ab8c11e51fd8746aaea78f91600`
- Reference geometry: US Letter portrait; left/right margins 0.75 in; bottom margin 0.80 in; Cathay Praxis Law floating logo plus address block and horizontal rule in `word/header1.xml`.
- Reference pages/sections: one page and one section. The header is the recurring letterhead component and must remain on every page.
- Editable scope: replace the source reports' existing header/footer with the reference letterhead; keep every body paragraph, table, list, bilingual string, and body order unchanged; set body text to black 仿宋 4 号 (14 pt); bold body title/heading paragraphs and table heading rows.
- Explicit adaptation: body top margin is set to 1.35 in so the report title clears the reference letterhead's horizontal rule. This is a necessary non-text layout adjustment.
- Preserve-only: all source-body content and table geometry; template header image, its relationship, and the template's letterhead text. Source footer content is intentionally removed.
- QA gates: source/final body-text hashes must match; all final body runs must use 14 pt black 仿宋 settings; final package must have the template header and no footer reference; render all final pages and inspect the rendered output.
