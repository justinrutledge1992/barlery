# Seeding Events for Barlery

This guide explains how to populate your development database with sample events.

## Setup

1. Create the management command directory structure:
   ```bash
   mkdir -p barlery/management/commands
   ```

2. Create `__init__.py` files:
   ```bash
   touch barlery/management/__init__.py
   touch barlery/management/commands/__init__.py
   ```

3. Place `seed_events.py` in `barlery/management/commands/`

## Usage

### Seed the database with sample events:
```bash
python manage.py seed_events
```

### Clear existing events and reseed:
```bash
python manage.py seed_events --clear
```

## What Gets Created

The command creates 12 diverse sample events including:

- **Live Music**: Jazz nights, rock bands, acoustic performances, tribute bands
- **Interactive Events**: Open mic nights, karaoke, trivia nights
- **Special Events**: Beer tastings, comedy shows, New Year's Eve celebration
- **Community Events**: Local artist showcases, vinyl listening nights

Each event includes:
- Title
- Date (spread over the next 45 days)
- Start and end times
- Detailed description

## Event Dates

All events are scheduled relative to today's date:
- Events are spread from 3 days out to 45 days out
- This ensures they always appear as "upcoming" events
- Events are automatically sorted by date on the calendar page

## Notes

- Events won't be duplicated - if an event with the same title and date exists, it will be skipped
- The `--clear` flag deletes ALL events before seeding (use with caution in production!)
- You can run the command multiple times safely
- Events don't include images by default (they'll use placeholder images)

## Customization

To modify the events, edit the `events_data` list in `seed_events.py`. Each event is a dictionary with:
- `title`: Event name (string)
- `date`: Event date (date object)
- `start_time`: Start time (time object)
- `end_time`: End time (time object)
- `description`: Event details (text)

## Example Output

```
Seeding events...
  ✓ Created: Live Jazz Night with The Riverside Trio on 2024-12-26
  ✓ Created: Open Mic Night on 2024-12-30
  ✓ Created: Trivia Tuesday: 90s Pop Culture Edition on 2025-01-02
  ...

✓ Successfully seeded 12 events!
Total events in database: 12
```