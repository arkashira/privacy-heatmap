from heatmap import Heatmap, ClickData

def test_generate_heatmap():
    heatmap = Heatmap(10, 10)
    heatmap.add_click(5, 5)
    heatmap.add_click(5, 5)
    heatmap.add_click(3, 3)
    expected_heatmap = [[0 for _ in range(10)] for _ in range(10)]
    expected_heatmap[5][5] = 2
    expected_heatmap[3][3] = 1
    assert heatmap.generate_heatmap() == expected_heatmap

def test_render_heatmap():
    heatmap = Heatmap(10, 10)
    heatmap.add_click(5, 5)
    heatmap.add_click(5, 5)
    heatmap.add_click(3, 3)
    rendered_heatmap = heatmap.render_heatmap()
    assert "rgb(255, 0, 0)" in rendered_heatmap
    assert "rgb(0, 0, 255)" in rendered_heatmap

def test_toggle_heatmap():
    heatmap = Heatmap(10, 10)
    assert heatmap.toggle_heatmap(True) != ""
    assert heatmap.toggle_heatmap(False) == ""

def test_get_color():
    heatmap = Heatmap(10, 10)
    assert heatmap.get_color(10, 10) == "rgb(255, 0, 0)"
    assert heatmap.get_color(0, 10) == "rgb(0, 0, 255)"
