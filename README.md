# Session Replay Engine

This project provides a session replay engine that can load and play back user sessions.

## Features
* Loads session events within 3 seconds
* Includes mouse movements, clicks, and scrolls
* Can be paused, resumed, and scrubbed

## Usage
1. Create a `SessionReplay` object with a list of `SessionEvent` objects.
2. Call the `load` method to load the session events.
3. Call the `play` method to start playing back the session.
4. Call the `pause` method to pause the playback.
5. Call the `resume` method to resume the playback.
6. Call the `scrub` method to scrub to a specific timestamp.
