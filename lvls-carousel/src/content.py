"""Carousel copy + slide structure (Thu 15 Oct — LVLS Agency)."""

HANDLE = "@lvlsmarketing"      # <- swap for the real LVLS handle before export
POST_DATE = "THU 15 OCT · 8:00 AM ET"
TOTAL_FLOWS = 5

FLOWS = ["WELCOME", "ABANDONED CART", "BROWSE ABANDONMENT", "POST-PURCHASE", "WINBACK"]
FLOW_ICONS = ["envelope", "bag", "eye", "heart", "moon"]

SLIDES = [
    # ------------------------------------------------------------------ 01 ---
    {
        "kind": "cover",
        "num": "01",
        "eyebrow_chip": "EMAIL MARKETING",
        "eyebrow_text": "CLOTHING BRANDS · FLOW CHECKLIST",
        "headline": [
            {"tokens": [{"text": "5 EMAIL", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "FLOWS", "font": "disp", "color": "accent_ink",
                     "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "EVERY CLOTHING", "font": "disp_b", "color": "ink"},
                ]
            },
            {
                "tokens": [
                    {"text": "BRAND", "font": "disp_b", "color": "ink"},
                    {"text": "needs.", "font": "serif", "color": "accent_soft",
                     "scale": 1.12},
                ]
            },
        ],
        "list_title": "THE 5 FLOWS",
        "footer_left": {"icon": "bookmark", "text": "SAVE THIS"},
        "footer_right": {"text": "SWIPE", "chevrons": 3},
    },
    # ------------------------------------------------------------------ 02 ---
    {
        "kind": "flow",
        "num": "02",
        "flow_index": 0,
        "kicker": "FLOW 01",
        "icon": "envelope",
        "name": "WELCOME",
        "headline": [
            {"tokens": [{"text": "FIRST", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "IMPRESSION", "font": "disp", "color": "accent_ink",
                     "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "ON", "font": "disp_b", "color": "ink"},
                    {"text": "autopilot.", "font": "serif", "color": "accent_soft",
                     "scale": 1.12},
                ]
            },
        ],
        "bullets": [
            {"icon": "envelope", "text": "Tell your brand story."},
            {"icon": "bag", "text": "Show your best sellers."},
            {"icon": "tag", "text": "Offer an incentive only if it fits."},
        ],
    },
    # ------------------------------------------------------------------ 03 ---
    {
        "kind": "flow",
        "num": "03",
        "flow_index": 1,
        "kicker": "FLOW 02",
        "icon": "bag",
        "name": "ABANDONED CART",
        "headline": [
            {"tokens": [{"text": "THE CART", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "SAVED", "font": "disp", "color": "accent_ink", "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "ITSELF.", "font": "disp_b", "color": "ink"},
                    {"text": "Answer the doubt.", "font": "serif", "color": "accent_soft",
                     "scale": 1.0},
                ]
            },
        ],
        "bullets": [
            {"icon": "clock", "text": "Remind them within hours."},
            {"icon": "tshirt", "text": "Show the exact product."},
            {"icon": "question", "text": "Answer sizing and shipping."},
        ],
    },
    # ------------------------------------------------------------------ 04 ---
    {
        "kind": "flow",
        "num": "04",
        "flow_index": 2,
        "kicker": "FLOW 03",
        "icon": "eye",
        "name": "BROWSE ABANDONMENT",
        "headline": [
            {"tokens": [{"text": "THEY LOOKED.", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "THEY LEFT.", "font": "disp", "color": "accent_ink",
                     "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "Bring the product back.", "font": "serif",
                     "color": "accent_soft", "scale": 1.05},
                ]
            },
        ],
        "bullets": [
            {"icon": "eye", "text": "They viewed it, never added it."},
            {"icon": "tshirt", "text": "Follow up with that exact product."},
        ],
    },
    # ------------------------------------------------------------------ 05 ---
    {
        "kind": "flow",
        "num": "05",
        "flow_index": 3,
        "kicker": "FLOW 04",
        "icon": "heart",
        "name": "POST-PURCHASE",
        "headline": [
            {"tokens": [{"text": "THE SALE IS", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "NOT THE END.", "font": "disp", "color": "accent_ink",
                     "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "Keep them, then ask.", "font": "serif",
                     "color": "accent_soft", "scale": 1.05},
                ]
            },
        ],
        "bullets": [
            {"icon": "heart", "text": "Thank them."},
            {"icon": "label", "text": "Explain care and styling."},
            {"icon": "sparkle", "text": "Ask for a review after delivery."},
        ],
    },
    # ------------------------------------------------------------------ 06 ---
    {
        "kind": "flow",
        "num": "06",
        "flow_index": 4,
        "kicker": "FLOW 05",
        "icon": "moon",
        "name": "WINBACK",
        "headline": [
            {"tokens": [{"text": "QUIET LIST,", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "WARM AGAIN.", "font": "disp", "color": "accent_ink",
                     "hl": "accent"},
                ]
            },
            {
                "tokens": [
                    {"text": "Newness beats discounts.", "font": "serif",
                     "color": "accent_soft", "scale": 1.05},
                ]
            },
        ],
        "bullets": [
            {"icon": "moon", "text": "Quiet for one repurchase cycle?"},
            {"icon": "sparkle", "text": "Send something new, not a discount."},
        ],
    },
    # ------------------------------------------------------------------ 07 ---
    {
        "kind": "cta",
        "num": "07",
        "eyebrow_chip": "NEXT STEP",
        "eyebrow_text": "FLOW AUDIT · LVLS AGENCY",
        "headline": [
            {"tokens": [{"text": "DM", "font": "disp", "color": "ink"}]},
            {
                "tokens": [
                    {"text": "AUDIT", "font": "disp", "color": "accent_ink", "hl": "accent"},
                ]
            },
        ],
        "bullets": [
            {"icon": "bookmark", "text": "Save this before you build."},
            {"icon": "share",
             "text": "Send it to a founder still running one welcome email."},
            {"icon": "chat", "text": "Get a review of your flows."},
        ],
        "button": "DM \u201cAUDIT\u201d",
        "button_note": "WE RECORD YOUR FLOWS · WHAT'S MISSING · WHAT TO FIX FIRST",
        "footer_left": {"icon": "bookmark", "text": "SAVE"},
        "footer_right": {"text": "SHARE", "chevrons": 0, "icon": "share"},
    },
]

# ------------------------------------------------------------------ caption ---
CAPTION = """Most clothing brands are running one welcome email and calling it a strategy.

Here are the 5 flows that actually carry revenue for a fashion brand — in the order we build them:

01 WELCOME — brand story, best sellers, and an incentive only if your price position can carry it.
02 ABANDONED CART — within hours, exact product, sizing + shipping answered.
03 BROWSE ABANDONMENT — they viewed it, never added it. Follow up with that product.
04 POST-PURCHASE — thank them, teach care and styling, ask for the review after delivery.
05 WINBACK — one repurchase cycle of quiet gets newness, not another discount.

Save this. Send it to a founder still running one welcome email.
DM "AUDIT" and we'll review your flows.

#emailmarketing #klaviyo #ecommerce #fashionbrand #clothingbrand #emailflows #lifecyclemarketing #retention #ecommercemarketing #digitalmarketingagency #lvlsagency #directtoconsumer #shopify #marketingstrategy"""

STORY_BEATS = [
    "01 Cover — hook: 5 flows, no fluff",
    "02 Welcome — story, best sellers, incentive only if it fits",
    "03 Abandoned cart — speed + product + objections",
    "04 Browse abandonment — the product they viewed",
    "05 Post-purchase — thank, teach, review",
    "06 Winback — newness, not discount",
    "07 CTA — save, share, DM AUDIT",
]


# ============================================================================
# MINIMAL BLACK edition — the approved reference style (bottom-weighted)
# ============================================================================
MIN_SLIDES = [
    {
        "num": "01", "label": "EMAIL MARKETING", "icon": "flow",
        "micro": ["THE LVLS CHECKLIST", "five flows · one revenue engine"],
        "title": [[("5 EMAIL FLOWS", "w")],
                  [("every clothing brand ", "w2"), ("needs.", "a2")]],
        "lines": [],
        "swipe": "Swipe for more",
    },
    {
        "num": "02", "label": "EMAIL FLOW 01", "icon": "envelope",
        "micro": ["FLOW 01 · WELCOME", "window: day 0–7 of subscriber life"],
        "title": [[("WELCOME", "w")]],
        "lines": [
            [("Tell your brand story.", "w")],
            [("Show your best sellers.", "w")],
            [("Offer an incentive ", "w"), ("only if it fits.", "a")],
        ],
        "swipe": "Swipe",
    },
    {
        "num": "03", "label": "EMAIL FLOW 02", "icon": "bag",
        "micro": ["FLOW 02 · ABANDONED CART", "window: first 24 hours"],
        "title": [[("ABANDONED ", "w"), ("CART", "a")]],
        "lines": [
            [("Remind them ", "w"), ("within hours.", "a")],
            [("Show the exact product.", "w")],
            [("Answer sizing and shipping.", "w")],
        ],
        "swipe": "Swipe",
    },
    {
        "num": "04", "label": "EMAIL FLOW 03", "icon": "eye",
        "micro": ["FLOW 03 · BROWSE ABANDONMENT", "window: day 1–3 after view"],
        "title": [[("BROWSE ", "w"), ("ABANDONMENT", "a")]],
        "lines": [
            [("They viewed it, ", "w"), ("never added it.", "a")],
            [("Follow up with that exact product.", "w")],
        ],
        "swipe": "Swipe",
    },
    {
        "num": "05", "label": "EMAIL FLOW 04", "icon": "heart",
        "micro": ["FLOW 04 · POST-PURCHASE", "trigger: delivery confirmed"],
        "title": [[("POST-", "w"), ("PURCHASE", "a")]],
        "lines": [
            [("Thank them.", "w")],
            [("Explain care and styling.", "w")],
            [("Ask for a review ", "w"), ("after delivery.", "a")],
        ],
        "swipe": "Swipe",
    },
    {
        "num": "06", "label": "EMAIL FLOW 05", "icon": "moon",
        "micro": ["FLOW 05 · WINBACK", "trigger: one repurchase cycle quiet"],
        "title": [[("WINBACK", "w")]],
        "lines": [
            [("Quiet for one repurchase cycle?", "w")],
            [("Send something new, ", "w"), ("not a discount.", "a")],
        ],
        "swipe": "Swipe",
    },
    {
        "num": "07", "label": "SAVE THIS", "icon": "bookmark",
        "micro": ["FREE FLOW TEARDOWN", "48-hour turnaround"],
        "title": [[("DM ", "w"), ("AUDIT", "a")]],
        "lines": [
            [("Send it to a founder still running one welcome email.", "w")],
            [("Get a review of your flows.", "a")],
        ],
        "swipe": None,
        "button": "DM \u201cAUDIT\u201d",
    },
]
