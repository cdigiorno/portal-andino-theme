# coding=utf-8
from config_controller import GobArConfigController


def get_theme_config(path=None, default=None):
    return GobArConfigController.get_theme_config(path, default)


def update_frequencies(freq_id=None):
    frequencies = [
        ("R/PT1S", "Continuamente actualizado"),
        ("R/PT1H", "Cada hora"),
        ("R/P1D", "Diariamente"),
        ("R/P0.33W", "Tres veces a la semana"),
        ("R/P0.5W", "Dos veces a la semana"),
        ("R/P3.5D", "Cada media semana"),
        ("R/P1W", "Semanalmente"),
        ("R/P0.33M", "Tres veces por mes"),
        ("R/P0.5M", "Cada 15 días"),
        ("R/P1M", "Mensualmente"),
        ("R/P2M", "Bimestralmente"),
        ("R/P3M", "Trimestralmente"),
        ("R/P4M", "Cuatrimestralmente"),
        ("R/P6M", "Cada medio año"),
        ("R/P1Y", "Anualmente"),
        ("R/P2Y", "Cada dos años"),
        ("R/P3Y", "Cada tres años"),
        ("R/P4Y", "Cada cuatro años"),
        ("R/P10Y", "Cada diez años"),
        ('eventual', 'Eventual')
    ]
    if freq_id is not None:
        filtered_freq = filter(lambda freq: freq[0] == freq_id, frequencies)
        if len(filtered_freq) > 0:
            return filtered_freq[0]
        return None
    return frequencies
