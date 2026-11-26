#!/usr/bin/env python3
"""HundeWissenTv – einfaches Magazin-Video (ruhige Bilder, 3 Szenen + Logo-Schluss) aus einer Beschreibung bauen.

Aufruf: python3 hundewissen/bau_einfach.py <name>   (Daten unten in VIDEOS)
Regeln (Nutzer 16.11.): keine Wackel-/Bewegungs-Effekte am Hund, kein Fortschrittsbalken, ruhigeres Tempo,
Schluss immer mit großem Logo + „Folg uns für mehr“.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
T = [(0.0, 4.2), (4.2, 8.4), (8.4, 12.4)]  # Szenenzeiten
SCHLUSS = 12.4
DUR = 15

VIDEOS = {
    "hw-f-schokolade": [
        dict(h="Schokolade ist <i>giftig</i> für Hunde.", size=104, pose="bettelnd", ph=580,
             caps=["dein hund bettelt um <b>schokolade</b>?", "bitte <b>niemals</b> geben"]),
        dict(h="Schuld ist der Stoff <i>Theobromin.</i>", size=100, pose="ueberrascht", ph=560, px=690,
             extra='<div class="chip x" style="top:1000px">🍫 je dunkler,</div><div class="chip x" style="top:1130px">desto gefährlicher</div>',
             caps=["schuld ist <b>theobromin</b>", "dunkle schokolade ist <b>am schlimmsten</b>"]),
        dict(h="Hat er genascht? <i>Sofort zum Tierarzt.</i>", size=96, pose="zeigend", ph=560,
             caps=["hat er doch genascht?", "dann <b>sofort zum tierarzt</b>"]),
    ],
    "hw-f-schlaf": [
        dict(h="Dein Hund schläft <i>ständig?</i>", size=112, pose="gaehnend", ph=580,
             caps=["schläft dein hund <b>den ganzen tag</b>?", "das ist <b>völlig normal</b>"]),
        dict(h="Erwachsene Hunde: <i>12 bis 14 Stunden.</i>", size=100, pose="schlafend", ph=440,
             caps=["erwachsene hunde schlafen", "<b>12 bis 14 stunden</b> am tag"]),
        dict(h="Welpen sogar <i>bis zu 20.</i>", size=112, pose="rueckenlage", ph=380,
             caps=["welpen schlafen", "sogar <b>noch viel mehr</b>"]),
    ],
    "hw-f-kopfschief": [
        dict(h="Warum legt er den Kopf <i>schief?</i>", size=104, pose="verwirrt", ph=580,
             caps=["dein hund legt den kopf <b>schief</b>?", "das hat einen <b>grund</b>"]),
        dict(h="Er hört <i>ganz genau hin.</i>", size=112, pose="brille", ph=580, src="Studie: Universität Budapest (2022)",
             caps=["er will dich <b>besser verstehen</b>", "vor allem bei wörtern, die er <b>kennt</b>"]),
        dict(h="Sag mal <i>„Gassi“</i> – und schau hin!", size=104, pose="freudig", ph=560,
             caps=["probier's aus: sag mal <b>gassi</b>", "und achte auf <b>seinen kopf</b>"]),
    ],
    "hw-f-dunkel": [
        dict(h="Im Dunkeln sieht er <i>besser als du.</i>", size=104, pose="stolz", ph=560,
             caps=["im dunkeln sieht dein hund", "<b>viel besser</b> als du"]),
        dict(h="Sein Auge hat einen <i>Licht-Spiegel.</i>", size=104, pose="ueberrascht", ph=580,
             caps=["hinter der netzhaut sitzt ein <b>spiegel</b>", "der das restlicht <b>verstärkt</b>"]),
        dict(h="Dafür sieht er <i>weniger Farben.</i>", size=104, pose="rennend", ph=440,
             caps=["dafür sieht er <b>weniger farben</b>", "aber <b>bewegung</b> erkennt er super"]),
    ],
    "hw-g-zaehne": [
        dict(h="Putzt du deinem Hund <i>die Zähne?</i>", size=104, pose="zahnbuerste", ph=560,
             caps=["putzt du deinem hund <b>die zähne</b>?", "das solltest du <b>unbedingt</b>"]),
        dict(h="Die meisten haben mit 3 Jahren <i>Zahnprobleme.</i>", size=92, pose="krank", ph=400, src="Tierärzte-Verband AVMA",
             caps=["die meisten hunde haben mit 3 jahren", "schon <b>probleme mit den zähnen</b>"]),
        dict(h="Nur <i>Hunde-Zahnpasta</i> nehmen!", size=104, pose="aufmerksam", ph=580, px=700,
             extra='<div class="chip x" style="top:1000px">❌ Menschen-Zahnpasta</div><div class="chip x" style="top:1130px">✅ Hunde-Zahnpasta</div>',
             caps=["nimm nie <b>deine eigene</b> zahnpasta", "sondern <b>spezielle für hunde</b>"]),
    ],
    "hw-g-schuldblick": [
        dict(h="Fühlt er sich <i>wirklich schuldig?</i>", size=104, pose="schuldig", ph=580,
             caps=["kennst du diesen <b>blick</b>?", "als hätte er ein <b>schlechtes gewissen</b>"]),
        dict(h="Er reagiert auf <i>deine Stimme.</i>", size=104, pose="aufmerksam", ph=580, src="Studie: Barnard College, New York (2009)",
             caps=["forscher sagen: er reagiert", "auf <b>deinen ärger</b>, nicht auf schuld"]),
        dict(h="Schimpfen danach <i>bringt nichts.</i>", size=104, pose="traurig", ph=540,
             caps=["schimpfen im nachhinein", "<b>versteht er nicht</b>"]),
    ],
    "hw-g-winterpfoten": [
        dict(h="Schnee macht Spaß – <i>aber Vorsicht!</i>", size=100, pose="schnee", ph=520,
             caps=["schnee macht <b>riesig spaß</b>", "aber pass auf <b>seine pfoten</b> auf"]),
        dict(h="Streusalz <i>reizt die Pfoten.</i>", size=110, pose="pfoetchen", ph=580,
             caps=["streusalz kann die pfoten", "<b>wund und rissig</b> machen"]),
        dict(h="Nach dem Gassi: <i>Pfoten abspülen.</i>", size=100, pose="badewanne", ph=480,
             caps=["darum nach dem gassi", "die pfoten mit <b>warmem wasser</b> abspülen"]),
    ],
    "hw-g-buddeln": [
        dict(h="Warum buddelt er <i>ständig Löcher?</i>", size=100, pose="buddeln", ph=540,
             caps=["buddelt dein hund <b>ständig löcher</b>?", "dafür gibt es <b>gründe</b>"]),
        dict(h="Oft steckt <i>Langeweile</i> dahinter.", size=104, pose="gelangweilt", ph=380,
             extra='<div class="chip x" style="top:860px">🦴 Etwas verstecken</div><div class="chip x" style="top:990px">😎 Kühler Liegeplatz</div>',
             caps=["er versteckt etwas, sucht kühle", "oder ihm ist <b>einfach langweilig</b>"]),
        dict(h="Mehr Spielen hilft <i>am besten.</i>", size=104, pose="ball", ph=560,
             caps=["mehr <b>spielen und schnüffeln</b>", "dann buddelt er <b>weniger</b>"]),
    ],
    "hw-s1-problem": [
        dict(h="Ist dein Hund ein <i>Schnellfresser?</i>", size=104, pose="schlingt", ph=560,
             caps=["ist sein napf in sekunden <b>leer</b>?", "dann frisst er <b>zu schnell</b>"]),
        dict(h="Er schluckt dabei <i>viel Luft.</i>", size=110, pose="themen/magen-luft", ph=560,
             caps=["beim schlingen schluckt er <b>viel luft</b>", "der bauch <b>bläht sich auf</b>"]),
        dict(h="Die Folge: <i>Bauchweh.</i>", size=110, pose="aufgeblaeht", ph=600,
             caps=["das kann <b>bauchweh</b> machen", "oder er <b>würgt</b> alles wieder hoch"]),
        dict(h="Im schlimmsten Fall: <i>Magendrehung.</i>", size=96, pose="themen/magen-verdreht", ph=540, px=480,
             bilder=[("themen/warnung", 220, 850, 820)],
             caps=["im schlimmsten fall dreht sich <b>der magen</b>", "vor allem bei <b>großen hunden</b>"]),
        dict(h="Das ist ein <i>Notfall!</i>", size=116, pose="themen/tierarzt-koffer", ph=330, px=830,
             extra='<div class="chip x" style="top:880px">🎈 Dicker Bauch</div><div class="chip x" style="top:1010px">🤢 Würgen ohne Erbrechen</div><div class="chip x" style="top:1140px">😰 Unruhe</div>',
             caps=["bei diesen zeichen sofort", "<b>zum tierarzt</b> – jede minute zählt"]),
        dict(h="Die Lösung: <i>langsamer fressen.</i>", size=104, pose="antischling-frisst", ph=560,
             caps=["ein <b>anti-schling-napf</b> hilft", "so frisst er <b>ganz entspannt</b>"]),
    ],
    "hw-s2-tipps": [
        dict(h="5 Tipps gegen <i>Schlingen.</i>", size=116, pose="schlingt", ph=560,
             caps=["dein hund <b>schlingt</b> sein futter?", "diese <b>5 tipps</b> helfen"]),
        dict(h="Tipp 1: <i>Anti-Schling-Napf.</i>", size=100, pose="themen/antischling-napf", ph=380,
             caps=["die rillen im napf", "<b>bremsen</b> ihn beim fressen"]),
        dict(h="Tipp 2: <i>Schnüffelteppich.</i>", size=100, pose="schnueffelteppich-frisst", ph=540,
             caps=["im schnüffelteppich muss er", "jedes stück <b>erst suchen</b>"]),
        dict(h="Tipp 3: <i>Muffinblech.</i>", size=110, pose="themen/muffinblech", ph=340,
             caps=["futter ins <b>muffinblech</b> verteilen", "der <b>günstige trick</b> von zuhause"]),
        dict(h="Tipp 4: <i>Kleinere Portionen.</i>", size=100, pose="themen/portionen", ph=520,
             caps=["lieber <b>2 bis 3 kleine</b> mahlzeiten", "statt einer <b>großen</b>"]),
        dict(h="Tipp 5: <i>Ruhe nach dem Fressen.</i>", size=96, pose="wartet-napf", ph=600,
             caps=["nach dem fressen <b>kein toben</b>", "lieber <b>ausruhen</b> lassen"]),
    ],
    "hw-s3-test": [
        dict(h="Mach den <i>Schnellfresser-Test!</i>", size=100, pose="themen/stoppuhr", ph=520,
             caps=["mach mal einen <b>kleinen test</b>", "es dauert nur <b>eine minute</b>"]),
        dict(h="Napf füllen, <i>Uhr starten.</i>", size=110, pose="themen/napf-voll", ph=360,
             bilder=[("themen/stoppuhr", 260, 850, 780)],
             caps=["füll seinen napf <b>wie immer</b>", "und starte <b>die uhr</b>"]),
        dict(h="In Sekunden fertig? <i>Schnellfresser!</i>", size=96, pose="schlingt", ph=560,
             caps=["ist er nach <b>wenigen sekunden</b> fertig?", "dann ist er ein <b>schnellfresser</b>"]),
        dict(h="Achte auf <i>diese Zeichen.</i>", size=110, pose="wuergt", ph=520, px=790,
             extra='<div class="chip x" style="top:900px">🤢 Würgt oft</div><div class="chip x" style="top:1030px">💨 Viele Pupse</div><div class="chip x" style="top:1160px">🎈 Bläht sich auf</div>',
             caps=["würgt er oft oder <b>pupst</b> viel?", "auch das sind <b>hinweise</b>"]),
        dict(h="Mach Fressen <i>zum Spiel.</i>", size=110, pose="themen/futterball", ph=440,
             bilder=[("themen/schnueffelteppich", 240, 830, 860)], px=380,
             caps=["mit <b>futterball</b> oder", "<b>schnüffelteppich</b> wird's ein spiel"]),
        dict(h="So frisst er <i>gesund.</i>", size=116, pose="antischling-frisst", ph=560,
             caps=["so frisst er <b>langsamer</b>", "und viel <b>gesünder</b>"]),
    ],

    "hw-p1-schnellfresser": [
        dict(h='Dein Hund frisst in <i>10 Sekunden?</i>', size=104, pose='schlingt', ph=560, caps=['ist sein napf nach <b>10 sekunden</b> leer?', 'dann solltest du <b>jetzt aufpassen</b>']),
        dict(h='Schlingen ist <i>gefährlicher,</i> als du denkst.', size=96, pose='themen/warnung', ph=420, caps=['schlingen ist <b>gefährlicher</b> als gedacht', 'am ende zeig ich dir <b>die lösung</b>']),
        dict(h='Er schluckt dabei <i>viel Luft.</i>', size=110, pose='themen/magen-luft', ph=560, caps=['beim schlingen schluckt er <b>viel luft</b>', 'der bauch <b>bläht sich auf</b>'], infos=[('Luft + Futter = <b>Blähbauch</b>', 70, 830), ('Magen dehnt sich <b>stark</b>', 560, 1050), ('Kann <b>Schmerzen</b> machen', 70, 1270)]),
        dict(h='Die Folge: <i>Bauchweh.</i>', size=116, pose='aufgeblaeht', ph=600, caps=['das kann richtig <b>bauchweh</b> machen', 'und er fühlt sich <b>unwohl</b>']),
        dict(h='Oder er <i>würgt</i> alles wieder hoch.', size=100, pose='wuergt', ph=580, caps=['oft würgt er das futter', '<b>gleich wieder hoch</b>']),
        dict(h='Im schlimmsten Fall: <i>Magendrehung.</i>', size=96, pose='themen/magen-verdreht', ph=540, caps=['im schlimmsten fall dreht sich <b>der magen</b>', 'das ist <b>lebensgefährlich</b>'], px=470, bilder=[('themen/warnung', 210, 850, 830)], infos=[('Magen <b>dreht sich</b>', 60, 1190), ('Blut wird <b>abgeschnürt</b>', 560, 1130), ('Nur eine <b>OP</b> hilft', 600, 1290)]),
        dict(h='Das ist ein <i>Notfall!</i>', size=116, pose='themen/tierarzt-koffer', ph=330, caps=['bei diesen zeichen sofort', '<b>zum tierarzt</b> – jede minute zählt'], px=830, extra='<div class="chip x" style="top:880px">🎈 Dicker Bauch</div><div class="chip x" style="top:1010px">🤢 Würgen ohne Erbrechen</div><div class="chip x" style="top:1140px">😰 Unruhe</div>'),
        dict(h='Besonders gefährdet: <i>große Hunde.</i>', size=100, pose='stolz', ph=580, caps=['große hunde mit <b>tiefer brust</b>', 'haben das <b>höchste risiko</b>']),
        dict(h='Lösung 1: <i>Anti-Schling-Napf.</i>', size=96, pose='antischling-frisst', ph=560, caps=['die rillen im napf', '<b>bremsen</b> ihn beim fressen'], shop='Den Anti-Schling-Napf'),
        dict(h='Lösung 2: <i>Schnüffelteppich.</i>', size=96, pose='schnueffelteppich-frisst', ph=540, caps=['im schnüffelteppich muss er', 'jedes stück <b>erst suchen</b>'], shop='Den Schnüffelteppich'),
        dict(h='Lösung 3: <i>Kleinere Portionen.</i>', size=96, pose='themen/portionen', ph=520, caps=['lieber <b>2 bis 3 kleine</b> mahlzeiten', 'statt einer <b>großen</b>']),
        dict(h='Nach dem Fressen: <i>Ruhe.</i>', size=110, pose='korb', ph=420, caps=['nach dem fressen <b>kein toben</b>', 'lieber <b>ausruhen</b> lassen']),
        dict(h='So frisst er <i>gesund.</i>', size=116, pose='wartet-napf', ph=600, caps=['so frisst er <b>langsam</b>', 'und bleibt <b>gesund</b>']),
    ],
    "hw-p2-test": [
        dict(h='Schlingt dein Hund? <i>Mach den Test!</i>', size=100, pose='themen/stoppuhr', ph=520, caps=['wie schnell frisst <b>dein hund</b>?', 'mach jetzt diesen <b>einfachen test</b>']),
        dict(h="Viele Hunde schlingen – <i>keiner merkt's.</i>", size=96, pose='gierig', ph=540, caps=['viele hunde schlingen <b>unbemerkt</b>', 'am ende verrat ich dir, <b>was hilft</b>']),
        dict(h='Napf füllen, <i>Uhr starten.</i>', size=110, pose='themen/napf-voll', ph=360, caps=['füll seinen napf <b>wie immer</b>', 'und starte <b>die uhr</b>'], bilder=[('themen/stoppuhr', 260, 850, 780)]),
        dict(h='In Sekunden leer? <i>Schnellfresser!</i>', size=100, pose='schlingt', ph=560, caps=['ist er nach <b>wenigen sekunden</b> fertig?', 'dann ist er ein <b>schnellfresser</b>']),
        dict(h='Zeichen 1: <i>Er würgt oft.</i>', size=110, pose='wuergt', ph=580, caps=['würgt er oft', '<b>nach dem fressen</b>?']),
        dict(h='Zeichen 2: <i>Dicker Bauch.</i>', size=110, pose='aufgeblaeht', ph=600, caps=['ist sein bauch danach', '<b>dick und prall</b>?']),
        dict(h='Zeichen 3: <i>Er bettelt sofort weiter.</i>', size=96, pose='bettelnd', ph=580, caps=['bettelt er direkt', '<b>um mehr futter</b>?']),
        dict(h='Darum ist das <i>gefährlich.</i>', size=110, pose='themen/magen-luft', ph=560, caps=['er schluckt dabei <b>viel luft</b>', 'im schlimmsten fall <b>dreht sich der magen</b>'], infos=[('Luft + Futter = <b>Blähbauch</b>', 70, 830), ('Magen dehnt sich <b>stark</b>', 560, 1050), ('Im Notfall: <b>Magendrehung</b>', 70, 1270)]),
        dict(h='Tipp 1: <i>Muffinblech.</i>', size=116, pose='themen/muffinblech', ph=340, caps=['futter ins <b>muffinblech</b> verteilen', 'der <b>günstige trick</b> von zuhause']),
        dict(h='Tipp 2: <i>Futterball.</i>', size=116, pose='themen/futterball', ph=460, caps=['im futterball muss er', 'sich jedes stück <b>erarbeiten</b>'], shop='Den Futterball'),
        dict(h='Tipp 3: <i>Anti-Schling-Napf.</i>', size=100, pose='themen/antischling-napf', ph=380, caps=['die rillen im napf', '<b>bremsen</b> ihn beim fressen'], shop='Den Anti-Schling-Napf'),
        dict(h='Tipp 4: <i>Futter suchen lassen.</i>', size=96, pose='schnueffelteppich-frisst', ph=540, caps=['futter im <b>schnüffelteppich</b> verstecken', 'das macht ihn <b>langsam und satt</b>'], shop='Den Schnüffelteppich'),
        dict(h='Ruhig fressen = <i>gesund fressen.</i>', size=96, pose='antischling-frisst', ph=560, caps=['so frisst er <b>langsamer</b>', 'und viel <b>gesünder</b>']),
    ],
    "hw-schnellfresser-teil1": [
        dict(h='Dein Hund frisst in <i>10 Sekunden?</i>', size=104, pose='schlingt', ph=560, caps=[]),
        dict(h='Schlingen ist <i>gefährlicher,</i> als du denkst.', size=96, pose='themen/warnung', ph=420, caps=[]),
        dict(h='Schlingt deiner <i>auch?</i>', size=116, pose='gierig', ph=520, caps=[]),
        dict(h='Teil 1: <i>Die Gefahr beim Schlingen.</i>', size=96, pose='aufmerksam', ph=600, caps=[]),
        dict(h='Er schluckt dabei <i>viel Luft.</i>', size=110, pose='themen/magen-luft', ph=480, px=790, caps=[], infos=[('Luft + Futter = <b>Blähbauch</b>', 60, 900), ('Bläht sich auf wie ein <b>Ballon</b>', 60, 1060), ('Kann <b>Schmerzen</b> machen', 60, 1220)]),
        dict(h='Die Folge: <i>Bauchweh.</i>', size=116, pose='aufgeblaeht', ph=560, px=770, caps=[], infos=[('<b>Blähungen</b>', 60, 1000), ('Fühlt sich <b>unwohl</b>', 60, 1160)]),
        dict(h='Oft würgt er <i>alles wieder hoch.</i>', size=100, pose='wuergt', ph=580, caps=[]),
        dict(h='Im schlimmsten Fall: <i>Magendrehung.</i>', size=96, pose='themen/magen-verdreht', ph=480, px=790, caps=[], infos=[('Magen <b>dreht sich</b>', 60, 900), ('Blut wird <b>abgeschnürt</b>', 60, 1060), ('Nur eine <b>OP</b> hilft', 60, 1220)]),
        dict(h='Besonders gefährdet: <i>große Hunde.</i>', size=100, pose='themen/dogge', ph=600, px=340, caps=[], bilder=[('themen/schaeferhund', 500, 770, 900)], infos=[('<b>Doggen</b>', 120, 1420), ('<b>Schäferhunde</b>', 640, 1420)]),
        dict(h='Achte auf diese <i>Notfall-Zeichen.</i>', size=100, pose='zittert', ph=380, px=540, caps=[], extra='<div class="chip x" style="top:700px">🎈 Dicker, harter Bauch</div><div class="chip x" style="top:810px">🤢 Würgen, aber nichts kommt</div><div class="chip x" style="top:920px">😰 Große Unruhe</div>'),
        dict(h='Jede Minute zählt: <i>sofort zum Tierarzt!</i>', size=96, pose='themen/tierarzt-koffer', ph=420, caps=[]),
        dict(h='In Teil 2: <i>So frisst er langsamer.</i>', size=96, pose='antischling-frisst', ph=580, caps=[]),
    ],
    "hw-schnellfresser-teil2": [
        dict(h='Dein Hund <i>schlingt?</i>', size=120, pose='schlingt', ph=560, caps=[]),
        dict(h='Teil 2: <i>5 Tipps gegen Schlingen.</i>', size=100, pose='zeigend', ph=600, caps=[]),
        dict(h='Schick das Video <i>weiter!</i>', size=110, pose='freudig', ph=520, caps=[]),
        dict(h='Tipp 1: <i>Anti-Schling-Napf.</i>', size=100, pose='antischling-frisst', ph=580, caps=[]),
        dict(h='Gibt\'s in <i>unserem Shop!</i>', size=110, pose='themen/shop-antischling-napf', ph=380, caps=[], shop='Den Anti-Schling-Napf'),
        dict(h='Tipp 2: <i>Schnüffelteppich.</i>', size=100, pose='themen/shop-schnueffelteppich', ph=360, caps=[], shopbtn=True, infos=[('Futter mit der <b>Nase</b> suchen', 60, 760), ('Macht <b>langsam</b> und müde', 560, 760)]),
        dict(h='Tipp 3: <i>Muffinblech.</i>', size=116, pose='themen/muffinblech', ph=320, caps=[], infos=[('<b>0 €</b> – hast du schon zuhause', 270, 760)]),
        dict(h='Tipp 4: <i>Kleinere Portionen.</i>', size=100, pose='themen/portionen', ph=480, caps=[], infos=[('<b>2–3</b> kleine statt <b>1</b> große', 260, 740)]),
        dict(h='Tipp 5: <i>Ruhe nach dem Fressen.</i>', size=96, pose='korb', ph=350, px=770, caps=[], infos=[('Mind. <b>1 Stunde</b> kein Toben', 60, 1040), ('Schont den <b>Magen</b>', 60, 1180)]),
        dict(h='Welchen Tipp <i>probierst du?</i>', size=104, pose='nachdenken', ph=540, caps=[]),
        dict(h='In Teil 3: <i>Der große Test.</i>', size=104, pose='themen/stoppuhr', ph=480, caps=[]),
    ],
}

# Kommentar-Aufruf am Ende der letzten Szene: (getippter Text, Banner)
KOMMENTAR = {
    "hw-schnellfresser-teil2": ("Ich probier Tipp 3!", "WELCHER TIPP? <b>AB IN DIE KOMMENTARE</b>"),
    "hw-schnellfresser-teil1": ("Meiner schlingt auch!", "SCHREIB'S IN DIE <b>KOMMENTARE</b>"),
    "hw-p1-schnellfresser": ("Meiner schlingt auch!", "SCHREIB'S IN DIE <b>KOMMENTARE</b>"),
    "hw-p2-test": ("Meiner braucht 20 Sekunden", "WIE SCHNELL IST DEINER? <b>KOMMENTIER!</b>"),
    "hw-s1-problem": ("Meiner schlingt auch!", "SCHREIB'S IN DIE <b>KOMMENTARE</b>"),
    "hw-s2-tipps": ("Tipp 3 probier ich aus!", "WELCHER TIPP? <b>AB IN DIE KOMMENTARE</b>"),
    "hw-s3-test": ("Meiner braucht 20 Sekunden", "WIE SCHNELL IST DEINER? <b>KOMMENTIER!</b>"),
}
KOM_DAUER = 4.2
UNTERTITEL = False  # Nutzer 24.11.: ab sofort keine Untertitel
# Hinweis: Produkt gibt's im Shop-Kanal (nur bei Produkten, die dort wirklich verkauft werden)
SHOP = ('<div class="shop"><img src="assets/beagle.png" alt="" /><span>🛒 Gibt\'s bei uns!<small>HundeWissenTv 2.0</small></span></div>')
# Logo-Intro nach der ersten Szene (Hook), 3 s, mit Jingle wie HundeFinanzTv
INTRO = {"hw-s1-problem", "hw-s2-tipps", "hw-s3-test", "hw-p1-schnellfresser", "hw-p2-test"}
INTRO_DAUER = 3.0
INTRO_TAG = "GESUNDHEIT <i>|</i> VERHALTEN <i>|</i> ERZIEHUNG"  # Nutzer 24.11.


def kommentar_html(text):
    z = "".join(f'<span class="tz">{"&nbsp;" if c == " " else c}</span>' for c in text)
    return (f'<div id="co"><div class="t1">Kommentare</div><div class="row"><div class="av"><img src="assets/beagle.png" alt="" /></div>'
            f'<div class="in">{z}<span id="co-cur"></span></div></div><div class="bt"><span class="ab">Abbrechen</span><span id="co-btn">Kommentieren</span></div></div>'
            '<div id="co-z"><svg viewBox="0 0 24 24" style="width:100%;height:100%;filter:drop-shadow(0 4px 6px #0006)"><path d="M4 2 L4 20 L9 15.5 L12.5 23 L15.5 21.6 L12 14.3 L19 14 Z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg></div>')


def infos_html(sz):
    out = ""
    for k, (txt, x, y) in enumerate(sz.get("infos", [])):
        out += f'<div class="info info{k}" style="left:{x}px;top:{y}px">{txt}</div>'
    return out


def shopk(sz):
    if not sz.get("shop"):
        return ""
    ding = sz["shop"] if isinstance(sz["shop"], str) else "Das"
    return (f'<div class="shopk"><img src="assets/beagle.png" alt="" /><div>🛒 {ding} gibt\'s in unserem Shop!'
            f'<small>👇 Link in der Beschreibung · HundeWissenTv 2.0</small></div></div>')


def sfx(ziel, dur, tick_at, pops):
    import numpy as np, soundfile as sf
    sr = 44100; y = np.zeros(int(sr * dur) + sr); rng = np.random.default_rng(3)
    def tick(t, lv, f):
        i = int(t * sr); L = int(0.03 * sr); e = np.exp(-np.arange(L) / (0.004 * sr))
        y[i:i + L] += lv * e * (0.6 * rng.standard_normal(L) + np.sin(2 * np.pi * f * np.arange(L) / sr))
    def plopp(t):  # kurzer, weicher Plopp (Ton fällt schnell ab)
        i = int(t * sr); L = int(0.12 * sr); tt = np.arange(L) / sr
        f = 900 * np.exp(-tt * 28) + 180
        y[i:i + L] += 0.8 * np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 30)
    if tick_at:
        a, n = tick_at
        for k in range(n): tick(a + 0.5 + k * 0.08, 0.25, 1800 + 300 * (k % 3))
        tick(a + 0.5 + n * 0.08 + 0.9, 0.6, 900)
    for t in pops: plopp(t)
    y = y[: int(sr * dur)]
    sf.write(ziel, (y / max(1e-6, np.abs(y).max()) * 0.5).astype("float32"), sr)


def kommentar_sound(ziel, dur, a, n):
    import numpy as np, soundfile as sf
    sr = 44100; y = np.zeros(int(sr * dur)); rng = np.random.default_rng(3)
    def tick(t, lv, f):
        i = int(t * sr); L = int(0.03 * sr); e = np.exp(-np.arange(L) / (0.004 * sr))
        y[i:i + L] += (lv * e * (0.6 * rng.standard_normal(L) + np.sin(2 * np.pi * f * np.arange(L) / sr)))[: len(y[i:i + L])]
    for k in range(n): tick(a + 0.5 + k * 0.08, 0.25, 1800 + 300 * (k % 3))
    tick(a + 0.5 + n * 0.08 + 0.9, 0.6, 900)
    sf.write(ziel, (y / max(1e-6, np.abs(y).max()) * 0.5).astype("float32"), sr)

# Videos mit Stimme: Zeiten je Szene (aus hundewissen/plan_voice.py)
PLAENE = {}
_pl = ROOT / "hundewissen" / "plaene.json"
if _pl.exists():
    import json as _j
    PLAENE = _j.loads(_pl.read_text())

HTML = """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/magazin.css" />
    <style>
      .h {{ text-align: center; }}
      .pose {{ position: absolute; filter: drop-shadow(0 26px 30px #00000030); }}
      .shadow {{ position: absolute; height: 40px; border-radius: 50%; background: radial-gradient(#0000002a, transparent 70%); }}
      .chip {{ position: absolute; left: 80px; padding: 16px 34px 20px; border-radius: 40px; background: #fbf8f2; border: 2px solid #1d1b1922; box-shadow: 0 14px 30px #0000001a; font-weight: 800; font-size: 44px; }}
      .call {{ position: absolute; padding: 14px 30px 18px; border-radius: 40px; background: #fbf8f2; border: 2px solid #1d1b1922; box-shadow: 0 14px 30px #0000001a; font-weight: 800; font-size: 40px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{SCENES}
{CAPS}
      <div id="logo"><img src="assets/beagle.png" alt="" /></div>
      <div id="name">HundeWissenTv</div>
      <div id="cta"><div class="ring"><img src="assets/beagle.png" alt="" /></div><div class="n">HundeWissenTv</div><div class="pill"><span>+ Folgen</span></div></div>
{KOM}
      <div id="grain"></div>
      <div id="frame"></div>
    </div>
    <script>
      const DUR = {DUR};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
    <script src="assets/magazin.js"></script>
    <script>
      kopf2();
{JS}
{KOMJS}
      schluss({SCHLUSS});
      tl.to({{}}, {{ duration: 0.01 }}, DUR - 0.01);
    </script>
  </body>
</html>
"""


def bildpfad(n):
    return ROOT / "brand" / (f"{n}.png" if "/" in n else f"aussie/{n}.png")


def bau(name):
    d = ROOT / "videos" / name
    if not d.exists():
        subprocess.run(["bash", str(ROOT / "hundewissen/neu.sh"), name], check=True)
    for f in ["magazin.css", "magazin.js"]:
        (d / "assets" / f).write_bytes((ROOT / "hundewissen/magazin" / f).read_bytes())
    (d / "assets/themen").mkdir(exist_ok=True)
    sz_list = VIDEOS[name]
    plan = PLAENE.get(name)
    kom = KOMMENTAR.get(name)
    if plan:  # mit Stimme: Zeiten kommen aus der Sprachaufnahme
        zeiten, t_intro, schluss, dur = plan["zeiten"], plan.get("t_intro"), plan["schluss"], plan["dur"]
    else:
        if len(sz_list) == 3:
            zeiten, schluss, dur = T, SCHLUSS, DUR
        else:  # längere Videos: je Szene 4,5 s, Schluss 3 s
            zeiten, t = [], 0.0
            for sz in sz_list:
                l = 4.5 + sz.get("plus", 2.5 if sz.get("infos") else 0) + (1.5 if sz.get("shop") else 0)
                zeiten.append((round(t, 2), round(t + l, 2))); t += l
            schluss = zeiten[-1][1]; dur = schluss + 3
        t_intro = None
        if name in INTRO and len(zeiten) > 1:
            t_intro = zeiten[0][1]
            zeiten = [zeiten[0]] + [(round(a + INTRO_DAUER, 2), round(b + INTRO_DAUER, 2)) for a, b in zeiten[1:]]
            schluss += INTRO_DAUER; dur += INTRO_DAUER
        if kom:
            schluss += KOM_DAUER; dur += KOM_DAUER
    def img(n):
        if "/" in n:
            (d / "assets" / f"{n}.png").write_bytes(bildpfad(n).read_bytes())
            return f"assets/{n}.png"
        return f"assets/aussie/{n}.png"
    scenes, caps, js, pops = [], [], [], []
    for i, (sz, (a, b)) in enumerate(zip(sz_list, zeiten), 1):
        w0, h0 = Image.open(bildpfad(sz["pose"])).size
        ph = sz["ph"]; pw = round(w0 * ph / h0)
        if pw > 860: pw = 860; ph = round(h0 * pw / w0)
        cx = sz.get("px", 540); top = 1400 - ph
        src = f'<div class="src" style="top:{1418 if UNTERTITEL else 1700}px">{sz["src"]}</div>' if sz.get("src") else ""
        mehr = ""
        for (bn, bh, bx, by) in sz.get("bilder", []):
            bw0, bh0 = Image.open(bildpfad(bn)).size; bw = round(bw0 * bh / bh0)
            mehr += f'<img class="pose x" src="{img(bn)}" style="left:{bx - bw / 2:.0f}px;top:{by}px;width:{bw}px" alt="" />'
        scenes.append(f'''      <div id="s{i}" class="scene">
        <div id="h{i}" class="h" style="top: 470px; font-size: {sz["size"]}px">{sz["h"]}</div>
        <div style="position:absolute;inset:0;transform:translateY({0 if UNTERTITEL else 100}px)">
        <div class="shadow" style="left:{cx - pw * 0.42:.0f}px;top:1378px;width:{pw * 0.84:.0f}px"></div>
        <img id="p{i}" class="pose" src="{img(sz["pose"])}" style="left:{cx - pw / 2:.0f}px;top:{top}px;width:{pw}px" alt="" />
        <div id="x{i}">{sz.get("extra", "")}{mehr}</div>{infos_html(sz)}</div>{src}{shopk(sz)}{SHOP if sz.get("shopbtn") else ""}
      </div>''')
        m = round((a + b) / 2, 2)
        for k, (c, ca, cb) in enumerate(zip(sz["caps"] if UNTERTITEL else [], [a, m], [m, b])):
            caps.append(f'      <div id="k{i}{k}" class="cap">{c}</div>')
            js.append(f'      show("#k{i}{k}", {ca}, {cb});')
        js.append(f'      up("#h{i}", {a + 0.25}, 0.6);')
        js.append(f'      tl.fromTo("#p{i}", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }}, {a + 0.5});')
        if sz.get("shop"):
            ts = b - 2.6
            js.append(f'      tl.fromTo("#s{i} .shopk", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {ts});')
            pops.append(ts)
        if sz.get("shopbtn"):
            js.append(f'      tl.fromTo("#s{i} .shop", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.5)" }}, {a + 1.2});')
            pops.append(a + 1.2)
        for k, _ in enumerate(sz.get("infos", [])):
            ti = a + 1.6 + k * 0.9
            js.append(f'      tl.fromTo("#s{i} .info{k}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(3)" }}, {ti:.2f});')
            pops.append(ti)
        js.append(f'      tl.fromTo("#x{i} .x", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, stagger: 0.35, ease: "power3.out" }}, {a + 1.4});')
    if plan:
        sc = [f'["#s{i}", {a}, {b if i < len(zeiten) else schluss + 0.2}]' for i, (a, b) in enumerate(zeiten, 1)]
    else:
        sc = [f'["#s{i}", {a}, {(t_intro if (t_intro and i == 1) else b) if i < len(zeiten) else schluss + 0.2}]' for i, (a, b) in enumerate(zeiten, 1)]
    js.insert(0, f'      scenes([{", ".join(sc)}]);')
    komhtml = komjs = ""; tick_at = None
    if kom:
        ka = plan["ka"] if plan and "ka" in plan else zeiten[-1][1] + 0.2; n = len(kom[0])
        komhtml = "      " + kommentar_html(kom[0]) + f'<div id="co-bn"><span>{kom[1]}</span></div>'
        tick_at = (ka, n)
        komjs = f"      kommentar({ka}, {n});"
    if tick_at or pops:
        sfx(d / "assets/cta.wav", dur, tick_at, pops)
        komhtml += f'\n      <audio id="ctasnd" src="assets/cta.wav" data-start="0" data-duration="{dur}" data-track-index="5" data-volume="0.7"></audio>'
    if plan:
        komhtml += f'\n      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{dur}" data-track-index="4"></audio>'
        if plan.get("teil"):
            komhtml += f'\n      <div id="teil">{plan["teil"]}</div>'
        if plan.get("teilen"):
            komhtml += f'\n      <div id="teilen"><span>📤 Teile das Video mit Freunden!</span></div>'
            komjs += f'\n      teilen({plan["teilen"]});'
    if t_intro is not None:
        (d / "assets/logo-jingle.mp3").write_bytes((ROOT / "hundewissen/magazin/logo-jingle.mp3").read_bytes())
        komhtml += (f'\n      <div id="ls-bg"></div><div id="ls-ring"></div><div id="ls-logo"><img src="assets/beagle.png" alt="" /></div>'
                    f'<div id="ls-txt"><div id="ls-name">HundeWissen<b>Tv</b></div><div id="ls-tag">{INTRO_TAG}</div></div>'
                    f'\n      <audio id="jingle" src="assets/logo-jingle.mp3" data-start="{t_intro + 0.05}" data-duration="2.5" data-track-index="6"></audio>')
        komjs = f"      logoIntro({t_intro}, {INTRO_DAUER});\n" + komjs
    (d / "index.html").write_text(HTML.format(DUR=dur, SCENES="\n".join(scenes), CAPS="\n".join(caps), JS="\n".join(js), SCHLUSS=schluss, KOM=komhtml, KOMJS=komjs))
    print("gebaut:", d)

if __name__ == "__main__":
    for n in sys.argv[1:] or VIDEOS:
        bau(n)
