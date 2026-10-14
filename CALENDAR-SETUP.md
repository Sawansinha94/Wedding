# Auspicious Ceremonies — Add to Calendar

Each ceremony has an **Add to your Calendar** button directly beneath its title.

- Android: opens a pre-filled Google Calendar event. The visitor must tap **Save**.
- iPhone/iPad: downloads a standard `.ics` event that can be imported into iOS Calendar. Depending on iOS/browser settings, the visitor may need to open the downloaded file or share it to Calendar.
- Other platforms: opens Google Calendar.

Websites cannot silently insert events into personal calendars without authorization. Device detection is best-effort and is not identification of the visitor.

## Events
- Lagan: 20 Nov 2026, 4:00 PM IST. Venue not provided.
- Haldi: 22 Nov 2026, 6:00 PM IST. Venue not provided.
- Wedding: 24 Nov 2026, 7:00 PM IST, Swastik Foundation, Ranchi Ring Road, Ranchi, Jharkhand.
- Reception: 27 Nov 2026, 7:00 PM IST, Our Residence, Baghmara, Talcher, Odisha.

All event times are **start times**. The calendar entries use a provisional two-hour duration because no ending times were supplied. Adjust `eventTimes` in `assets/js/10-ceremony-calendar.js` when actual durations are known.

The JavaScript does not require new API keys or backend endpoints.
