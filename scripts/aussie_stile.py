G, D, L, W, C, A, I = "#8e979c", "#2d3236", "#b9c0c4", "#f7f4ef", "#b8642a", "#c98a2c", "#1a1a1a"

# 1) Niedlich (Chibi): großer Kopf, große Augen, kleiner Körper
chibi = f'''<svg viewBox="0 0 300 330" width="100%" height="100%">
<ellipse cx="150" cy="318" rx="90" ry="10" fill="#000" opacity=".08"/>
<ellipse cx="150" cy="268" rx="78" ry="58" fill="{G}"/>
<path d="M110 222 Q150 250 190 222 Q200 290 175 322 L125 322 Q100 290 110 222Z" fill="{W}"/>
<ellipse cx="118" cy="312" rx="22" ry="14" fill="{W}"/><ellipse cx="182" cy="312" rx="22" ry="14" fill="{W}"/>
<path d="M52 92 Q28 150 58 178 Q80 150 86 104Z" fill="{D}"/>
<path d="M248 92 Q272 150 242 178 Q220 150 214 104Z" fill="{D}"/>
<circle cx="150" cy="128" r="104" fill="{G}"/>
<path d="M60 110 Q76 58 128 66 Q134 132 96 160 Q62 148 60 110Z" fill="{D}"/>
<ellipse cx="214" cy="70" rx="20" ry="12" fill="{L}"/><ellipse cx="236" cy="150" rx="12" ry="18" fill="{D}"/>
<ellipse cx="96" cy="170" rx="22" ry="15" fill="{C}"/><ellipse cx="204" cy="170" rx="22" ry="15" fill="{C}"/>
<path d="M138 26 Q150 22 162 26 L168 118 Q214 150 200 196 Q150 226 100 196 Q86 150 132 118Z" fill="{W}"/>
<ellipse cx="108" cy="92" rx="12" ry="7" fill="{C}"/><ellipse cx="192" cy="92" rx="12" ry="7" fill="{C}"/>
<circle cx="110" cy="124" r="24" fill="{A}"/><circle cx="110" cy="126" r="14" fill="{I}"/><circle cx="118" cy="116" r="7" fill="#fff"/><circle cx="102" cy="132" r="3" fill="#fff"/>
<circle cx="190" cy="124" r="24" fill="{A}"/><circle cx="190" cy="126" r="14" fill="{I}"/><circle cx="198" cy="116" r="7" fill="#fff"/><circle cx="182" cy="132" r="3" fill="#fff"/>
<ellipse cx="150" cy="168" rx="16" ry="11" fill="{I}"/>
<path d="M136 184 Q150 200 164 184" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>
<ellipse cx="86" cy="186" rx="12" ry="7" fill="#f2a0a8" opacity=".6"/><ellipse cx="214" cy="186" rx="12" ry="7" fill="#f2a0a8" opacity=".6"/>
</svg>'''

# 2) Seitenansicht sitzend (Clipart wie Finanzbär-Videos)
seite = f'''<svg viewBox="0 0 320 330" width="100%" height="100%">
<ellipse cx="160" cy="318" rx="120" ry="10" fill="#000" opacity=".08"/>
<path d="M70 318 Q40 250 80 190 Q110 150 170 160 Q200 200 196 318Z" fill="{G}"/>
<path d="M80 230 Q95 200 120 205 Q118 250 96 280Z" fill="{D}"/><ellipse cx="150" cy="250" rx="16" ry="26" fill="{D}"/>
<ellipse cx="96" cy="300" rx="44" ry="22" fill="{G}"/><ellipse cx="80" cy="314" rx="26" ry="9" fill="{W}"/>
<path d="M150 150 Q200 150 214 200 Q222 260 206 318 L176 318 Q186 250 160 210Z" fill="{W}"/>
<path d="M186 230 L190 318 L210 318 L206 232Z" fill="{W}" stroke="#ddd6cb" stroke-width="3"/>
<path d="M196 296 Q202 292 208 296" stroke="{C}" stroke-width="4" fill="none"/>
<path d="M150 60 Q190 40 222 66 Q246 82 270 92 Q290 100 286 118 Q280 134 252 134 Q230 140 214 150 Q180 176 152 150 Q130 120 150 60Z" fill="{G}"/>
<path d="M152 66 Q174 52 196 64 Q196 110 170 132 Q150 120 152 66Z" fill="{D}"/>
<path d="M214 78 Q240 86 270 94 Q288 102 284 118 Q276 132 250 132 Q226 138 214 150 Q206 112 214 78Z" fill="{W}"/>
<ellipse cx="236" cy="128" rx="16" ry="10" fill="{C}"/>
<ellipse cx="284" cy="104" rx="11" ry="9" fill="{I}"/>
<path d="M258 128 Q268 136 280 128" stroke="{I}" stroke-width="3" fill="none"/>
<circle cx="222" cy="92" r="10" fill="{A}"/><circle cx="224" cy="93" r="5.5" fill="{I}"/><circle cx="226" cy="90" r="2.4" fill="#fff"/>
<ellipse cx="218" cy="76" rx="8" ry="4" fill="{C}"/>
<path d="M164 56 Q166 20 196 26 Q206 40 196 62Z" fill="{D}"/><path d="M180 28 Q200 24 204 40 Q196 44 190 50Z" fill="#1f2326"/>
<path d="M140 170 Q150 200 170 196 Q160 220 178 226" fill="none" stroke="{W}" stroke-width="10" stroke-linecap="round"/>
</svg>'''

# 3) Comic/Sticker mit dicken Konturen
O = 'stroke="#1a1a1a" stroke-width="6" stroke-linejoin="round"'
comic = f'''<svg viewBox="0 0 300 340" width="100%" height="100%">
<path d="M76 330 Q66 240 100 196 L200 196 Q234 240 224 330Z" fill="{G}" {O}/>
<path d="M118 196 Q150 220 182 196 Q196 262 176 330 L124 330 Q104 262 118 196Z" fill="{W}" {O}/>
<path d="M86 300 Q88 252 104 232 Q112 268 100 312Z" fill="{D}"/>
<rect x="114" y="270" width="30" height="64" rx="14" fill="{W}" {O}/><rect x="156" y="270" width="30" height="64" rx="14" fill="{W}" {O}/>
<path d="M70 104 Q50 50 84 30 Q114 38 128 66Z" fill="{D}" {O}/>
<path d="M230 104 Q250 50 216 30 Q186 38 172 66Z" fill="{D}" {O}/>
<path d="M68 118 Q66 40 150 40 Q234 40 232 118 Q232 196 150 200 Q68 196 68 118Z" fill="{G}" {O}/>
<path d="M76 110 Q92 70 128 82 Q130 124 100 140 Q78 132 76 110Z" fill="{D}"/>
<ellipse cx="198" cy="72" rx="16" ry="9" fill="{L}"/>
<ellipse cx="104" cy="150" rx="18" ry="12" fill="{C}"/><ellipse cx="196" cy="150" rx="18" ry="12" fill="{C}"/>
<path d="M140 46 Q150 42 160 46 L168 112 Q202 140 192 172 Q150 198 108 172 Q98 140 132 112Z" fill="{W}" stroke="#1a1a1a" stroke-width="4"/>
<circle cx="116" cy="112" r="16" fill="{A}" {O}/><circle cx="117" cy="113" r="8" fill="{I}"/><circle cx="121" cy="108" r="3.5" fill="#fff"/>
<circle cx="184" cy="112" r="16" fill="{A}" {O}/><circle cx="185" cy="113" r="8" fill="{I}"/><circle cx="189" cy="108" r="3.5" fill="#fff"/>
<ellipse cx="150" cy="152" rx="18" ry="12" fill="{I}"/>
<path d="M132 168 Q150 196 168 168" fill="#5a1f1f" {O}/><path d="M142 178 Q150 196 158 178Z" fill="#e88a9a"/>
</svg>'''

# 4) Porträt (Kopf + Schultern, mehr Fell-Details, nah am Foto)
portrait = f'''<svg viewBox="0 0 300 330" width="100%" height="100%">
<path d="M30 330 Q40 230 100 210 L200 210 Q260 230 270 330Z" fill="{G}"/>
<path d="M40 330 Q50 260 90 236 Q96 290 80 330Z" fill="{D}"/><path d="M250 330 Q246 270 214 240 Q206 290 224 330Z" fill="{D}"/>
<path d="M90 214 Q150 250 210 214 Q232 270 214 330 L86 330 Q68 270 90 214Z" fill="{W}"/>
<path d="M92 218 l10 22 l10 -18 l10 22 l10 -18 l10 22 l8 -20 l8 20 l10 -22 l10 18 l10 -22 l10 18 l10 -22" fill="none" stroke="#e7e1d6" stroke-width="5" stroke-linejoin="round"/>
<path d="M58 96 Q44 44 76 22 Q108 26 124 58Z" fill="{D}"/><path d="M76 22 Q100 18 116 40 Q100 50 92 62Z" fill="#1f2326"/>
<path d="M242 96 Q256 44 224 22 Q192 26 176 58Z" fill="{D}"/><path d="M224 22 Q200 18 184 40 Q200 50 208 62Z" fill="#454c51"/>
<path d="M60 120 Q56 50 150 46 Q244 50 240 120 Q246 170 214 196 Q182 222 150 222 Q118 222 86 196 Q54 170 60 120Z" fill="{G}"/>
<path d="M60 120 Q64 70 106 64 Q124 80 126 112 Q120 150 92 166 Q62 154 60 120Z" fill="{D}"/>
<path d="M190 60 Q222 64 236 92 Q222 100 204 90Z" fill="{D}"/><ellipse cx="226" cy="146" rx="12" ry="18" fill="{D}"/>
<ellipse cx="178" cy="70" rx="10" ry="6" fill="{L}"/><ellipse cx="88" cy="190" rx="10" ry="6" fill="{L}"/>
<path d="M78 150 Q100 140 122 158 Q116 186 96 192 Q76 178 78 150Z" fill="{C}"/>
<path d="M222 150 Q200 140 178 158 Q184 186 204 192 Q224 178 222 150Z" fill="{C}"/>
<path d="M142 50 Q150 46 158 50 L166 124 Q204 150 196 186 Q176 214 150 214 Q124 214 104 186 Q96 150 134 124Z" fill="{W}"/>
<ellipse cx="112" cy="100" rx="11" ry="6" fill="{C}"/><ellipse cx="188" cy="100" rx="11" ry="6" fill="{C}"/>
<ellipse cx="114" cy="122" rx="15" ry="13" fill="{A}"/><circle cx="114" cy="123" r="7" fill="{I}"/><circle cx="118" cy="118" r="3" fill="#fff"/>
<path d="M98 118 Q114 106 130 118" stroke="{I}" stroke-width="3" fill="none"/>
<ellipse cx="186" cy="122" rx="15" ry="13" fill="{A}"/><circle cx="186" cy="123" r="7" fill="{I}"/><circle cx="190" cy="118" r="3" fill="#fff"/>
<path d="M170 118 Q186 106 202 118" stroke="{I}" stroke-width="3" fill="none"/>
<path d="M132 160 Q150 152 168 160 Q170 176 150 180 Q130 176 132 160Z" fill="{I}"/>
<ellipse cx="143" cy="162" rx="6" ry="3" fill="#fff" opacity=".35"/>
<path d="M150 180 L150 192 Q140 200 128 196 M150 192 Q160 200 172 196" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
</svg>'''

cells = [("A · Niedlich", chibi), ("B · Comic mit Kontur", comic), ("C · Porträt", portrait)]
html = '<html><body style="margin:0;background:#fff;font-family:sans-serif;display:grid;grid-template-columns:repeat(3,400px)">'
for t, s in cells:
    html += f'<div style="padding:20px;text-align:center"><div style="height:420px">{s}</div><div style="font-size:30px;font-weight:700;margin-top:10px">{t}</div></div>'
open(__file__.replace("stile.py", "stile.html"), "w").write(html + "</body></html>")
