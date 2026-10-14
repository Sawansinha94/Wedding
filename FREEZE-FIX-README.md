# Chrome Page Unresponsive — performance patch

## Root cause
The multilingual script observed every newly added DOM node and rescanned the entire page on a short timer. Animated petals append a DOM node every 750 ms, so this continuously retriggered the full-page translation traversal. The proactive concierge also creates dynamic DOM nodes.

## Fixes
- Ignore decorative petals and other irrelevant nodes in the translation observer.
- Disconnect the observer during translation and language-change updates to prevent feedback loops.
- Debounce meaningful dynamic content changes to 350 ms.
- Reduce petal creation frequency and prevent duplicate animation timers.
- Keep the bundled English/Hindi/Odia/Telugu translations and existing backend unchanged.

## Run
Extract the ZIP and run the website using your existing startup instructions. Hard refresh Chrome with Cmd+Shift+R. If it still freezes, use Chrome Performance recording to identify the next blocking script.

## Validation
JavaScript syntax checked. Live Chrome behavior and API connectivity have not been tested.
