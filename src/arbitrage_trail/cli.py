"""Ligne de commande.

    arbitrage-trail list    EXPORT              # inventaire de l'export
    arbitrage-trail convert EXPORT -o VAULT     # un .md par conversation
    arbitrage-trail serve   [--host] [--port]   # web app
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .export import write_dir
from .loader import load_path
from .parsers import PARSERS, UnknownFormat


def _filter(convs, query: str | None):
    if not query:
        return convs
    q = query.lower()
    return [c for c in convs if q in c.title.lower() or c.id.startswith(query)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="arbitrage-trail", description="Conversations génératives -> Markdown.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sources = ["auto", *PARSERS]

    p_list = sub.add_parser("list", help="Lister les conversations d'un export")
    p_list.add_argument("export")
    p_list.add_argument("--source", choices=sources, default="auto")

    p_conv = sub.add_parser("convert", help="Convertir un export en fichiers Markdown")
    p_conv.add_argument("export")
    p_conv.add_argument("-o", "--out", required=True, help="Dossier de sortie (ex. vault Obsidian)")
    p_conv.add_argument("--source", choices=sources, default="auto")
    p_conv.add_argument("--match", help="Ne convertir que les titres contenant ce texte (ou cet id)")

    p_srv = sub.add_parser("serve", help="Lancer la web app")
    p_srv.add_argument("--host", default="127.0.0.1")
    p_srv.add_argument("--port", type=int, default=8765)
    p_srv.add_argument("--vault", help="Dossier où le bouton « Enregistrer dans le vault » écrit")

    args = p.parse_args(argv)

    if args.cmd == "serve":
        from .web import serve

        serve(args.host, args.port, vault=args.vault)
        return 0

    try:
        convs = load_path(args.export, args.source)
    except (OSError, UnknownFormat) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 2

    if args.cmd == "list":
        for c in convs:
            date = c.created.strftime("%Y-%m-%d") if c.created else "????-??-??"
            flag = "  ⚠" if c.warnings else ""
            print(f"{date}  {c.source:<8} {len(c.messages):>4} msg  {c.title}{flag}")
        print(f"\n{len(convs)} conversation(s).")
        return 0

    selected = _filter(convs, args.match)
    paths = write_dir(selected, args.out)
    incomplete = sum(1 for c in selected if c.warnings)
    print(f"{len(paths)} fichier(s) écrit(s) dans {args.out}" + (f" ({incomplete} avec avertissement)" if incomplete else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
