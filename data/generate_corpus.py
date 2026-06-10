"""Data generation script for realistic 320 user feedback responses."""

import json
import random

random.seed(42)

themes_data = [
    (
        "Onboarding & First-Run Setup Friction",
        [
            "The initial onboarding checklist is really confusing when inviting team members to a newly created space.",
            "I tried to setup my new workspace but got stuck on the teammate invite step with no clear error message.",
            "Setting up our company account took forever because the first-run guide crashed midway through.",
            "New users on our team don't understand how to create their first project board or add initial columns.",
            "The welcome modal keeps popping up every time I log in and won't remember dismissal across sessions.",
            "Onboarding flow lacks clear explanations of workspace permission levels and admin access roles.",
            "We had three new hires try to join today and none of them received the initial activation email.",
            "The workspace onboarding setup was frustrating because it required phone verification immediately.",
            "Empty state screens provide zero contextual hints for how to populate tasks or invite collaborators.",
            "Getting started tutorial feels overwhelming with too many tooltips firing simultaneously on first login."
        ],
        ["CSAT Survey", "Support Ticket", "User Interview"],
        ["New Trial User", "Team Lead"]
    ),
    (
        "Search Latency & Platform Sluggishness",
        [
            "Global search is painfully slow when looking up archived documents across nested team folders.",
            "Every time I type in the search bar it takes 5 seconds for results to populate on screen.",
            "Platform search latency makes it almost impossible to quickly find client notes during live meetings.",
            "Search feels laggy and frequently fails to return recently created files or newly tagged tickets.",
            "The app slows down to a crawl when opening large tables with more than 50 rows and custom columns.",
            "Typing has significant lag on long documents, especially when multiple people are viewing simultaneously.",
            "Search indexing seems broken because newly created epics don't show up in search results for hours.",
            "Searching by tag or assignee takes way too long and sometimes times out with an unexpected 504 error.",
            "Filter queries take several seconds to refresh the dashboard view and freeze the browser tab.",
            "Autocomplete suggestions in search are delayed and often display stale cached queries."
        ],
        ["Support Ticket", "CSAT Survey", "App Store Review"],
        ["Individual Contributor", "Team Lead", "Enterprise Admin"]
    ),
    (
        "Billing Invoicing & License Seat Transparency",
        [
            "We were billed for inactive seats that were deactivated two weeks ago by our IT administrator.",
            "There is no self-serve way to download past PDF invoices for our internal accounting department.",
            "Upgrading our billing tier was confusing and accidentally charged our corporate card twice.",
            "We need clearer visibility into user seat utilization and pending invites before the renewal date.",
            "The subscription management portal is hidden deep within settings and hard to navigate.",
            "Our finance team cannot reconcile the monthly statement without detailed line-item tax breakdowns.",
            "We wanted to switch from monthly to annual billing but customer support took 4 days to respond.",
            "Why is there no warning email sent before automatically renewing our enterprise annual plan?",
            "Seat deallocation does not credit prorated amounts back to the workspace billing balance.",
            "Credit card updates fail silently without triggering an administrative alert or retry notice."
        ],
        ["Support Ticket", "Sales Objection", "CSAT Survey"],
        ["Enterprise Admin", "Team Lead"]
    ),
    (
        "Real-Time Collaborative Multi-User Editing",
        [
            "When two people edit the same document simultaneously, text blocks frequently get overwritten.",
            "Real-time cursor presence is jerky and does not accurately track where my colleague is typing.",
            "Multiplayer collaboration lost my paragraph changes when an unexpected offline sync collision occurred.",
            "We experienced a sync collision where comments were duplicated four times on the same board card.",
            "Live updates lag behind by 10 to 15 seconds during team sprint grooming and live retrospectives.",
            "Co-editing works okay for two people but completely desyncs when 5 or more teammates join the document.",
            "Collaborative editing needs version rollback history so we can recover deleted paragraphs safely.",
            "Conflicts happen constantly if someone has a spotty wifi connection during collaborative sessions.",
            "Presence avatars often show teammates as active when they closed their laptop tabs hours ago.",
            "Simultaneous table cell updates overwrite adjacent cells without notifying active editors."
        ],
        ["User Interview", "CSAT Survey", "App Store Review"],
        ["Individual Contributor", "Team Lead"]
    ),
    (
        "Third-Party Integration & Webhook Reliability",
        [
            "Slack integration notifications randomly stop firing every other Tuesday without any alert.",
            "Our Zapier webhook triggers fail silently without any retry notification or error alert delivery.",
            "Connecting our GitHub repository via webhooks fails with a 401 token authentication error.",
            "Bi-directional sync with Jira drops custom field updates during sprint transfers.",
            "Microsoft Teams bot does not display rich card formatting and only posts plain text links.",
            "We need reliable outgoing webhooks whenever a task status transitions to complete or blocked.",
            "Integration setup requires global org admin permissions which our IT department will not grant.",
            "Webhook deliveries often queue up for an hour during peak morning hours before executing downstream.",
            "Disconnecting and reconnecting Slack deletes existing channel notification routing configurations.",
            "API rate limit errors do not return retry-after headers causing integration workers to crash."
        ],
        ["Support Ticket", "Sales Objection", "User Interview"],
        ["Enterprise Admin", "Team Lead", "Individual Contributor"]
    )
]

def generate():
    corpus = []
    resp_counter = 1

    for theme_title, templates, sources, segments in themes_data:
        for i in range(64):
            resp_id = f"RESP-{resp_counter:03d}"
            base_text = templates[i % len(templates)]
            prefixes = [
                "",
                "Feedback: ",
                "Customer Note: ",
                "Pain Point: ",
                "Critical Issue: ",
            ]
            suffixes = [
                "",
                " This is causing significant friction for our team daily.",
                " Please prioritize fixing this in the next release.",
                " We really need a solution for this workflow blocker.",
                " This impacts our organization's daily productivity.",
            ]
            text = f"{random.choice(prefixes)}{base_text}{random.choice(suffixes)}"
            source = random.choice(sources)
            segment = random.choice(segments)
            nps = random.choice([2, 3, 4, 5]) if "slow" in text.lower() or "fail" in text.lower() or "bill" in text.lower() else random.choice([5, 6, 7, 8])

            item = {
                "feedback_id": resp_id,
                "source": source,
                "user_segment": segment,
                "text": text,
                "nps_score": nps,
                "timestamp": f"2026-05-{random.randint(1, 28):02d}T{random.randint(9, 18):02d}:{random.randint(10, 59):02d}:00Z"
            }
            corpus.append(item)
            resp_counter += 1

    with open("AIResearchSynthesisAssistant/data/user_feedback_corpus.json", "w") as f:
        json.dump(corpus, f, indent=2)

    print(f"Generated {len(corpus)} records in user_feedback_corpus.json")

if __name__ == "__main__":
    generate()
