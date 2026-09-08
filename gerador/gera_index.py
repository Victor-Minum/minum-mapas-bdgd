# -*- coding: utf-8 -*-
"""Reconstroi docs/index.html a partir de docs/cidades.json. Rode depois de cada cidade nova."""
import json, os, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(AQUI), "docs")

cid = json.load(open(os.path.join(DOCS, "cidades.json"), encoding="utf-8"))
br = lambda n: f"{n:,}".replace(",", ".")

def card(c):
    return f'''
      <a class="card" href="{c['slug']}.html">
        <h3>{c['titulo']}</h3>
        <div class="big">{br(c['ucs'])}<span> UCs no funil</span></div>
        <div class="kv"><span>Consumo somado</span><b>{br(round(c['kwh_mes']/1000))} MWh/mês</b></div>
        <div class="kv"><span>Corte aplicado</span><b>≥ {br(c['min'])} kWh/mês</b></div>
        <div class="kv"><span>Cidades com UCs</span><b>{c['cidades'][0] if c.get('estado') else len(c['cidades'])}</b></div>
        <div class="kv"><span>Já tinham GD</span><b>{br(c['com_gd'])}</b></div>
        <div class="ft">Safra {c['safra']} · atualizado em {datetime.date.fromisoformat(c['atualizado']).strftime('%d/%m/%Y')}
          &nbsp;·&nbsp; <span class="xls" data-x="{c['planilha']}">planilha .xlsx</span></div>
      </a>'''

est = [c for c in cid if c.get("estado")]
rec = [c for c in cid if not c.get("estado")]
blocos = ""
if est:
    blocos += '<h2 class="grupo">Estados inteiros</h2><div class="grid">' + "\n".join(card(c) for c in est) + '</div>'
if rec:
    blocos += '<h2 class="grupo">Recortes por cidade</h2><div class="grid">' + "\n".join(card(c) for c in rec) + '</div>'
cards = blocos

tot_ucs = sum(c["ucs"] for c in cid)
tot_kwh = sum(c["kwh_mes"] for c in cid)

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Mapas de consumo BDGD — Minum</title>
<style>
  :root{{--bg:#0f1720;--panel:#161f2b;--ink:#e8eef5;--mut:#9fb0c3;--line:#2a3644;--acc:#4da3ff}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
       font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.55}}
  .wrap{{max-width:960px;margin:0 auto;padding:48px 20px 80px}}
  h1{{font-size:26px;margin:0 0 8px}}
  .sub{{color:var(--mut);font-size:14.5px;margin:0 0 28px;max-width:64ch}}
  .stats{{display:flex;gap:28px;flex-wrap:wrap;padding:16px 20px;background:var(--panel);
         border:1px solid var(--line);border-radius:12px;margin-bottom:32px}}
  .stats div{{font-size:13px;color:var(--mut)}}
  .stats b{{display:block;font-size:22px;color:var(--ink);font-weight:650}}
  .grupo{{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);
         margin:34px 0 14px;font-weight:600}}
  .grupo:first-of-type{{margin-top:0}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
  .card{{display:block;background:var(--panel);border:1px solid var(--line);border-radius:12px;
        padding:18px 20px;text-decoration:none;color:inherit;transition:border-color .15s,transform .15s}}
  .card:hover{{border-color:var(--acc);transform:translateY(-2px)}}
  .card h3{{margin:0 0 10px;font-size:16px}}
  .big{{font-size:30px;font-weight:700;color:var(--acc);margin-bottom:12px}}
  .big span{{font-size:13px;font-weight:400;color:var(--mut)}}
  .kv{{display:flex;justify-content:space-between;font-size:13px;color:var(--mut);padding:2px 0}}
  .kv b{{color:var(--ink);font-weight:600}}
  .ft{{margin-top:12px;padding-top:10px;border-top:1px solid var(--line);font-size:11.5px;color:var(--mut)}}
  .xls{{color:var(--acc);font-weight:600}}
  .nota{{margin-top:36px;padding:16px 20px;border:1px solid var(--line);border-radius:12px;
        font-size:13px;color:var(--mut)}}
  .nota b{{color:var(--ink)}}
  code{{background:#0b121a;padding:1px 5px;border-radius:4px;font-size:12px}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Mapas de consumo de energia — BDGD/ANEEL</h1>
  <p class="sub">Unidades consumidoras de <b>baixa tensão</b> de alto consumo, por cidade, a partir da
     Base de Dados Geográfica da Distribuidora. Cada mapa permite filtrar por setor, classe, consumo e
     geração distribuída, e localizar uma UC pelo <b>código do medidor</b> que aparece na fatura.</p>
  <div class="stats">
    <div>Recortes publicados<b>{len(cid)}</b></div>
    <div>UCs no funil<b>{br(tot_ucs)}</b></div>
    <div>Consumo mapeado<b>{br(round(tot_kwh/1000))} MWh/mês</b></div>
  </div>
  {cards}
  <div class="nota">
    <b>Sobre os dados.</b> Fonte: BDGD/ANEEL, safra 31/12/2024 — dado público, sem CNPJ, nome ou
    titular. A coordenada é a do <b>poste de conexão</b>, não da fachada: prova proximidade, não
    titularidade. O consumo é o que passou pelo medidor, então quem já tem geração própria aparece
    com consumo residual. Clientes de <b>média tensão</b> são removidos da base: quando o mesmo
    <code>COD_ID</code> aparece também na tabela de MT, é o mesmo cliente registrado nas duas —
    Grupo A, fora do modelo de geração compartilhada.
  </div>
</div>
<script>
document.querySelectorAll('.xls').forEach(function(e){{
  e.addEventListener('click',function(ev){{ev.preventDefault();ev.stopPropagation();
    window.location.href=e.dataset.x;}});
}});
</script>
</body>
</html>
'''
open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(html)
print("gravado:", os.path.join(DOCS, "index.html"), "-", len(cid), "cidade(s)")
