"""Rigenera i grafici Plotly dai CSV di data/ e li salva in docs/grafici.json, che docs/index.html carica all'apertura.
Uso: python src/rigenera_grafici.py   (la pagina e il suo testo non vengono toccati)"""
import json
from pathlib import Path

from utils import calcoli, grafici
from utils.dati import carica_modello

USCITA = Path(__file__).resolve().parent.parent / "docs" / "grafici.json"
MODELLI = ["iPhone14", "iPhone15", "iPhone16", "iPhone17"]


def figure(dati):
    """{nome: figura}; il nome e' quello di data-grafico nei <div class="grafico"> della pagina."""
    return {
        "sconto_per_giorno": grafici.sconto_per_giorno(dati),
        "heatmap_trimestri": grafici.heatmap_trimestri(dati),
        "box_trimestri": grafici.box_trimestri(dati),
        "minimi": grafici.minimi(calcoli.riepilogo_minimi(dati)),
        "costo_attesa": grafici.costo_attesa({m: calcoli.costo_attesa(df) for m, df in dati.items()}),
        "stagionalita": grafici.stagionalita(calcoli.stagionalita_mensile(dati), calcoli.stagionalita_settimanale(dati)),
        "offerte": grafici.offerte(calcoli.profilo_offerte(dati)),
        "effetto_lancio": grafici.effetto_lancio(calcoli.effetto_lancio(dati)),
    }


def main():
    dati = {m: carica_modello(m) for m in MODELLI}
    fig = {nome: json.loads(grafici.stile_html(f).to_json()) for nome, f in figure(dati).items()}
    USCITA.write_text(json.dumps(fig, separators=(",", ":")), encoding="utf-8")
    print(f"{len(fig)} grafici salvati in {USCITA} ({USCITA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
