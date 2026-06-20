import json
from dataclasses import dataclass
from typing import List

@dataclass
class ClickData:
    x: int
    y: int
    count: int

class Heatmap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.click_data = []

    def add_click(self, x: int, y: int):
        for click in self.click_data:
            if click.x == x and click.y == y:
                click.count += 1
                return
        self.click_data.append(ClickData(x, y, 1))

    def generate_heatmap(self) -> List[List[int]]:
        heatmap = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for click in self.click_data:
            heatmap[click.y][click.x] = click.count
        return heatmap

    def render_heatmap(self) -> str:
        heatmap = self.generate_heatmap()
        max_count = max(max(row) for row in heatmap) if any(any(row) for row in heatmap) else 1
        html = ""
        for y, row in enumerate(heatmap):
            for x, count in enumerate(row):
                color = self.get_color(count, max_count)
                html += f"<div style='position: absolute; top: {y}px; left: {x}px; width: 1px; height: 1px; background-color: {color};'></div>"
        return html

    def get_color(self, count: int, max_count: int) -> str:
        ratio = count / max_count
        r = int(255 * ratio)
        g = 0
        b = int(255 * (1 - ratio))
        return f"rgb({r}, {g}, {b})"

    def toggle_heatmap(self, enabled: bool) -> str:
        if enabled:
            return self.render_heatmap()
        else:
            return ""
