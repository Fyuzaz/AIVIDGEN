import shutil

code = """
/* --- FLEXBOX GAP POLYFILL FOR OLDER BROWSER COMPATIBILITY --- */
.input-group > * + * { margin-left: 1rem; }
.logo > * + * { margin-left: 1rem; }
.editor-actions > * + * { margin-left: 1rem; }
.editor-options > * + * { margin-top: 1.2rem; }

/* For style-selector which wraps, we use negative margin hack */
.style-selector { margin: -0.25rem; }
.style-selector > * { margin: 0.25rem; }

.overlay-selector > * + * { margin-left: 0.75rem; }
.timeline-controls > * + * { margin-left: 0.75rem; }
.segment-info > * + * { margin-left: 0.75rem; }
.segment-actions > * + * { margin-left: 0.4rem; }
.apiKey-input > * + * { margin-left: 1rem; }
.chips-scroll > * + * { margin-left: 0.5rem; }
.video-card { display: flex; flex-direction: column; }
.video-info > * + * { margin-top: 0.3rem; }
.video-stats > * + * { margin-left: 0.5rem; }

/* Basic aspect ratio fallback */
@supports not (aspect-ratio: 9 / 16) {
    .video-preview {
        height: 0;
        padding-bottom: 177.77%;
        position: relative;
    }
    .video-preview > video {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
}
"""

with open('static/style.css.min', 'a', encoding='utf-8') as f:
    f.write(code)

shutil.copy('static/style.css.min', 'static/style.css')
print("Successfully appended polyfills and copied to style.css")
