# Privacy Heatmap
A Python project for automatically purging data older than 90 days.

## Usage
1. Create a `PrivacyHeatmap` object.
2. Add records to the object using the `add_record` method.
3. Call the `purge_records` method to remove records older than 90 days.
4. Access the log of purged records using the `get_log` method.

## Testing
Run the tests using `pytest`.
