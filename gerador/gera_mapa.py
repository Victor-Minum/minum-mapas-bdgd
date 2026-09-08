# -*- coding: utf-8 -*-
"""Gera o mapa HTML + o Excel de campo de UCs de alto consumo, a partir da BDGD.

Uso (rodar de dentro de Documents\bdgd\mapas):
  python gera_mapa.py --uf MT --cidade 5103403=Cuiaba --cidade 5108402="Varzea Grande" \
      --titulo "Cuiaba + Varzea Grande - MT" --min 5000 --slug Cuiaba_VarzeaGrande

Le apenas os .parquet em <UF>\out\ (UCBT_tab, PONNOT, EQME, UGBT_tab).
"""
import argparse, csv, json, os, re, struct, sys, unicodedata
import duckdb, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cnae_map

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)                       # ...\mapas-bdgd
BASE_PADRAO = os.environ.get("BDGD_BASE", r"C:\Users\VictorFranco\Documents\bdgd")

UF_COD = {"RO":"11","AC":"12","AM":"13","RR":"14","PA":"15","AP":"16","TO":"17",
          "MA":"21","PI":"22","CE":"23","RN":"24","PB":"25","PE":"26","AL":"27","SE":"28",
          "BA":"29","MG":"31","ES":"32","RJ":"33","SP":"35","PR":"41","SC":"42","RS":"43",
          "MS":"50","MT":"51","GO":"52","DF":"53"}

def municipios_da_uf(uf):
    """Nome de cada municipio da UF, do cadastro IBGE em gerador/municipios.csv."""
    arq = os.path.join(AQUI, "municipios.csv")
    if not os.path.exists(arq):
        sys.exit("municipios.csv nao encontrado em " + AQUI + " — necessario para --estado")
    cod = UF_COD[uf.upper()]
    with open(arq, encoding="utf-8") as f:
        return {r["codigo_ibge"]: r["nome"] for r in csv.DictReader(f) if r["codigo_uf"] == cod}

CLASSE = {"RE": "Residencial", "CO": "Comercial", "IN": "Industrial", "RU": "Rural",
          "PP": "Poder Público", "IP": "Iluminação Pública", "SP": "Serviço Público",
          "CPR": "Consumo Próprio"}

def classe_de(cs):
    if not cs:
        return "Não informada"
    cs = str(cs).strip().upper()
    if cs.startswith("CPR"):
        return "Consumo Próprio"
    return CLASSE.get(cs[:2], "Não informada")

def wkb_ponto_xy(b):
    if b is None or not isinstance(b, (bytes, bytearray, memoryview)):
        return (None, None)
    b = bytes(b)
    if len(b) < 21:
        return (None, None)
    o = "<" if b[0] == 1 else ">"
    tipo = struct.unpack(o + "I", b[1:5])[0]
    pos = 5
    if tipo & 0x20000000:
        pos += 4
    if (tipo & 0xFF) != 1:
        return (None, None)
    x, y = struct.unpack(o + "dd", b[pos:pos + 16])
    return (round(y, 7), round(x, 7))

def jitter(cod, i):
    """Deslocamento deterministico de poucos metros, so para UCs que dividem o mesmo poste."""
    if i == 0:
        return (0.0, 0.0)
    h = 0
    for ch in str(cod):
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    ang = ((h % 360) + i * 47) * 3.14159265 / 180.0
    r = 0.000045 + 0.000025 * ((i - 1) % 3)
    import math
    return (r * math.cos(ang), r * math.sin(ang))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uf", required=True)
    ap.add_argument("--cidade", action="append", default=[],
                    help='CODIGO_IBGE=Nome (pode repetir)')
    ap.add_argument("--estado", action="store_true",
                    help="todas as cidades da UF (nomes vindos de municipios.csv)")
    ap.add_argument("--titulo", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--min", type=float, default=5000.0)
    ap.add_argument("--base", default=BASE_PADRAO,
                    help="pasta da BDGD (onde ficam MT\\out, GO\\out, ...)")
    ap.add_argument("--docs", default=os.path.join(RAIZ, "docs"))
    ap.add_argument("--planilhas", default=os.path.join(RAIZ, "docs", "planilhas"))
    ap.add_argument("--manter-pp", action="store_true",
                    help="nao excluir poder publico / IP / saneamento / consumo proprio")
    a = ap.parse_args()

    if a.estado:
        nomes = municipios_da_uf(a.uf)
        muns = list(nomes)
        print(f"[0/7] modo estado: {len(muns)} municipios de {a.uf.upper()} no cadastro IBGE")
    else:
        if not a.cidade:
            sys.exit("informe --cidade CODIGO=Nome (pode repetir) ou --estado")
        muns, nomes = [], {}
        for c in a.cidade:
            cod, _, nome = c.partition("=")
            muns.append(cod.strip())
            nomes[cod.strip()] = (nome.strip() or cod.strip())

    BASE = a.base
    out = os.path.join(BASE, a.uf, "out")
    os.makedirs(a.docs, exist_ok=True); os.makedirs(a.planilhas, exist_ok=True)
    ucbt = os.path.join(out, "UCBT_tab.parquet").replace("\\", "/")
    ponnot = os.path.join(out, "PONNOT.parquet").replace("\\", "/")
    eqme = os.path.join(out, "EQME.parquet").replace("\\", "/")
    ugbt = os.path.join(out, "UGBT_tab.parquet").replace("\\", "/")

    con = duckdb.connect()
    con.execute("SET preserve_insertion_order = false")
    ene = " + ".join(f"COALESCE(ENE_{m:02d},0)" for m in range(1, 13))
    lista = ",".join("'" + m + "'" for m in muns)
    excl = "" if a.manter_pp else (
        " AND NOT (CLAS_SUB LIKE 'PP%' OR CLAS_SUB = 'IP' OR CLAS_SUB LIKE 'SP%' "
        "OR CLAS_SUB = 'CPR') AND substr(CNAE,1,2) NOT IN ('84','36','37')")

    print("[1/7] mapeando clientes de media tensao (mesmo COD_ID na UCMT)...")
    ucmt = os.path.join(out, "UCMT_tab.parquet").replace("\\", "/")
    con.execute(f"""
      CREATE TABLE mtcli AS SELECT DISTINCT COD_ID FROM read_parquet('{ucmt}')
    """)

    print("[2/7] filtrando UCs de BT...")
    con.execute(f"""
      CREATE TABLE bt_bruta AS
      SELECT COD_ID, PN_CON, MUN, BRR, CEP, CNAE, CLAS_SUB, GRU_TAR, GRU_TEN, TEN_FORN,
             CAR_INST, DAT_CON, ARE_LOC, CEG_GD, CTMT,
             ({ene})/12.0 AS KWH_MES, ({ene})*1.0 AS KWH_ANO
      FROM read_parquet('{ucbt}')
      WHERE SIT_ATIV='AT' AND MUN IN ({lista}) AND ({ene})/12.0 >= {a.min} {excl}
    """)
    bruto = con.execute("SELECT COUNT(*) FROM bt_bruta").fetchone()[0]
    con.execute("""
      CREATE TABLE bt AS SELECT b.* FROM bt_bruta b
      WHERE NOT EXISTS (SELECT 1 FROM mtcli m WHERE m.COD_ID = b.COD_ID)
    """)
    n = con.execute("SELECT COUNT(*) FROM bt").fetchone()[0]
    print(f"      {bruto} UCs no recorte; {bruto - n} excluidas por serem clientes de media tensao")
    print(f"      {n} UCs de baixa tensao")

    print("[3/7] contando UCs por poste...")
    con.execute(f"""
      CREATE TABLE postes AS
      SELECT PN_CON, COUNT(*) AS UC_NO_POSTE
      FROM read_parquet('{ucbt}')
      WHERE SIT_ATIV='AT' AND MUN IN ({lista}) GROUP BY 1
    """)

    print("[4/7] medidores (EQME)...")
    con.execute(f"""
      CREATE TABLE med AS
      SELECT e.UC_UG AS COD_ID, string_agg(e.COD_ID, ' / ') AS MEDIDOR,
             min(e.DAT_IMO) AS MED_DESDE
      FROM read_parquet('{eqme}') e
      JOIN bt ON bt.COD_ID = e.UC_UG GROUP BY 1
    """)

    print("[5/7] potencia de GD (UGBT)...")
    con.execute(f"""
      CREATE TABLE ug AS
      SELECT CEG_GD, SUM(COALESCE(POT_INST,0)) AS POT_GD
      FROM read_parquet('{ugbt}')
      WHERE CEG_GD IS NOT NULL AND TRIM(CEG_GD) <> '' GROUP BY 1
    """)

    print("[6/7] coordenada (PONNOT) e montagem...")
    df = con.execute(f"""
      SELECT b.*, p."Shape" AS _WKB, m.MEDIDOR, m.MED_DESDE,
             COALESCE(po.UC_NO_POSTE,1) AS UC_NO_POSTE, ug.POT_GD
      FROM bt b
      LEFT JOIN read_parquet('{ponnot}') p ON p.COD_ID = b.PN_CON
      LEFT JOIN med m ON m.COD_ID = b.COD_ID
      LEFT JOIN postes po ON po.PN_CON = b.PN_CON
      LEFT JOIN ug ON ug.CEG_GD = b.CEG_GD
      ORDER BY b.KWH_MES DESC
    """).df()

    df["LAT"], df["LON"] = zip(*df["_WKB"].map(wkb_ponto_xy))
    sem_coord = int(df["LAT"].isna().sum())
    print(f"      sem coordenada: {sem_coord} de {len(df)}")
    df = df.dropna(subset=["LAT", "LON"]).reset_index(drop=True)

    df["Cidade"] = df["MUN"].map(nomes)
    df["Classe"] = df["CLAS_SUB"].map(classe_de)
    setdes = df["CNAE"].map(cnae_map.lookup)
    df["Setor"] = [s[0] for s in setdes]
    df["CNAE_DESCR"] = [s[1] for s in setdes]
    df["Tem_GD"] = df["CEG_GD"].fillna("").astype(str).str.strip().ne("").map({True: "Sim", False: "Nao"})
    df["Rank"] = range(1, len(df) + 1)

    # jitter so entre UCs do mesmo poste dentro da selecao
    df["_ord"] = df.groupby("PN_CON").cumcount()
    dl = [jitter(c, i) for c, i in zip(df["COD_ID"], df["_ord"])]
    df["LAT_MAPA"] = df["LAT"] + [d[0] for d in dl]
    df["LON_MAPA"] = df["LON"] + [d[1] for d in dl]

    # distancia ao centro da propria cidade -> sinaliza coordenada suspeita (ressalva 7 do guia)
    # O limite nao pode ser fixo: municipio de MT ou do PA e maior que estado do Sudeste,
    # entao UC rural legitima fica a 60 km da sede. Usamos a propria dispersao da cidade:
    # suspeito e o que passa de 3x o p90 dela, com piso de 40 km.
    import math
    df["DIST_CENTRO_KM"] = 0.0
    df["_LIM"] = 40.0
    for mun, g in df.groupby("MUN"):
        la0, lo0 = g["LAT"].median(), g["LON"].median()
        d = [round(math.hypot((la - la0) * 111.0, (lo - lo0) * 111.0 * math.cos(math.radians(la0))), 1)
             for la, lo in zip(g["LAT"], g["LON"])]
        df.loc[g.index, "DIST_CENTRO_KM"] = d
        p90 = pd.Series(d).quantile(0.90) if len(d) >= 5 else max(d + [0.0])
        df.loc[g.index, "_LIM"] = round(max(40.0, 3.0 * float(p90)), 1)
    df["COORD_OK"] = df["DIST_CENTRO_KM"] <= df["_LIM"]
    print(f"      coordenada a conferir: {int((~df['COORD_OK']).sum())} de {len(df)}")

    df["Link_Maps"] = ("https://www.google.com/maps?q=" +
                       df["LAT"].astype(str) + "," + df["LON"].astype(str))

    # ---------------- Excel ----------------
    print("[7/7] gravando Excel e HTML...")
    cols = [("Rank", "Rank"), ("Cidade", "Cidade"), ("KWH_MES", "Consumo médio (kWh/mês)"),
            ("KWH_ANO", "Consumo ano (kWh)"), ("Classe", "Classe"), ("Setor", "Setor"),
            ("CNAE", "CNAE"), ("CNAE_DESCR", "Descrição CNAE"), ("BRR", "Bairro"),
            ("CEP", "CEP"), ("MEDIDOR", "Medidor(es)"), ("MED_DESDE", "Medidor instalado em"),
            ("GRU_TAR", "Grupo tarifário"), ("TEN_FORN", "Cód. tensão (TEN_FORN)"),
            ("CAR_INST", "Carga instalada (kW)"), ("DAT_CON", "Ligação em"),
            ("Tem_GD", "Tem GD"), ("POT_GD", "Potência GD (kW)"), ("ARE_LOC", "Área"),
            ("UC_NO_POSTE", "UCs no mesmo poste"),
            ("DIST_CENTRO_KM", "Dist. do centro (km)"), ("_LIM", "Limite da cidade (km)"),
            ("COORD_OK", "Coordenada confiável"),
            ("LAT", "Latitude"), ("LON", "Longitude"),
            ("Link_Maps", "Google Maps"), ("COD_ID", "COD_ID da UC"), ("PN_CON", "Poste (PN_CON)")]
    x = df[[c[0] for c in cols]].copy()
    x.columns = [c[1] for c in cols]
    x["Consumo médio (kWh/mês)"] = x["Consumo médio (kWh/mês)"].round(1)
    x["Consumo ano (kWh)"] = x["Consumo ano (kWh)"].round(0)
    for extra in ["Visitado?", "Nome do local", "Responsável / contato", "Telefone",
                  "Interesse", "Observação"]:
        x[extra] = ""

    xls = os.path.join(a.planilhas, f"UCs_{a.slug}.xlsx")
    with pd.ExcelWriter(xls, engine="xlsxwriter") as w:
        x.to_excel(w, sheet_name="UCs", index=False, startrow=1, header=False)
        wb, ws = w.book, w.sheets["UCs"]
        hdr = wb.add_format({"bold": True, "bg_color": "#16324F", "font_color": "#FFFFFF",
                             "border": 1, "text_wrap": True, "valign": "vcenter"})
        num = wb.add_format({"num_format": "#,##0.0"})
        num0 = wb.add_format({"num_format": "#,##0"})
        anot = wb.add_format({"bg_color": "#FFF7E0", "border": 1})
        for i, c in enumerate(x.columns):
            ws.write(0, i, c, hdr)
        larg = {"Rank": 6, "Cidade": 15, "Consumo médio (kWh/mês)": 14, "Consumo ano (kWh)": 14,
                "Classe": 12, "Setor": 24, "CNAE": 11, "Descrição CNAE": 40, "Bairro": 24,
                "CEP": 11, "Medidor(es)": 16,
                "Dist. do centro (km)": 10, "Limite da cidade (km)": 10, "Coordenada confiável": 10, "Medidor instalado em": 12, "Grupo tarifário": 9,
                "Tensão (V)": 9, "Carga instalada (kW)": 11, "Ligação em": 11, "Tem GD": 7,
                "Potência GD (kW)": 11, "Área": 7, "UCs no mesmo poste": 10, "Latitude": 12,
                "Longitude": 12, "Google Maps": 34, "COD_ID da UC": 34, "Poste (PN_CON)": 34}
        for i, c in enumerate(x.columns):
            f = None
            if c == "Consumo médio (kWh/mês)":
                f = num
            elif c in ("Consumo ano (kWh)", "Carga instalada (kW)", "Potência GD (kW)"):
                f = num0
            elif c in ("Visitado?", "Nome do local", "Responsável / contato", "Telefone",
                       "Interesse", "Observação"):
                f = anot
            ws.set_column(i, i, larg.get(c, 18), f)
        ws.freeze_panes(1, 2)
        ws.autofilter(0, 0, len(x), len(x.columns) - 1)
        ws.data_validation(1, list(x.columns).index("Visitado?"), len(x),
                           list(x.columns).index("Visitado?"),
                           {"validate": "list", "source": ["Sim", "Não", "Agendado"]})
        ws.data_validation(1, list(x.columns).index("Interesse"), len(x),
                           list(x.columns).index("Interesse"),
                           {"validate": "list", "source": ["Quente", "Morno", "Frio", "Descartar"]})
    print("      " + xls)

    # ---------------- HTML ----------------
    dados = []
    for r in df.itertuples(index=False):
        dados.append({
            "i": int(r.Rank), "lat": round(float(r.LAT_MAPA), 7), "lng": round(float(r.LON_MAPA), 7),
            "la": round(float(r.LAT), 7), "lo": round(float(r.LON), 7),
            "km": round(float(r.KWH_MES), 1), "ka": round(float(r.KWH_ANO), 0),
            "gd": r.Tem_GD, "pg": (None if pd.isna(r.POT_GD) else round(float(r.POT_GD), 1)),
            "cl": r.Classe, "st": r.Setor,
            "cn": ("" if r.CNAE is None or pd.isna(r.CNAE) else str(r.CNAE)),
            "cd": r.CNAE_DESCR,
            "ci": r.Cidade, "br": ("" if pd.isna(r.BRR) else str(r.BRR)),
            "cp": ("" if pd.isna(r.CEP) else str(r.CEP)),
            "md": ("" if r.MEDIDOR is None or pd.isna(r.MEDIDOR) else str(r.MEDIDOR)),
            "gt": ("" if pd.isna(r.GRU_TAR) else str(r.GRU_TAR)),
            "tv": ("" if pd.isna(r.TEN_FORN) else str(r.TEN_FORN)),
            "ck": (None if pd.isna(r.CAR_INST) else round(float(r.CAR_INST), 1)),
            "dc": ("" if pd.isna(r.DAT_CON) else str(r.DAT_CON)),
            "np": int(r.UC_NO_POSTE),
            "ok": (1 if bool(r.COORD_OK) else 0), "dk": float(r.DIST_CENTRO_KM),
        })

    excluidas = bruto - n
    if excluidas > 0:
        nota_mt = (f"Clientes de média tensão foram removidos desta base: {excluidas} UCs cujo mesmo "
                   f"COD_ID também consta na tabela de MT da distribuidora.")
        nota_curta = f"Sem média tensão ({excluidas} UCs removidas)."
    else:
        nota_mt = ("<b style='color:#ffc078'>Atenção:</b> nesta distribuidora o cruzamento de média "
                   "tensão não retorna nada — nenhum COD_ID da tabela de BT aparece na de MT. "
                   "Esta lista <b>não tem</b> a exclusão automática de média tensão que os mapas da "
                   "Energisa têm; confirmar em campo antes de abordar os maiores consumos.")
        nota_curta = "Sem exclusão automática de média tensão nesta distribuidora — ver rodapé."
    teto = int(max(40000, min(df["KWH_MES"].max(), 200000)))
    teto = int(round(teto / 5000.0) * 5000)

    vend = os.path.join(AQUI, "vendor")
    mc_js = open(os.path.join(vend, "markercluster.js"), encoding="utf-8").read()
    mc_css = open(os.path.join(vend, "markercluster.css"), encoding="utf-8").read()

    tpl = open(os.path.join(AQUI, "template_mapa.html"), encoding="utf-8").read()
    html = (tpl.replace("__TITULO__", a.titulo)
               .replace("__MINCONS__", str(int(a.min)))
               .replace("__MAXCONS_FMT__", f"{teto:,}".replace(",", ".") + "+")
               .replace("__MAXCONS__", str(teto))
               .replace("__NOTA_MT_CURTA__", nota_curta)
               .replace("__NOTA_MT__", nota_mt)
               .replace("__NUCS__", str(len(dados)))
               .replace("__MC_CSS__", mc_css)
               .replace("__MC_JS__", mc_js)
               .replace("__DATA__", json.dumps(dados, ensure_ascii=False, separators=(",", ":"))))
    hf = os.path.join(a.docs, f"{a.slug}.html")
    open(hf, "w", encoding="utf-8").write(html)
    print("      " + hf)
    print("\nResumo por cidade:")
    resumo = df.groupby("Cidade").agg(UCs=("Rank", "count"),
                                      kWh_mes_total=("KWH_MES", "sum")).round(0)
    if a.estado:
        print(f"  {len(resumo)} cidades com UCs no recorte — as 15 maiores:")
        print(resumo.sort_values("UCs", ascending=False).head(15).to_string())
    else:
        print(resumo.to_string())

    # manifesto do site (docs/cidades.json) -> alimenta o index.html
    import datetime, json as _json
    man = os.path.join(a.docs, "cidades.json")
    reg = {}
    if os.path.exists(man):
        reg = {c["slug"]: c for c in _json.load(open(man, encoding="utf-8"))}
    reg[a.slug] = {
        "slug": a.slug, "titulo": a.titulo, "uf": a.uf,
        "cidades": ([f"{len(df['Cidade'].unique())} cidades"] if a.estado
                    else [nomes[m] for m in muns]),
        "estado": bool(a.estado), "min": int(a.min),
        "ucs": int(len(df)),
        "excluidas_mt": int(excluidas),
        "kwh_mes": int(df["KWH_MES"].sum()),
        "com_gd": int((df["Tem_GD"] == "Sim").sum()),
        "planilha": "planilhas/" + os.path.basename(xls),
        "atualizado": datetime.date.today().isoformat(),
        "safra": "2024-12-31",
    }
    _json.dump(sorted(reg.values(), key=lambda c: c["titulo"]), open(man, "w", encoding="utf-8"),
               ensure_ascii=False, indent=1)
    print("      " + man)

if __name__ == "__main__":
    main()
