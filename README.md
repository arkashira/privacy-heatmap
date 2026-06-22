# Collector
A lightweight JavaScript collector for recording visitor events.

## Features

* Records click, scroll, mouse-move, and form-field focus events
* Stores events in a MySQL table prefixed with `wp_ph_`
* No HTTP requests are made to domains outside the host server

## Usage

1. Install the collector using pip: `pip install collector`
2. Import the collector in your Python script: `from collector import Collector`
3. Create a collector instance: `collector = Collector()`
4. Collect events: `collector.collect(Event('click', {'x': 10, 'y': 20}))`
5. Store events in a database: `collector.store(db)`
