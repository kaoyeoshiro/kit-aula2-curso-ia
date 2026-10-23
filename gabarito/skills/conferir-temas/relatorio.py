"""Gera o relatório de conformidade com os Temas 6 e 1234 do STF em Word, a partir de um JSON.
Uso: python3 relatorio.py caso.json logo.png saida.docx   (precisa de python-docx: pip install python-docx)"""
import json, sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

VERDE, COBRE, CINZA = "064A45", "B87548", "666666"
SITUACAO = {   # rótulo, cor de fundo
    "atendido": ("Atendido", "2E7D5B"),
    "nao_comprovado": ("Alegado, não comprovado", "C98A0B"),
    "nao_encontrado": ("Não encontrei nos autos", "B3402F"),
    "dispensado": ("Dispensado", "5F7390"),
}
NOME = "Dias & Moura"


def rgb(h):
    return RGBColor.from_string(h)


def run(par, texto, tam=11, negrito=False, cor=None, italico=False):
    r = par.add_run(texto)
    r.font.name = "Georgia"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Georgia")
    r.font.size = Pt(tam); r.bold = negrito; r.italic = italico
    if cor: r.font.color.rgb = rgb(cor)
    return r


def fundo(cel, cor):
    pr = cel._tc.get_or_add_tcPr()
    for velho in pr.findall(qn("w:shd")):
        pr.remove(velho)
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), cor)
    pr.append(s)


def bordas(cel, **lados):
    """lados: top/bottom/left/right = (cor, tamanho em oitavos de ponto); lado omitido fica sem borda."""
    pr = cel._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for lado in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{lado}"); v = lados.get(lado)
        e.set(qn("w:val"), "single" if v else "nil")
        if v: e.set(qn("w:sz"), str(v[1])); e.set(qn("w:color"), v[0])
        b.append(e)
    pr.append(b)


def margens(cel, cima=80, lados=140):
    pr = cel._tc.get_or_add_tcPr(); m = OxmlElement("w:tcMar")
    for k, v in (("top", cima), ("start", lados), ("bottom", cima), ("end", lados)):
        e = OxmlElement(f"w:{k}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    pr.append(m)


def filete(par, cor=COBRE, tam=12):
    pr = par._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", str(tam)), ("space", "4"), ("color", cor)):
        e.set(qn(f"w:{k}"), v)
    b.append(e); pr.append(b)


def larguras(tab, cms):
    tab.autofit = False
    pr = tab._tbl.tblPr
    for velho in pr.findall(qn("w:tblW")) + pr.findall(qn("w:tblLayout")):
        pr.remove(velho)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), str(int(sum(cms) * 567))); w.set(qn("w:type"), "dxa"); pr.append(w)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); pr.append(lay)
    for lin in tab.rows:
        for c, w in zip(lin.cells, cms):
            c.width = Cm(w)


def campo(par, instr):
    for t, txt in (("begin", None), (None, instr), ("end", None)):
        r = run(par, "", 8.5, cor=CINZA)
        if t:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), t); r._r.append(f)
        else:
            i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = txt; r._r.append(i)


def titulo_secao(doc, texto):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18); p.paragraph_format.space_after = Pt(6)
    run(p, texto, 12, True, VERDE)


def linha_fina(par, lado="bottom", cor="BFBFBF", tam=4, espaco=4):
    pr = par._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement(f"w:{lado}")
    for k, v in (("val", "single"), ("sz", str(tam)), ("space", str(espaco)), ("color", cor)):
        e.set(qn(f"w:{k}"), v)
    b.append(e); pr.append(b)


def main(caso_json, logo, saida):
    c = json.load(open(caso_json, encoding="utf-8"))
    d = Document(); sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.25); sec.top_margin, sec.bottom_margin = Cm(3.0), Cm(2.2)
    d.styles["Normal"].font.name = "Georgia"; d.styles["Normal"].font.size = Pt(11)
    d.styles["Normal"].paragraph_format.space_after = Pt(0); d.styles["Normal"].paragraph_format.line_spacing = 1.2
    L = sec.page_width - sec.left_margin - sec.right_margin
    h = sec.header.paragraphs[0]; h.paragraph_format.tab_stops.add_tab_stop(L, WD_TAB_ALIGNMENT.RIGHT)
    h.add_run().add_picture(logo, height=Cm(1.3)); run(h, "\t\tDocumento de trabalho", 9, cor=CINZA); linha_fina(h, cor=COBRE, tam=6, espaco=6)
    f = sec.footer.paragraphs[0]; f.paragraph_format.tab_stops.add_tab_stop(L, WD_TAB_ALIGNMENT.RIGHT)
    run(f, f"{NOME} Advocacia · documento fictício\t\tPágina ", 8.5, cor=CINZA); campo(f, "PAGE")

    # título
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    run(p, "Relatório de conformidade", 20, True, VERDE)
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(10)
    run(p, f"Temas 6 e 1234 do STF · {c['medicamento']}", 11, False, CINZA, italico=True); linha_fina(p, cor=COBRE, tam=8, espaco=8)

    # ficha do caso
    ficha = d.add_table(rows=3, cols=2); larguras(ficha, [5.0, 11.5])
    for i, (k, v) in enumerate([("Processo", c["processo"]), ("Autor representado por", c["representacao"]),
                                ("Data da análise", c["data_analise"])]):
        a, b = ficha.rows[i].cells
        for x in (a, b): margens(x, 50, 0); bordas(x, bottom=("D9D9D9", 4))
        run(a.paragraphs[0], k, 10, False, CINZA); run(b.paragraphs[0], v, 10.5, True)

    # conclusão
    ok = sum(1 for r in c["requisitos"] if r["situacao"] in ("atendido", "dispensado"))
    total = len(c["requisitos"]); cumpriu = ok == total
    titulo_secao(d, "Conclusão")
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(4)
    run(p, "O autor cumpriu os requisitos do Tema 6. " if cumpriu else "O autor não cumpriu todos os requisitos do Tema 6. ", 11, True)
    run(p, f"Estão atendidos ou dispensados {ok} de {total}. ", 11)
    run(p, c["resumo"], 11)

    # matriz
    titulo_secao(d, "Tema 6: requisitos")
    m = d.add_table(rows=1, cols=4)
    for cel, txt in zip(m.rows[0].cells, ("Requisito", "Situação", "Onde nos autos", "Observação")):
        margens(cel, 60, 80); bordas(cel, bottom=(VERDE, 10)); run(cel.paragraphs[0], txt, 9, True, VERDE)
    for r in c["requisitos"]:
        lin = m.add_row().cells; rot, cor = SITUACAO[r["situacao"]]
        for cel in lin: margens(cel, 70, 80); bordas(cel, bottom=("D9D9D9", 4))
        run(lin[0].paragraphs[0], f"({r['id']}) {r['nome']}", 9.5)
        run(lin[1].paragraphs[0], "● ", 9.5, False, cor); run(lin[1].paragraphs[0], rot, 9.5, True, cor)
        run(lin[2].paragraphs[0], r["onde"], 9.5); run(lin[3].paragraphs[0], r["obs"], 9.5)
    larguras(m, [3.7, 2.8, 3.4, 6.6])
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(4)
    for rot, cor in SITUACAO.values():
        run(p, "●", 8, False, cor); run(p, f" {rot}    ", 8, False, CINZA)

    # competência
    titulo_secao(d, "Tema 1234: competência")
    cp = c["competencia"]; k = d.add_table(rows=3, cols=2); larguras(k, [7.0, 9.5])
    for i, (rot, val) in enumerate([("Valor anual do tratamento", cp["valor_anual"]), ("210 salários mínimos", cp["limite"]),
                                    ("Onde tramita", cp["resultado"])]):
        a, b = k.rows[i].cells
        for x in (a, b): margens(x, 50, 0); bordas(x, bottom=("D9D9D9", 4))
        run(a.paragraphs[0], rot, 10, False, CINZA); run(b.paragraphs[0], val, 10.5, True)
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(6); run(p, cp["nota"], 9, italico=True, cor=CINZA)

    # conferência humana
    titulo_secao(d, "Pontos para conferência humana")
    for item in c["conferencia"]:
        p = d.add_paragraph(); p.paragraph_format.space_after = Pt(3); p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.5); run(p, "–  " + item, 10)
    d.save(saida)


if __name__ == "__main__":
    main(*sys.argv[1:4])
