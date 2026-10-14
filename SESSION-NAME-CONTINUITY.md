# Visitor name continuity

- First successful welcome form saves the entered name to Neon and to tab-scoped sessionStorage.
- The welcome envelope does not reappear on page refresh or same-tab navigation.
- The homepage welcome and Concierge read the current tab name. RSVP and Wishes can update it for the current tab.
- The visit/session identifier also survives refresh within the tab.
- A new tab normally starts a new session and asks for a name again. Some browsers restore sessionStorage when restoring closed tabs, so tab close is not an absolute expiry guarantee.
- No name is inferred from device identifiers.
