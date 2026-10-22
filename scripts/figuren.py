"""Wiederverwendbare SVG-Figuren für die Videos.

aussie(): der feste Kanal-Hund (Australian Shepherd, blue merle, Vorlage: brand/aussie-referenz.png),
sitzend von vorn. Bellen: das Element mit id "<prefix>-open" ein-/ausblenden (Opacity).
"""

GREY, DARK, LIGHT, WHITE, COPPER, AMBER, INK = "#8e979c", "#2d3236", "#b9c0c4", "#f7f4ef", "#b8642a", "#c98a2c", "#1a1a1a"


def aussie(prefix, style="width:100%;height:100%", extra=""):
    return f'''<svg viewBox="0 0 300 370" style="{style}" {extra}>
  <ellipse cx="150" cy="352" rx="110" ry="14" fill="#000" opacity="0.08" />
  <path d="M68 348 Q58 250 95 192 L205 192 Q242 250 232 348 Z" fill="{GREY}" />
  <path d="M74 300 Q80 248 100 228 Q112 270 96 322 Z" fill="{DARK}" />
  <ellipse cx="214" cy="282" rx="14" ry="32" fill="{DARK}" />
  <ellipse cx="200" cy="225" rx="10" ry="8" fill="{LIGHT}" />
  <path d="M112 188 Q150 218 188 188 Q204 262 180 348 L120 348 Q96 262 112 188 Z" fill="{WHITE}" />
  <path d="M102 196 Q112 214 122 204 Q130 226 142 212 Q150 234 158 212 Q170 226 178 204 Q188 214 198 196 Q170 186 150 190 Q130 186 102 196 Z" fill="{WHITE}" />
  <rect x="110" y="268" width="32" height="84" rx="15" fill="{WHITE}" stroke="#ddd6cb" stroke-width="3" />
  <rect x="158" y="268" width="32" height="84" rx="15" fill="{WHITE}" stroke="#ddd6cb" stroke-width="3" />
  <path d="M116 300 Q126 296 136 300" stroke="{COPPER}" stroke-width="4" fill="none" opacity="0.6" />
  <path d="M164 300 Q174 296 184 300" stroke="{COPPER}" stroke-width="4" fill="none" opacity="0.6" />
  <path d="M74 100 Q56 52 84 30 Q112 34 128 64 Z" fill="{DARK}" />
  <path d="M84 30 Q108 26 122 50 Q104 58 96 70 Q86 52 84 30 Z" fill="#1f2326" />
  <path d="M226 100 Q244 52 216 30 Q188 34 172 64 Z" fill="{DARK}" />
  <path d="M216 30 Q192 26 178 50 Q196 58 204 70 Q214 52 216 30 Z" fill="#454c51" />
  <ellipse cx="150" cy="116" rx="82" ry="74" fill="{GREY}" />
  <path d="M74 104 Q90 66 128 78 Q132 122 102 140 Q78 130 74 104 Z" fill="{DARK}" />
  <ellipse cx="200" cy="72" rx="16" ry="10" fill="{LIGHT}" />
  <ellipse cx="218" cy="128" rx="10" ry="14" fill="{DARK}" />
  <ellipse cx="106" cy="146" rx="18" ry="13" fill="{COPPER}" />
  <ellipse cx="194" cy="146" rx="18" ry="13" fill="{COPPER}" />
  <path d="M140 44 Q150 39 160 44 L168 110 Q202 138 192 170 Q150 198 108 170 Q98 138 132 110 Z" fill="{WHITE}" />
  <ellipse cx="114" cy="88" rx="10" ry="6" fill="{COPPER}" />
  <ellipse cx="186" cy="88" rx="10" ry="6" fill="{COPPER}" />
  <circle cx="117" cy="110" r="14" fill="{AMBER}" /><circle cx="117" cy="111" r="7.5" fill="{INK}" /><circle cx="121" cy="106" r="3.2" fill="#fff" />
  <circle cx="183" cy="110" r="14" fill="{AMBER}" /><circle cx="183" cy="111" r="7.5" fill="{INK}" /><circle cx="187" cy="106" r="3.2" fill="#fff" />
  <ellipse cx="150" cy="150" rx="18" ry="12" fill="{INK}" />
  <ellipse cx="144" cy="146" rx="5" ry="3" fill="#fff" opacity="0.35" />
  <path d="M150 162 Q150 172 139 176 M150 162 Q150 172 161 176" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" />
  <g id="{prefix}-open" opacity="0">
    <path d="M130 166 Q150 212 170 166 Q150 174 130 166 Z" fill="#5a1f1f" />
    <path d="M139 182 Q150 204 161 182 Q150 188 139 182 Z" fill="#e88a9a" />
  </g>
</svg>'''
