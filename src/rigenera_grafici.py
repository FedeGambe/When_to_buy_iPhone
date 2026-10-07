"""Rigenera i grafici Plotly dai CSV di data/ e li sostituisce, in ordine, nei <figure> di docs/index.html.
Uso: python src/rigenera_grafici.py   (il testo della pagina non viene toccato)"""
import re
from pathlib import Path

from utils import calcoli, grafici
from utils.dati import carica_modello

PAGINA = Path(__file__).resolve().parent.parent / "docs" / "index.html"
MODELLI = ["iPhone14", "iPhone15", "iPhone16", "iPhone17"]


def figure(dati):
    """Nello stesso ordine in cui compaiono nella pagina."""
    return [
        grafici.sconto_per_giorno(dati),
        grafici.heatmap_trimestri(dati),
        grafici.box_trimestri(dati),
        grafici.minimi(calcoli.riepilogo_minimi(dati)),
        grafici.costo_attesa({m: calcoli.costo_attesa(df) for m, df in dati.items()}),
        grafici.stagionalita(calcoli.stagionalita_mensile(dati), calcoli.stagionalita_settimanale(dati)),
        grafici.offerte(calcoli.profilo_offerte(dati)),
        grafici.effetto_lancio(calcoli.effetto_lancio(dati)),
    ]


def main():
    dati = {m: carica_modello(m) for m in MODELLI}
    html = PAGINA.read_text(encoding="utf-8")
    blocchi = list(re.finditer(r"<figure>.*?</figure>", html, flags=re.S))
    nuove = figure(dati)
    assert len(blocchi) == len(nuove), f"{len(blocchi)} figure nella pagina, {len(nuove)} grafici"
    for i, (b, fig) in reversed(list(enumerate(zip(blocchi, nuove)))):  # dal fondo, così gli indici restano validi
        fig = grafici.stile_html(fig)
        corpo = fig.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False, config=grafici.CONFIG_HTML,
                            post_script=grafici.POST_BOTTONI if fig.layout.meta else None)
        html = html[:b.start()] + "<figure>" + corpo + "</figure>" + html[b.end():]
    PAGINA.write_text(html, encoding="utf-8")
    print(f"{len(nuove)} grafici aggiornati in {PAGINA}")


if __name__ == "__main__":
    main()
