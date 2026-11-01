# From an AI Preview to a Live Website: What I Had to Learn

By Paul A. Magaji

Editorial context: Links to a fixed release, reproducible checks and dated publication results. Availability checks do not establish reader impact or full accessibility.

Seeing an idea become a page is exciting. Headings, sections and controls give a visible form to something that existed only in conversation.

Then another stage begins. Where does the website live? How does the domain reach it? Do its links work? What happens on a phone? How will tomorrow’s correction reach the public version?

My projects have taught me to distinguish a convincing preview from a website ready for visitors.

## Examine it without the conversation

I know what each section is supposed to mean. A new visitor does not.

I need to ask whether someone can understand where they are, find the next step and receive what the page promises. The preview gives me something to assess; it does not establish every part of that experience.

I also need to know which version I am examining. A working copy, preview and public website can represent different states of the project.

## Understand the publishing arrangement

My work includes WordPress on Hostinger and projects involving GitHub and Vercel. Each arrangement has its own way of storing changes and making them public.

When I request an improvement, I want to know where the change is happening and what would publish it. I also want a way to recover earlier work if necessary.

My landdesk.ng investigation made the domain connection especially tangible. A saved setting did not settle whether the intended address reached the intended project.

## Review the content separately

Technical progress can distract from the words. Are claims supported? Do references open? Has placeholder material remained? Does an unfinished feature appear available?

I have encountered references returning errors. A link’s presence did not establish that it led to useful evidence.

The same attention belongs to contact details, navigation and calls to action. I need to follow the path I ask readers to follow.

## Check promises through tasks

A download promises a file. A worksheet promises a process someone can complete. A print option promises a usable result.

Each needs examination at the level of the task: which file arrived, could it open, and did the printed version preserve the necessary information?

Mobile use deserves direct attention too. Can I read comfortably, use the controls and understand what happens after an action? A narrow-screen screenshot alone cannot answer every question.

## Decide deliberately

A passed check establishes something specific. The remaining uncertainty still needs judgment, with the scope of review following what the website asks people to do.

Publication begins continuing care: corrections, changing references and unexpected visitor difficulties. I want a setup I can understand and maintain.

## My release note

For the next publication, I would record the version, intended audience, main tasks checked, content reviewed and unresolved limitations. I would identify how to correct or withdraw the change. That makes “live” a more meaningful statement than a page appearing somewhere online.


## Case record: publishing this collection

This collection provides a bounded example of moving from drafts to a live website. The scope was 13 articles, a reading guide and a companion project brief, integrated with NaijaOS's existing content.

The [release pull request](https://github.com/godwillmakeaday/naijaos/pull/9) records the files and scope. The [merged release commit](https://github.com/godwillmakeaday/naijaos/commit/61357e3ad46dd3dd0d43e98903f1d4ebec4caf19) identifies a fixed version a reader can inspect. This was an AI-assisted publication under my direction; it is not a claim that I hand-coded every page.

The package included individual Markdown articles, a combined text edition, a self-contained HTML reading edition and a ZIP. The HTML edition contains its own styles and can be opened offline. Its online source links still require connectivity.

## What was checked at release

The local publication checks covered 13 article entries, 15 new HTML pages, the reading sequence and 307 local links and fragments. The original ZIP contained 16 files, checked against the packaged source. These counts describe that release; later additions can change them.

After publication on 1 November 2026, an automated HTTP check visited 22 production routes, including all 13 articles, the collection, related pages, stylesheet and main downloads. Each returned HTTP 200. The downloaded ZIP matched the local package by SHA-256 hash.

Those results establish availability and package correspondence at the time of checking. HTTP 200 alone does not establish that a page is understandable, accessible or useful.

## Make the release inspectable

The [collection builder](https://github.com/godwillmakeaday/naijaos/blob/61357e3ad46dd3dd0d43e98903f1d4ebec4caf19/scripts/build-building-series.py) and [integrity checker](https://github.com/godwillmakeaday/naijaos/blob/61357e3ad46dd3dd0d43e98903f1d4ebec4caf19/scripts/check-building-series.py) show how the edition was assembled and what the automated checks examined. Someone with Python and a copy of that repository version can repeat the local build and check.

A reader can also open the [collection](https://naijaos.io/how-i-build-from-nigeria), follow an article's next link and compare its downloadable text with the page. The test is tied to an actual task rather than the appearance of the homepage alone.

## Where the evidence stops

Desktop browser review covered the layout, a first-article navigation and keyboard activation of its contents disclosure. It did not establish full accessibility conformance. Actual Android use, screen-reader navigation and the printed output remained unverified at that release.

The edition has print styling, but the presence of that styling is not proof of a checked printed result. Nor does successful publication establish traffic, reader benefit or revenue. Those require different observations.

This distinction is the lesson I want to preserve: describe the version, perform relevant checks and state precisely what their results support.
