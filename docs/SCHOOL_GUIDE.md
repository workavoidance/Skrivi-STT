# Skrivi for schools: Snakk and Lytt

**Language:** [Norsk](SCHOOL_GUIDE_NB.md) | English

Updated 20 September 2026. This shared guide supports a school's assessment of
one or both apps. It is not official approval, certification or legal advice.
Record the actual package version and features being considered: current source
code, test builds and published downloads may differ.

## Two tools, one family

**Snakk — write with your voice.** Hold the configured shortcut, speak and release.
Your words appear at the cursor, for example in Word. Review and correct the result.
A pupil who finds typing difficult can speak a draft and then edit it.

**Lytt — have text read aloud.** Select text and press Ctrl + Alt + Space, or paste
text into Lytt and start reading aloud. Headphones can help. A pupil can listen to
an assignment or hear their own draft to notice missing words. The app does not
explain the assignment or answer it.

The Windows apps have separate installations. Either can be used on its own.
Both support Norwegian and English; test the available voices and recognition
with the pupil's actual language needs. Recognition, pronunciation and language
detection can be wrong. Do not assume support for every dialect or written variety.

## Shared foundation

- Speech recognition and speech synthesis run locally. This processing does not
  upload pupil text or audio to Skrivi or a cloud service.
- Once required models are installed, these functions work offline. Downloading,
  distribution and update services are separate network activities.
- No Skrivi pupil account, login or profile is required. Windows, Microsoft Store
  and school-managed distribution may have their own account requirements.
- No licence fee or subscription. Application source is open; bundled models,
  voices and dependencies retain their own documented licences.
- Neither app generates answers, ideas, summaries or improved schoolwork.
  Snakk transcribes speech; Lytt synthesises audio from existing text.
- Local processing and open source support assessment; they do not guarantee
  security, accuracy, suitability or automatic school approval.

The school should consider the whole workflow, including other applications.
Word, a learning platform or a clipboard service may retain or sync information
independently of Skrivi. No pupil account does not mean no personal data is processed.

## Differences to include in the assessment

### Snakk: microphone → local recognition → text in another app

Snakk holds microphone audio in memory during transcription. It does not save
dictated audio to disk or keep a dictated-text history. The receiving application
may retain the text through documents, undo history, autosave or cloud sync.
Consider microphone access, transcription errors, noise and whether others can
overhear the pupil. Memory handling is not a guarantee against Windows paging
or system-level diagnostics.

### Lytt: selected or pasted text → local synthesis → audio

Selected text is obtained through Windows accessibility, with copying and restoring
the clipboard as a fallback. Text can also be pasted directly into the reader.
Lytt creates temporary audio files, removed on normal exit. Do not assume cleanup
after an abnormal exit. Audio deliberately saved by the user remains until deleted.
Consider clipboard access/history/sync, sensitive source text, temporary files,
saved audio, pronunciation errors and headphones.

Versions that include screen-region reading additionally process selected screen
content with local optical character recognition (OCR). Record whether that feature
is present and permitted. Check recognition errors before relying on the result.
Do not assume a newer feature exists in the package linked from the website.

## Installation, updates and support

Use the [Snakk product page](https://skrivi.no/dictation/) or
[Lytt product page](https://skrivi.no/read-aloud/) to identify the advertised download.
Record its version, source, publisher/signature status and installation route.
The two apps and Store/standalone packages can have different release status.
Do not bypass school security controls to run an unapproved package.

Snakk requires a speech-model download before offline use. Lytt's full installer
bundles its default speech models. Check disk space, Windows compatibility,
permissions, shortcuts and accessibility on a representative school laptop.
Plan how IT will deploy, update and remove the chosen package. Standalone Lytt
uninstall preserves its library/settings/saved assets; uninstall is not a data
deletion procedure. Review storage and deletion for the actual distribution.

Use [website help](https://skrivi.no/help/) and the relevant repository for support.
Do not include pupil text, audio or screenshots containing personal data in public
issues. Agree a school contact and a procedure for problems and security concerns.

## Shared assessment record

Complete once, with app-specific notes where needed.

- [ ] Scope: Snakk / Lytt / both; package versions and sources: __________
- [ ] Features included (microphone, selected text, saved audio, OCR): __________
- [ ] Pupil needs, intended use and limits: __________
- [ ] Data flow reviewed, including other apps, clipboard and cloud sync.
- [ ] Storage, access, deletion and abnormal-exit behaviour reviewed.
- [ ] Privacy/security assessment completed under school procedures; IT and,
      where needed, the data protection officer involved.
- [ ] Installation, signatures, updates, removal and support responsibilities agreed.
- [ ] Limited pilot agreed following review; shortcuts, languages, accessibility,
      accuracy and offline operation tested on the intended devices.
- [ ] Decision and any conditions: __________
- [ ] Responsible contact and review date/triggers: __________

Shared evidence can support both apps, but record which apps and versions the
decision covers. A new feature or material change may require a fresh review.

## Classroom use and examinations

Distinguish everyday schoolwork, classroom assessment and formal examinations.
An everyday-use decision is not itself examination permission. Ask the school
to check current rules and any individual accommodations for the intended context.
Do not describe a planned examination mode as an available, approved feature.

## References

[Udir: school-owner privacy responsibilities (Norwegian)](https://www.udir.no/regelverk-og-tilsyn/personvern-for-barnehage-og-skole/barnehage--og-skoleeiers-ansvar/)
explains responsibilities for data handling, security and risk assessment.

App-specific references supplement this guide; they are not separate application processes:

- Snakk: [privacy and data flow](PRIVACY.md), [security](../SECURITY.md),
  [architecture](ARCHITECTURE.md), [source](https://github.com/workavoidance/Skrivi-STT).
- Lytt (English technical references): [installation and privacy](https://github.com/workavoidance/Skrivi-TTS/blob/main/README.md),
  [architecture](https://github.com/workavoidance/Skrivi-TTS/blob/main/docs/ARCHITECTURE.md),
  [component and voice licences](https://github.com/workavoidance/Skrivi-TTS/blob/main/THIRD_PARTY_NOTICES.md),
  [source](https://github.com/workavoidance/Skrivi-TTS).

Technical references on the main branch describe current development; use the
matching release/tag when reviewing an older package.
