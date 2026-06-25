# Collector
A lightweight JavaScript collector for recording visitor events.

## Features

* Records click, scroll, mousemove, and form-field focus events
* Stores events in a MySQL table prefixed with `wp_ph_`
* No HTTP requests are made to domains outside the host server

## Installation

1. Install the collector plugin on your WordPress site
2. Configure the plugin to inject the collector script

## Usage

1. Visit your WordPress site
2. Interact with the site to generate events
3. The collector will record and store the events in the database
