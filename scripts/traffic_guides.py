"""T-31 traffic wave (session 19dbf5e2), merged into build_site.GUIDES.

Six guides aimed at the questions a buyer actually types, written for the six weeks after
publication (Thanksgiving 2026-11-26, Christmas 2026-12-25, the leftover weeks after it).

Rules this file obeys, because the build gate enforces them and the owner's brief demands them:
  * every product figure is read from data/products.json, which carries the listing citation for
    each value. Nothing here was measured, tested, or inferred.
  * every food-safety figure is read from the USDA FSIS Food Thermometers factsheet or the USDA
    safe-temperature chart, both in the source register, quoted rather than paraphrased.
  * no price, no star rating, no review count, no "best".
  * where a listing contradicts itself, both figures appear and neither is chosen.
Kept in a separate module so long HTML blocks never collide with the generator's own quoting.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_usda = json.loads((ROOT / "data" / "usda-temperatures.json").read_text())

# The USDA chart rows, rendered as a table that cites the official page on every row.
_usda_rows = "".join(
    '<tr><th scope="row">%s</th><td>%s</td><td class="src"><a href="%s" rel="noopener noreferrer">'
    'USDA FSIS</a></td></tr>' % (a, b, _usda["source_url"]) for a, b in _usda["rows"])
USDA_TABLE = (
    '<table><caption>USDA safe minimum internal temperatures, from the same chart this site quotes '
    'on every thermometer page (read %s).</caption><thead><tr><th scope="col">Food</th>'
    '<th scope="col">Minimum internal temperature</th><th scope="col">Source</th></tr></thead>'
    '<tbody>%s</tbody></table>' % (_usda["checked"], _usda_rows))

IMG = ('<figure class="guide-figure"><img src="../assets/img/{f}" alt="{alt}" width="1536" '
       'height="1024" loading="lazy"><figcaption>Original illustration made for this site &#8212; '
       'not a photograph of the product, and not Amazon imagery.</figcaption></figure>')


def _img(fname, alt):
    return IMG.format(f=fname, alt=alt)


# Entity-to-character normalisation for the escaped fields happens once, in the generator
# (build_site._guide_chars), so every guide record is treated the same way.

GUIDES = [
    # ------------------------------------------------------------------ 1
    dict(slug="dual-basket-worth-it",
         title="Is a dual-basket air fryer worth it, or are you just buying two baskets?",
         sub="Two zones pay off on exactly one condition. Check it against your own week before "
             "you spend anything on a second drawer.",
         kicker="Buying guide · November 2026",
         products=["P-01", "P-03", "P-02"],
         intro="""Every dual-basket fryer is sold with the same sentence: cook a main and a side at
         the same time. That is a real feature. It is also the only reason the format exists, which
         makes it a strange product to buy when your week does not contain that problem.""",
         verdict="""Buy two baskets if two parts of one dinner have to be ready in the same minute.
         Buy the single 8-quart basket if you cook one thing at a time for more than two people. If
         neither sentence describes your kitchen, the whole format is not your purchase, and the
         simpler one-zone basket on this page is the better gift to yourself.""",
         sections=[
            ("What the format actually buys you",
             """One box, two independent drawers, two timers. On the Chefman 6-quart in this
             category the mechanism is stated rather than implied: the listing describes two
             3-quart baskets, a Sync Finish function and two viewing windows, with a temperature
             range of 200&#8211;450 &#176;F and 120 volts / 1700 watts in its specification table.
             The alternative from the same brand is one 8-quart basket with four presets and no
             window. Same appliance class, opposite philosophy."""),
            ("The one question that decides it",
             """Not capacity. Not wattage. The question is whether you routinely finish two
             components at once. If you cook protein and vegetables as separate runs, two 3-quart
             drawers turn one dinner into one appliance run. If you cook one pot for a household,
             two small drawers are a compromise you paid for: 3 quarts will not hold what 8 quarts
             holds, and you cannot put a full tray of anything in a half-size basket."""),
            ("Where two baskets lose",
             """Three things, all visible on the listing before you buy. First, each drawer is
             half the promise: the dual unit's own Measurements table prints <em>6 liters</em> for
             a box marketed as 6 quarts, while the single-basket unit states 8 quarts flat. Second,
             footprint: 13.38 inches deep and 11.81 inches wide for the dual unit against 12.75
             deep and 13.5 wide for the single basket, so you are trading depth for width rather
             than getting something smaller. Third, weight and handling &#8212; 13.3 pounds against
             12.8, which matters the first time you lift a hot drawer to the sink."""),
            ("&#8220;Sync Finish&#8221; is a feature name, not a measurement",
             """The dual-basket listing names Sync Finish among its functions. What we cannot tell
             you, because the listing text does not say and we have not cooked with the unit, is
             how it behaves when one basket needs four more minutes than the other: whether it
             holds one basket, shortens the other, or finishes both and lets one rest. If that
             behaviour is what you are paying for, it is a question for the manual that arrives in
             the box, not something a review number settles."""),
            ("How to decide in five minutes, without us",
             """Write down the last five dinners you actually cooked. Mark the ones where two
             components needed to be ready together. Two or more out of five: the format is solving
             a problem you have. Zero or one: you want a bigger single basket, or an oven-style
             unit that can hold a whole tray &#8212; the Emeril in this category is 16.9 inches
             deep, which is its own warning label."""),
         ],
         extra="""<table><caption>The count that decides it &#8212; an editorial worksheet, not a
product claim.</caption><thead><tr><th scope="col">Your week looks like</th><th scope="col">What
you are buying</th><th scope="col">The honest verdict</th></tr></thead><tbody>
<tr><th scope="row">Two of you, main + veg, one run</th><td>Two small zones, synced timers</td>
<td>The format exists for this exact case</td></tr>
<tr><th scope="row">A household, one dish at a time</th><td>One 8-quart basket</td>
<td>More usable area in a similar box</td></tr>
<tr><th scope="row">Roast, toast, and something crisp</th><td>Oven-style cavity, 26 quarts
stated</td><td>Different appliance, needs a deeper counter</td></tr>
<tr><th scope="row">You have not cooked since August</th><td>Anything</td>
<td>A preset count will not fix this</td></tr></tbody></table>""" +
         _img("guide-dual-basket.jpg",
              "Two open air fryer drawers side by side on a counter, one with vegetables and one "
              "with protein, both steaming") + """
<div class="panel"><p class="kicker">Keep reading</p><p>Capacity is the next trap:
<a href="capacity-checklist.html">the no-hype capacity checklist</a>. Whether you can be bothered
to clean it is the one after that: <a href="cleanup-counter-space.html">cleanup and counter-space
trade-offs</a>. The wider fork, drawer or door, is
<a href="basket-vs-oven.html">basket or oven-style</a>.</p></div>"""),

    # ------------------------------------------------------------------ 2
    dict(slug="reheating-to-165",
         title="Reheating leftovers is a temperature, not a microwave guess: the 165-degree rule",
         sub="The USDA number for leftovers and casseroles, what a maximum-temperature line on an "
             "air fryer listing does and does not mean, and why this page has no minutes in it.",
         kicker="How-to · Holiday 2026",
         products=["P-04", "P-01", "P-02"],
         intro="""The week after a holiday is the biggest thermometer-selling week of the year, and
         the question is never how crisp the leftover gets. It is whether the middle got hot enough.
         USDA publishes the number; the appliance listing only publishes a range.""",
         verdict="""Reheat leftovers and casseroles to 165 &#176;F, measured in the centre with an
         instrument you have checked, and stir or check in more than one place on anything large or
         irregular. Everything else &#8212; rack position, temperature, how long &#8212; is a
         texture decision, and this site will not dress up a guess as a cook time.""",
         sections=[
            ("The number, and the one exception",
             """USDA's safe minimum internal temperature chart puts <em>leftovers and casseroles</em>
             at 165 &#176;F, the same line it puts poultry and reheated stuffing at. The exception
             worth knowing is ham: a fully cooked ham packaged in a USDA-inspected plant can be
             reheated to 140 &#176;F, and all others go to 165 &#176;F. Those are safety thresholds,
             not quality targets, and no appliance listing on this site is quoted as a source for
             either."""),
            ("The two-hour rule is the half people skip",
             """The FSIS guidance flags perishable food that has sat between 40 &#176;F and
             140 &#176;F for more than two hours. Reheating to 165 does not undo a long afternoon on
             a counter, and nothing in a small hot cavity can. If the plate has been out since the
             toast, the decision was made hours before the appliance was involved."""),
            ("What a temperature range on a listing actually tells you",
             """The ranges we read are settings, not instructions: 200&#8211;450 &#176;F on the
             dual-basket Chefman, 200&#8211;400 &#176;F in its specification table against a stated
             450 &#176;F Hi-Fry option on the 8-quart (that listing contradicts itself and we print
             both), and 75&#8211;500 &#176;F on the Emeril oven-style unit. The low end of a range
             is where a gentle, slow reheat lives; the top end is where you get colour. That is as
             far as the paperwork goes &#8212; which setting reaches 165 in the middle of your dish,
             without drying the edge, is exactly the kind of thing we have not tested."""),
            ("Why there are no minutes on this page",
             """Because a minute is a function of the dish, its density, its starting temperature and
             how much of it you stacked, and because nobody here cooked it. What we will point at is
             the measurement: in a small cavity, check thick portions in more than one place, stir
             halfway, and let a standing time do its work. That is the USDA guidance for large and
             irregular foods, and it survives the loss of the fake precision."""),
            ("What to look for in an appliance if reheating is your real job",
             """Not presets. Usable single-layer area, because food stacked in a second layer steams
             instead of crisping; a window, if you would rather look than open the drawer (the
             dual-basket unit states two viewing windows, the 8-quart states none); and a low end of
             the range gentle enough that the outside does not finish before the middle does."""),
         ],
         extra=USDA_TABLE + """
<table><caption>What the listing gives you, and what it never gives you.</caption><thead><tr>
<th scope="col">Line on the listing</th><th scope="col">Usable for</th><th scope="col">Not usable
for</th></tr></thead><tbody>
<tr><th scope="row">Maximum temperature setting</th><td>Whether the appliance can brown a surface</td>
<td>How long your lasagna takes</td></tr>
<tr><th scope="row">Minimum temperature setting</th><td>Whether a slow, gentle reheat is
possible</td><td>Proof that it will reach 165 &#176;F in the middle</td></tr>
<tr><th scope="row">Stated capacity</th><td>How much fits in one layer</td><td>How many guests it
feeds</td></tr>
<tr><th scope="row">Preset names</th><td>Guessing what the brand expects you to cook</td>
<td>Anything about safety</td></tr></tbody></table>
<div class="panel"><p class="kicker">Pair it with</p><p>The instrument you check with, and how to
know it is telling the truth: <a href="thermometer-ice-test.html">the ice-water test</a>. For the holiday
run-up itself, <a href="holiday-capacity.html">the hosting capacity worksheet</a> and
<a href="holiday-roast-thermometer.html">the roast question</a>.</p></div>"""),

    # ------------------------------------------------------------------ 5
    dict(slug="what-a-certification-line-means",
         title="&#8220;cETL approved&#8221; and &#8220;NIST and NSF&#8221;: what a certification line on a spec sheet really promises",
         sub="Two of the five listings on this site carry a safety-mark line and one carries a "
             "metrology acronym. Here is what each one can and cannot be asked to prove.",
         kicker="Explainer · November 2026",
         products=["P-01", "P-03", "P-04"],
         intro="""A certification line is the most reassuring sentence on a spec sheet and the
         easiest to read as something it does not say. It is a pointer to a document held by
         somebody else. That is the whole promise &#8212; and it is worth more than a stock photo of
         a hologram sticker.""",
         verdict="""Treat every certification line as a claim about a document you have not seen,
         including on this site. What makes it different from a marketing claim is that it can be
         asked for: an NRTL mark has a recognised body behind it, and a certificate has a number. If
         nobody can produce one, the line is a sentence, not evidence.""",
         sections=[
            ("What an NRTL is, in OSHA's words",
             """OSHA's Nationally Recognized Testing Laboratory program &#8220;recognizes private
             sector organizations to perform certification for certain products to ensure that they
             meet the requirements of both the construction and general industry OSHA electrical
             standards.&#8221; Each recognised lab has a scope of test standards it is recognised
             for, and uses its own registered certification mark. After certifying a product, the
             lab authorises the manufacturer to apply that mark; the mark &#8220;signifies that the
             NRTL tested and certified the product, and that the product complies with the
             requirements of one or more appropriate product safety test standards.&#8221;"""),
            ("Which is exactly where the usefulness starts",
             """Because that definition also draws the boundary. A mark speaks to specific test
             standards, within a specific scope, for a specific product. It is not a general
             safety rating, not a quality grade, not a performance claim, and not a government
             endorsement of the appliance on your counter. Two of the listings we read state
             <em>cETL approved</em> among their functions; that is the seller telling you a mark
             exists on the product, and the document behind it lives with the lab and the brand."""),
            ("&#8220;Specification Met: NIST and NSF&#8221; is a different kind of line",
             """On the ThermoMaven listing, the certification text appears in a seller-completed
             field of the listing rather than as a mark moulded into a housing. Our reading of the
             page, dated 2026-11-20, is that this is a self-declared line, and we have not inspected
             a certificate. It is also two different promises in three words. Ask the seller which:
             an accredited certification against a named standard, with a listing you can check, or
             calibration against a reference instrument &#8212; the second is what the phrase
             &#8220;NIST-traceable&#8221; usually describes in instrument catalogues, and it means
             something narrower than a mark."""),
            ("Three questions that cost nothing to ask",
             """Which body issued it; against which standard, by number; and where the record can be
             looked up. A brand that can answer all three has a document. A brand that answers
             &#8220;it is certified, trust us&#8221; has a marketing line, and you are now equipped to
             tell the difference on any listing, including ours."""),
            ("Why this site prints it anyway",
             """Because omitting the line would be its own distortion. The rule we apply to every
             value on these pages is the same rule we would want applied to us: quote the listing,
             date the reading, and say plainly what the source is. Where a listing contradicts
             itself, both numbers stay. Where a claim cannot be checked from an official document,
             it is labelled as the seller's statement and the answer to the deeper question is left
             blank instead of invented."""),
         ],
         extra="""<table><caption>What each kind of line can be asked to prove.</caption><thead><tr>
<th scope="col">Kind of line</th><th scope="col">What a reader can verify</th><th scope="col">What it
cannot tell you</th></tr></thead><tbody>
<tr><th scope="row">A registered mark (the &#8220;cETL approved&#8221; style of line)</th>
<td>Which body issued it and against which standards, from the issuer's records</td>
<td>Anything about how the appliance cooks, or how well it is made</td></tr>
<tr><th scope="row">A certification included in the box (the calibration certificate)</th>
<td>That a document shipped with the unit, and what it says the reference was</td>
<td>Whether the instrument is still in that state after a year in a drawer</td></tr>
<tr><th scope="row">A seller-completed spec field</th><td>That the seller typed it on a given date,
which is what this site's dates are for</td><td>Whether an independent body has ever seen it</td>
</tr></tbody></table>
<div class="panel"><p class="kicker">Sources for this page</p><p>OSHA's description of the NRTL
program is quoted from <a href="https://www.osha.gov/nationally-recognized-testing-laboratory-program"
rel="noopener noreferrer">osha.gov</a>, read 2026-11-20, and quoted
rather than paraphrased. The certification lines this page takes from listings are registered on the
<a href="../sources.html">source register</a>, next to the listing URLs they were read from. This site has not inspected any certificate, and says so
wherever a certificate is mentioned.</p></div>
<div class="panel"><p class="kicker">Where this fits</p><p>This is the same distinction this site
draws about its own numbers, written out on <a href="../how-we-choose.html">how we choose</a> and
tracked on the <a href="../sources.html">source register</a>. The ice-water test in
<a href="thermometer-ice-test.html">the ice-water calibration test</a> is what to do with an instrument when no
document is available.</p></div>"""),

    # ------------------------------------------------------------------ 6
    dict(slug="appliance-gift-checklist",
         title="Gifting an appliance in December: the five checks that decide whether it gets used",
         sub="Counter depth, doors, an app, a battery in the box and a warranty line. All five are "
             "answerable from the listing before you wrap anything.",
         kicker="Gift guide · Holiday 2026",
         products=["P-01", "P-02", "P-04"],
         intro="""Appliances are the gift that either becomes the most-used thing in the kitchen or
         goes back in the box. The difference is rarely the appliance. It is whether the recipient's
         counter, cabinet and habits were measured before it arrived.""",
         verdict="""Check the five lines on this page against the recipient's kitchen, in this order:
         depth, door swing, whether it needs a phone, what comes in the box, and the warranty
         sentence. If you cannot answer all five from the listing, you are gifting a chore.""",
         sections=[
            ("One: depth, not width",
             """Depth is what disqualifies a counter, because the wall, the vent gap and the swing
             all live there. The three units in this category state 13.38 inches, 16.9 inches and
             12.75 inches deep. The 16.9-inch unit opens with French doors, which need room in front
             as well as behind &#8212; a fact that is obvious in a kitchen and invisible on a spec
             sheet."""),
            ("Two: does the gift need a phone?",
             """The CHEF iQ listing states its probes work over Wi-Fi and Bluetooth through the
             CHEF iQ app. For the right person that is the entire value: alerts across a yard, three
             probes, live temperature. For somebody who dislikes pairing devices, it is a gift with
             setup homework, delivered on a day they are busy. The instant-read in this category
             needs no app at all, which is its own kind of thoughtfulness."""),
            ("Three: what is actually in the box",
             """Read the included-components line before you add accessories. The ThermoMaven listing
             lists the thermometer, one AAA battery, a user manual and a calibration certificate, so
             it works on arrival. The Emeril listing's accessories line is where its own page gets
             unclear: the title says six cooking accessories, the configuration and description fields
             say seven, and the included-components list names six. That is not a reason not to buy
             it; it is a reason to expect the box to differ from the page."""),
            ("Four: windows, light, and the thing nobody mentions",
             """Two viewing windows are stated as a feature of the dual-basket unit; the 8-quart
             listing states none. A window is not a performance claim, it is a behaviour change:
             you look instead of opening. If the person you are buying for is the type who opens the
             oven every four minutes, buy the one with the window."""),
            ("Five: the warranty sentence, read exactly",
             """The two Chefman listings state a one-year assurance and a one-year limited warranty.
             The CHEF iQ listing carries two figures on the same page &#8212; a two-year assurance in
             the bullets and a three-year warranty description in the details table &#8212; which we
             print rather than choose between. And the Emeril listing states no warranty line at all
             in the fields we read. A gift receipt outlives a lot of spec sheets; so does a
             screenshot of the page you bought from."""),
         ],
         extra="""<table><caption>The five-line pre-wrap check.</caption><thead><tr>
<th scope="col">Check</th><th scope="col">Where it is on the listing</th><th scope="col">Fail mode
it prevents</th></tr></thead><tbody>
<tr><th scope="row">Depth plus clearance</th><td>Measurements table</td><td>The return queue in
January</td></tr>
<tr><th scope="row">Door or drawer swing</th><td>Title, configuration, images of the mechanism</td>
<td>A counter that cannot open</td></tr>
<tr><th scope="row">App dependency</th><td>Connectivity line in the bullets</td><td>A gift that needs
a tech support call</td></tr>
<tr><th scope="row">Batteries and parts in the box</th><td>Included components</td><td>Present that
does not work on the day</td></tr>
<tr><th scope="row">Warranty wording</th><td>Bullets and item details &#8212; check both</td>
<td>A promise nobody can find afterwards</td></tr></tbody></table>
""" +
         _img("guide-gift-counter.jpg",
              "A wrapped box on a kitchen counter beside an air fryer with two drawers and a folding "
              "thermometer, tape measure resting in front") + """
<div class="panel"><p class="kicker">Why there is no price line here</p><p>Because Amazon's program
policies govern who may display price and availability, this site shows none &#8212; the button on
every product page opens the live listing, where the number is always current. See
<a href="../how-we-choose.html">how we choose</a>. For the fit questions behind this list, read
<a href="small-kitchen-air-fryer.html">measuring for a small kitchen</a> and
<a href="multi-function-questions.html">questions to ask before a multi-function appliance</a>.</p></div>"""),
]


GUIDES.append(dict(slug="first-week-wireless-probe",
     title="First week with a leave-in probe: seven checks before a long cook depends on it",
     sub="Pairing, the alert test across your own house, what a 1000-degree heat-safe figure refers to, and the two numbers one listing cannot agree on.",
     kicker="How-to \u00b7 first week",
     products=["P-05", "P-04"],
     intro="""A leave-in probe is the only cooking instrument that has to work at a distance, on a network, on a battery, while you are somewhere else. That is four chances to fail, and none of them show up in a specification table. So run the whole chain once, this week, with nothing cooking.""",
     verdict="""Do one dry run of the full chain \u2014 pair, place, alert, range, battery \u2014 before a four-hour cook depends on it, and keep a one-second instant-read for the spot checks a leave-in probe is not there to do. A cook is lost to a dropped connection far more often than to a wrong number.""",
     sections=[
       ("Pair it while the table is still clear",
        """The CHEF iQ Sense listing states its probes work over Wi-Fi and Bluetooth through the CHEF iQ app, and the kit is three probes plus a hub. That is the setup to do on a quiet evening, not at four o'clock with a brisket already in. What the app asks for \u2014 account, firmware, which device is the hub \u2014 is not something this site has run hands-on, so treat the manual as the authority and treat this page as the checklist that says: do it before the day it matters."""),
       ("What stays in the food, and what does not",
        """USDA's own table of thermometer types describes wireless and smart models as designed to remain in the food while it cooks, giving live status, and calling for the sensing point at least an inch deep in the thickest part. The listing for this kit states the probes are heat safe to 1000 &#176;F. That is a rating of the probe, and this page will not tell you what the hub, its cable or its battery can take. That is a manual question, and it is the one people skip."""),
       ("Test the alert, not just the number",
        """Set a target a long way below what you will actually cook to, leave the phone in the room you will really be sitting in, and walk the probe away from the hub. You are measuring three things no listing states: how long the alert takes to arrive, whether it arrives at all past the far wall, and what happens when it drops and reconnects. Write down the worst spot in your house. That distance, not the marketing range, is the size of your cook."""),
       ("The battery, and the two figures on one page",
        """The listing carries two numbers for the same object: an About-this-item line stating up to 50 hours on a full charge, and 70 hours recorded on an earlier read of the same page. Both are printed on this site rather than quietly averaged, because choosing between them would be inventing a fact. Practically, it changes one habit: charge before a long cook rather than after."""),
       ("The ambient sensor is the one people ignore",
        """Five sensors is what the listing states: four internal and one ambient. The ambient channel is the difference between \u201cmy food is at 145\u201d and \u201cmy cooker is losing heat, so my food will be late\u201d. Before the long cook, find out what your app actually does with that channel \u2014 graph, alert, or nothing \u2014 because a sensor you never read is a spec you paid for."""),
       ("What an instant-read still does that this cannot",
        """A leave-in probe watches one joint in one place. The instant-read in this category states a one-second read, no app, no network, no pairing, and a wipe-clean body, which is what you want when you are checking four chicken breasts, a burger and the thickest part of a chop inside thirty seconds. The two instruments are not rivals; one is a lookout, the other is a question you ask a drawer."""),
       ("Care, where the seller and the agency pull differently",
        """The kit's listing states its probes are waterproof and dishwasher-safe. USDA's general care guidance for food thermometers is that most should not be immersed and should be washed by hand, and warns that faces and plastics can be damaged by heat. Neither statement is wrong about the other's product: one is a specific claim about specific parts, the other is general advice for the category. Read the manual that arrives, because that is the document a warranty refers to."""),
     ],
     extra="""<table><caption>A seven-day dry run. Nothing here is a cook time \u2014 there are no cook times on this site because nobody here cooked.</caption><thead><tr><th scope="col">Day</th><th scope="col">Check</th><th scope="col">What to write down</th></tr></thead><tbody>
<tr><th scope="row">1</th><td>Pair probes and hub on the kitchen table</td><td>Which probe maps to which channel, and how long setup took</td></tr>
<tr><th scope="row">2</th><td>Alert test from the room you actually sit in</td><td>Seconds until the phone notices, and the worst distance that still works</td></tr>
<tr><th scope="row">3</th><td>Drop and recover: hub off, then on</td><td>Whether a missed alert re-sends or is simply gone</td></tr>
<tr><th scope="row">4</th><td>Placement practice on a cold roast</td><td>Where the thickest part is, clear of bone, fat and gristle</td></tr>
<tr><th scope="row">5</th><td>Charge, then note the figure you will plan against</td><td>The lower of the two numbers on the listing, deliberately</td></tr>
<tr><th scope="row">6</th><td>Find the ambient channel in the app</td><td>Graph, alert, or absent</td></tr>
<tr><th scope="row">7</th><td>Care check against the manual</td><td>What may be rinsed, what may not, and what voids nothing</td></tr></tbody></table>
<div class="panel"><p class="kicker">Run the number first</p><p>A probe that drifts tells you nothing useful at any distance, so before the seven days are out, do the calibration check the USDA publishes: <a href="thermometer-ice-test.html">the ice-water test</a>. For the long-cook question this instrument answers, see <a href="holiday-roast-thermometer.html">when a wireless probe earns its keep</a>, and <a href="instant-vs-wireless.html">which type for which cook</a>.</p></div>"""))


def _decode(g):
    """The generator escapes the fields a reader sees first (title, sub, kicker, intro, verdict
    and every section heading). An entity stored in one of those is escaped again, so the page
    prints `&#8220;` where a quote mark belongs. Decode at the source, in the record, so no
    renderer has to remember to do it. Raw section bodies and `extra` are HTML and are left alone.
    """
    import html as _h

    def fix(v):
        prev = None
        while v != prev:
            prev, v = v, _h.unescape(v)
        return v
    for k in ("title", "sub", "kicker", "intro", "verdict"):
        if g.get(k):
            g[k] = fix(g[k])
    if g.get("sections"):
        g["sections"] = [(fix(h), t) for h, t in g["sections"]]
    return g


GUIDES = [_decode(g) for g in GUIDES]
