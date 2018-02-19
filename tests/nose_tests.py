import nose as ns
from src import main as mn

def test_import_data():
    file = mn.load_file(r'..\data\Supplemental Data S2.csv')
    assert file.iloc[30114,12] == 15810.0158

