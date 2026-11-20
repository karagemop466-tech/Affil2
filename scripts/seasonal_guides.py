"""Holiday 2026 seasonal guide records (session bba2deed), merged into build_site.GUIDES.
Kept in a separate module so long HTML blocks never collide with the generator's own quoting."""
import json
import pathlib

_usda = json.loads((pathlib.Path(__file__).resolve().parent.parent / "data" / "usda-temperatures.json").read_text())
_rows = "".join(
    '<tr><th scope="row">%s</th><td>%s</td><td class="src"><a href="%s" rel="noopener noreferrer">USDA FSIS</a></td></tr>'
    % (a, b, _usda["source_url"]) for a, b in _usda["rows"])
USDA_TABLE = ('<table><caption>USDA Safe Minimum Internal Temperatures. Every row cites the '
              '<a href="%s" rel="noopener noreferrer">official USDA FSIS chart</a> (source %s, read %s).</caption>'
              '<thead><tr><th scope="col">Food</th><th scope="col">Minimum internal temperature</th>'
              '<th scope="col">Source</th></tr></thead><tbody>%s</tbody></table>'
              % (_usda["source_url"], _usda["source_id"], _usda["checked"], _rows))

EXTRA_CAPACITY = """<table><caption>An editorial planning grid &#8212; not a product claim. Adjust to your recipes.</caption>
<thead><tr><th scope="col">Guests</th><th scope="col">Air-fried dishes</th><th scope="col">What usually works</th></tr></thead>
<tbody><tr><th scope="row">2&#8211;4</th><td>1&#8211;2 sides</td><td>One basket-class unit handles it in 1&#8211;2 batches</td></tr>
<tr><th scope="row">4&#8211;6</th><td>2&#8211;3 dishes</td><td>Dual-basket units shine: main + side on synced timers</td></tr>
<tr><th scope="row">6&#8211;10</th><td>3&#8211;4 dishes, or a roast</td><td>Oven-style capacity, or dual baskets plus your wall oven</td></tr>
<tr><th scope="row">10+</th><td>Appetiser parade</td><td>Station cooking: one appliance crisps all evening in waves</td></tr></tbody></table>
<p><img src="../assets/img/guide-holiday-hosting.jpg" alt="Platter of crisp appetisers beside a countertop air fryer in warm holiday light" loading="lazy"></p>
<h2>The pre-holiday checklist</h2>
<ul class="tight">
<li>Measure your counter <em>with clearance</em> &#8212; French doors swing, baskets slide out, vents need air.</li>
<li>Write the batch worksheet above before you shop. The right size is whatever makes the minutes work.</li>
<li>Decide: crisp-while-the-oven-roasts (dual basket) or replace-the-oven for some dishes (oven-style)?</li>
<li>Read what &ldquo;dishwasher-safe parts&rdquo; actually promises on the listing &#8212; it is not the same as &ldquo;easy to clean&rdquo;.</li>
</ul>
<div class="panel"><p class="kicker">Season</p><p>This is part of the Holiday 2026 cluster. The other half: <a href="holiday-roast-thermometer.html">the holiday roast question</a>. For the single-basket question, see the <a href="air-fryer-thanksgiving.html">Thanksgiving fit guide</a> and the <a href="first-week-air-fryer.html">first-week guide</a>.</p></div>"""

EXTRA_ROAST = USDA_TABLE + """
<h2>Probe placement &#8212; the five-minute skill</h2>
<ul class="tight">
<li>Thickest part of the muscle, not touching bone, fat pockets, or the pan.</li>
<li>For poultry: the deepest part of the thigh, avoiding bone; the breast reads cooler and is where guests judge you.</li>
<li>For roasts: aim for the geometric centre of the thickest muscle.</li>
<li>Trust the number over the clock &#8212; ovens lie, roasts vary, and the USDA chart is the standard, not the recipe.</li>
</ul>
<p><img src="../assets/img/guide-roast.jpg" alt="A holiday roast with a wireless thermometer probe inserted, resting on a carving board" loading="lazy"></p>
<div class="panel"><p class="kicker">Season</p><p>Part of the Holiday 2026 cluster &#8212; the other half is <a href="holiday-capacity.html">the capacity worksheet</a>. The listings referenced above carry open contradictions (battery claims, warranty wording) that are published on the <a href="../flagged.html">Flagged for Review</a> page rather than smoothed over.</p></div>"""

GUIDES = [
    dict(slug="holiday-capacity",
         title="Holiday hosting: how much air fryer capacity does a full table actually need?",
         sub="Air fryer capacity is not quarts &#8212; it is layers and minutes. A holiday hosting worksheet with batch math.",
         kicker="Seasonal guide &#183; Holiday 2026",
         products=["P-01", "P-02", "P-03"],
         intro="Everyone asks how many quarts. The better question is how many batches, and do they "
               "finish before the gravy does? Here is the worksheet we would actually use.",
         verdict="Buy for the biggest meal you actually cook. Two 3-quart baskets that finish on synced "
                 "timers usually beat one 6-quart basket for a real dinner, and the 26-quart oven-style "
                 "unit &#8212; whose listing talks about a whole chicken or a 12-inch pizza inside &#8212; "
                 "is a different category of dinner entirely.",
         sections=[
             ("Capacity is layers, not litres",
              "An air fryer is a small convection oven with a loud fan. Crispness comes from hot air "
              "touching every surface, which means food ideally sits in one layer. Stack a second layer "
              "of fries and the bottom layer steams. Usable capacity is what fits in a single layer "
              "&#8212; not the number stamped on the box. That is why two independent 3-quart baskets "
              "can out-cook one 6-quart basket at dinner."),
             ("Write the meal down before you shop",
              "List the air-fried dishes, estimate single-layer volume per dish, assign minutes per "
              "batch, then add the batches up. Batches multiplied by minutes is the oven time you are "
              "really signing up for. If that number exceeds the calm window before you serve, you need "
              "more single-layer surface, a second zone, or fewer air-fried dishes."),
         ],
         extra=EXTRA_CAPACITY),
    dict(slug="holiday-roast-thermometer",
         title="The holiday roast question: when does a wireless thermometer actually earn its keep?",
         sub="Doneness is a temperature, not a timer. USDA safe temperatures, probe placement, and the walk-away test for wireless probes.",
         kicker="Seasonal guide &#183; Holiday 2026",
         products=["P-04", "P-05"],
         intro="A roast does not care what time it went in. It cares what temperature it reached. "
               "Everything else in the thermometer market is convenience &#8212; and convenience is "
               "worth paying for exactly when you would otherwise be standing by the oven.",
         verdict="If you would otherwise get up every ten minutes to check a closed oven, a wireless "
                 "probe solves a real problem. If you cook steaks and spot-check, a one-second "
                 "instant-read is the whole tool you need.",
         sections=[
             ("Start with the numbers that matter",
              "The USDA chart below is the reference we would tape inside a cabinet door. Measure in "
              "the thickest part of the food, away from bone. Note the rest time on roasts: it is part "
              "of the safety standard, and it is where carryover cooking happens &#8212; the "
              "temperature keeps climbing a few degrees after the meat leaves the heat."),
             ("Two different jobs",
              "An instant-read answers in about a second and goes away again &#8212; perfect for thin "
              "cuts, spot-checks and doneness confidence. Wireless probes stay in the meat while a hub "
              "streams temperature to your phone; they earn their keep on long, closed-door cooks: a "
              "turkey, a standing rib roast, an all-day brisket."),
         ],
         extra=EXTRA_ROAST),
]
