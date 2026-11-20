"""How-to and explainer guide records added by session 93894704, merged into build_site.GUIDES.

Kept in its own module for the same reason `seasonal_guides.py` is: long HTML blocks collide with
the generator's quoting when they are pasted inline, and a separate file keeps the merge surface
small for the other sessions working on this repo.

Every number in these two guides comes from one of three places, and each says which:
  * the USDA FSIS "Food Thermometers" factsheet (source register S24), quoted or closely paraphrased;
  * the official Amazon listing, as recorded in `data/products.json` with its dated section citation;
  * nothing else. No search-volume, popularity, performance or cook-time claim is made anywhere.
"""

USDA_THERMO_URL = "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers"

# USDA's own published reading speeds, copied from the "Types of Food Thermometers" table on S24.
_SPEED_ROWS = [
    ("Thermocouple (digital)", "2&ndash;5 seconds", "Fastest reading USDA lists; 1/4&nbsp;in or deeper, as needed", "Can be calibrated"),
    ("Thermistor (digital)", "about 10 seconds", "Reads thin and thick foods; 1/2&nbsp;in deep", "Some models; check the instructions"),
    ("Instant-read bimetal (dial)", "15&ndash;20 seconds", "2&ndash;2&frac12;&nbsp;in deep; not for thin foods sideways", "Some models; check the instructions"),
    ("Oven-safe bimetal (dial)", "1&ndash;2 minutes out of the food", "Not appropriate for food under 3&nbsp;in thick", "Some models; check the instructions"),
    ("Wireless / smart probe", "live in the oven", "At least 1&nbsp;in deep; designed to stay in the food", "Smart thermometers can be calibrated"),
    ("Oven-cord thermometer", "about 10 seconds", "At least 1/2&nbsp;in deep; base unit on the counter", "Cannot be calibrated"),
]
_speed = "".join(
    '<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in _SPEED_ROWS)

USDA_SPEED_TABLE = (
    '<table class="usda"><caption>Reading speed and calibration, by thermometer type, as published by '
    'the USDA. Source: <a href="%s">FSIS &mdash; Food Thermometers</a> (page last updated Mar 21, 2025), '
    'registered as S24 in the <a href="../sources.html">source register</a>.</caption>'
    '<thead><tr><th scope="col">Type</th><th scope="col">Time to a reading</th>'
    '<th scope="col">Placement USDA specifies</th><th scope="col">Can it be calibrated?</th></tr></thead>'
    '<tbody>%s</tbody></table>' % (USDA_THERMO_URL, _speed))

ICE_STEPS = """<h2>The test, step by step, as the USDA publishes it</h2>
<ol class="tight steps">
  <li>Fill a large glass with ice cubes.</li>
  <li>Add drinking water and stir well, so the glass holds an ice-water slurry rather than dry cubes.</li>
  <li>Immerse the stem a minimum of 2&nbsp;inches, touching neither the sides nor the bottom of the glass.</li>
  <li>Wait a minimum of 30&nbsp;seconds.</li>
  <li>Read it <em>without</em> taking the stem out of the water.</li>
</ol>
<p>The USDA states the target plainly: <q>It should read 32 degrees F; if it does, the thermometer is
calibrated.</q> If it does not, adjust it according to the manufacturer's instructions &mdash; many dials
have a calibration nut under the face &mdash; and if the unit gives you no way to adjust, the agency's own
conclusion is that you may need to replace it. Both thermometer listings here are dated
<span class="stamp">2026-11-20</span> in this site's register, so you are comparing a claim we read
against a test you can run.</p>
<p class="small">Steps and quotations: <a href="%s">USDA FSIS, Food Thermometers</a> (S24 in the
  <a href="../sources.html">source register</a>), section &ldquo;Calibration&rdquo;.</p>""" % USDA_THERMO_URL

CLUSTER_LINKS = """<div class="panel"><p class="kicker">Keep reading</p><p>%s</p></div>"""


GUIDES = [
    dict(slug="thermometer-ice-test",
         title="Is your meat thermometer telling the truth? The two-minute ice-water test",
         sub="USDA publishes the calibration check. Here it is step by step, and what a pass means "
             "when a listing claims plus or minus half a degree.",
         kicker="How-to · food safety", products=["P-04", "P-05"],
         intro="""A thermometer is the one instrument in the drawer nobody ever checks. There is a
         standard test for it, published by the USDA's Food Safety and Inspection Service, and it
         takes a glass, some ice, and about two minutes. Run it before the first roast you care
         about, not after.""",
         sections=[
            ("Why bother, if it came out of the box", """Because a thermometer is a measuring
            instrument, and instruments drift, get knocked, and are occasionally wrong from the
            start. USDA's baseline is worth knowing before you read any marketing number:
            <q>Most food thermometers will give an accurate reading within 2 to 4 degrees F.</q>
            That is the general expectation for the category. A listing that states something far
            tighter than that is making a specific claim, and the ice-water test is the cheapest way
            to see whether the claim survives contact with your kitchen.""",),
            ("What a pass buys you, and what a fail costs", """A pass at 32&nbsp;&deg;F means the
            cold end of the range is honest, which is the end most home cooks never check. A fail is
            not necessarily a dead instrument: USDA says to adjust according to the manufacturer's
            instructions, and notes that many thermometers have a calibration nut under the dial. The
            harder lesson is that not every type can be adjusted at all. USDA's own table marks oven-cord
            thermometers and thermometer forks as <em>cannot be calibrated</em>, thermocouples as
            <em>can be</em>, and most digital and dial models as <em>some models can be, check the
            instructions</em>. &ldquo;Calibratable&rdquo; is therefore a specification worth hunting for
            before you buy, and neither listing in this register states it, so we leave that field blank
            rather than assume.""",),
            ("Read the accuracy claim against that baseline", """The ThermoMaven HT07 listing states
            &plusmn;0.5&nbsp;&deg;F accuracy alongside a 0.1&deg; display resolution, and its Included
            Components line lists a calibration certificate in the box. Both are seller statements on a
            product page, dated in our register, not results of a test we ran. So: if your unit claims
            half a degree and your glass of ice says 34&nbsp;&deg;F, you have learned something about
            your unit that no listing could tell you. The CHEF iQ Sense is the other kind of object
            &mdash; the listing states a 4.75-inch immersion depth, Wi-Fi and Bluetooth through an app,
            and probes designed to stay in the food while it cooks, which is exactly the category USDA
            describes as live-status probes. Its alerts are only as good as the number underneath them,
            so the same test applies before you trust a push notification.""",),
            ("Placement beats calibration", """A perfectly calibrated thermometer in the wrong place
            still returns a wrong number. USDA is specific about this: the tip goes in the thickest part
            of the food, away from bone, fat and gristle; thin things like a burger patty or a boneless
            breast get the probe inserted through the side so the whole sensing area reaches the centre;
            a whole bird is checked in three places &mdash; the innermost thigh, the innermost wing and
            the thickest part of the breast. For a big roast it says check several spots, because the
            reading only reflects where the sensor sits. Before you conclude a thermometer is off, rule
            out that it was nowhere near the centre.""",),
            ("The one-point problem, and the boiling-water check", """The ice test checks one point on
            the scale. USDA publishes a second method for the top of it: a rolling boil, stem at least
            2&nbsp;inches deep, at least 30&nbsp;seconds, reading 212&nbsp;&deg;F at sea level. The
            agency flags the altitude caveat itself &mdash; water boils lower at altitude, likely by at
            least 2&nbsp;&deg;F and possibly by as much as 5&nbsp;&deg;F &mdash; which is why a boiling
            reading that looks wrong may be correct for your elevation. For cooking steaks and breast to
            USDA's stated minimums, the ice test is the one worth the two minutes.""",),
            ("Care, because the test involves a glass of water", """USDA's care guidance is blunt: wash
            with hot soapy water, most thermometers should not be immersed, and do not leave a
            thermometer in food while cooking unless the maker says it is designed for it. The two
            listings here do not agree with each other on that point, which is why the listing matters
            more than the habit: ThermoMaven's Materials &amp; Care field says <em>Wipe Clean</em> while
            the same page claims IP67 waterproof, and the CHEF iQ Sense page states waterproof,
            dishwasher-safe probes. Read the care field on your unit before you dunk anything.
            One caution when you go looking for the sensing area on a spec sheet: both listings give
            a length figure under a field that mixes &ldquo;Immersion Depth&rdquo; with &ldquo;Item
            Length&rdquo; (6.5 inches on the ThermoMaven, 4.75 inches on the CHEF iQ), which is not the
            same number as where the sensor ends. Treat the manual as the authority on immersion
            depth and use the listing figure only to check the probe is long enough for what you cook.""",),
         ],
         verdict="""Run the ice-water test before the first cook that matters: 32 °F after
         30 seconds in a properly stirred slurry means the cold end of your thermometer is honest,
         and if the unit cannot be adjusted, USDA's advice is to replace it. Anything tighter than that
         — a ±0.5 °F claim, a certificate mentioned in the box list — is a
         statement on a listing until your own glass says otherwise.""",
         extra='<figure class="guide-figure"><img src="../assets/img/guide-ice-water.jpg" alt="A tall glass of crushed ice and water with a folding digital thermometer inserted, condensation on the glass" width="1536" height="1024" loading="lazy"><figcaption>Illustrative image, generated for this site &#8212; the ice-water method is described below, and this is not a photograph of either product.</figcaption></figure>' + "\n" + ICE_STEPS + "\n" + USDA_SPEED_TABLE + "\n" + CLUSTER_LINKS % (
             'The claim this test checks is written up in '
             '<a href="thermometer-accuracy.html">how to read accuracy claims</a>, and the choice of tool '
             'in <a href="instant-vs-wireless.html">instant-read versus wireless</a>. Both products '
             'referenced here carry their dated specification tables on their own pages: '
             '<a href="../products/p04-thermomaven-1sec.html">ThermoMaven HT07</a> and '
             '<a href="../products/p05-chefiq-sense-gen3.html">CHEF iQ Sense</a>.')),

    dict(slug="read-an-air-fryer-listing",
         title="How to read an air fryer listing: what “Hi-Fry” and 24 presets actually tell you",
         sub="The title, the bullets and the specification table are three different sources stapled "
             "onto one page. Here is which one to trust for which number.",
         kicker="Explainer · how we read listings", products=["P-01", "P-02", "P-03"],
         intro="""Every product page is three documents wearing one coat: a title written for search,
         bullets written to sell, and a structured table written to be filtered. They are maintained
         separately, and they disagree. Knowing which block a number came from is most of the skill,
         and it takes about a minute per appliance.""",
         sections=[
            ("Three blocks, three jobs", """The <strong>title</strong> is a keyword string: capacity, a
            couple of feature names, a colour. It is the least reliable place for a number and the most
            quoted one. The <strong>bullets</strong> (&ldquo;About this item&rdquo;) are marketing prose
            with figures dropped into them. The <strong>Product information</strong> block &mdash;
            Features &amp; Specs, Measurements, Item details &mdash; is structured fields, and it is
            the closest thing to a data source on the page. Not a guarantee, though: it is filled in by
            the same seller, and on the pages in our register it sometimes contradicts the bullets and
            the title. When you cite a spec at anyone, including yourself, say which block it came
            from.""",),
            ("When the same number appears twice and disagrees", """These are all live on
            """ + "2026-11-20" + """ and all recorded in our register. The 8-quart Chefman prints 1700
            watts in the Features &amp; Specs fields and 1000 watts in a bullet; its title promises a
            450&nbsp;&deg;F Hi-Fry option while the temperature fields say 400&nbsp;&deg;F maximum. The
            Emeril's title says 24 one-touch preset options and one bullet says 25; the title and the
            Included Components field list six accessories while a description field says seven. The
            dual-basket Chefman says 6 quarts in the title and bullets, and its Measurements table prints
            6 litres, which is about 6.3 US quarts. None of these resolve into a single true number from
            the page alone. What a careful reader does with a disagreement like that: treat the figure as
            unsettled, ask the seller, and never quietly average the two.""",),
            ("Features versus decoration", """A word in a title is not a specification. &ldquo;Sync
            Finish&rdquo; on the dual-basket page describes a behaviour you can check on the spot: two
            baskets timed to end together. &ldquo;Hi-Fry&rdquo; is a mode with its own temperature
            ceiling &mdash; and it is exactly where the 450 versus 400 argument lives on the 8-quart.
            &ldquo;4-in-1&rdquo; counts cooking modes the seller decided to name, which tells you nothing
            about how well any of them works. &ldquo;24 one-touch presets&rdquo; counts buttons; the
            8-quart here has four &mdash; French fries, chicken, meat, fish &mdash; and four honest
            buttons beat 24 you will never use. Certification wording (&ldquo;cETL approved&rdquo; on two
            of these pages, &ldquo;NIST and NSF&rdquo; on a thermometer page) is a claim on a listing; we
            have not seen the certificates and neither of us has.""",),
            ("The numbers that actually decide the purchase", """Depth first, capacity second, and both
            from the structured fields. From our register: 13.38&nbsp;in deep for the dual-basket,
            12.75&nbsp;in for the 8-quart, 16.9&nbsp;in for the French-door oven, which also needs room in
            front for two doors to swing. Then capacity, understood properly: quarts describe the
            container, and an air fryer cooks what hot air can reach in a single layer. Two independent
            3-quart baskets do a different job from one 6-quart drawer, and both are a different job again
            from a 26-quart cavity whose own listing talks about a 12-inch pizza and a 6-pound chicken.
            Weight is what decides whether the appliance lives on the counter: 13.3 pounds and 12.8 pounds
            for the two Chefmans, and for the Emeril the listing simply does not state an item weight, so
            ours stays blank.""",),
            ("What a preset count is, and what it is not", """A preset is a stored pairing of a
            temperature and a run time. It adds no heat, no capacity and no method; it saves two
            button presses on a dish you repeat. That is the whole of it, which is why a count is a
            weak thing to compare: the 8-quart Chefman names four presets in its structured field
            (French fries, chicken, meat, fish) while the Emeril prints 24 in its title and
            description and 25 in the About-this-item bullets, on the same page, on the same day we
            read it. If you want the shortcuts that matter, look for the controls that fix a mistake
            rather than the ones that name a food: a +2-minute button, stated on the dual-basket
            listing, and an LED shake reminder, stated on the 8-quart. A frozen-chicken mode answers
            a question your dinner rarely asks."""),
            ("Four checks that cost one minute", """(1) Find the number in the structured table before
            you accept it from a bullet. (2) If two fields disagree, ask the seller before ordering, not
            after. (3) Read what Included Components actually lists, because accessory counts and
            preset counts are where pages drift. (4) Write down the date you read the page. These
            listings change without notice, which is why every table on this site carries its date and
            its link rather than our memory.""",),
         ],
         verdict="""Trust the structured field over the bullet and the title. Where two fields disagree,
         the number is unsettled — ask the seller instead of choosing the flattering one. And
         measure depth before you compare quarts: the counter decides the purchase, and a single layer
         decides the cooking.""",
         extra=CLUSTER_LINKS % (
             'The same three listings are compared field by field on the '
             '<a href="../compare.html">compare page</a>, and the capacity question is worked through in '
             '<a href="capacity-checklist.html">the no-hype capacity checklist</a>. Counter space and '
             'cleanup have their own guide: <a href="cleanup-counter-space.html">cleanup and '
             'counter-space trade-offs</a>.')),
]
