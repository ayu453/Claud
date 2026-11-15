# JEE Squad — Product & Engineering Specification

**Version:** MVP v0.1  
**Assumptions:** Responsive web app first; India-first launch; Asia/Kolkata default timezone; student accounts require guardian consent when under 18; content is original/licensed; commitment deposit is OFF; one active weekly track per learner.

## 1. Product summary and assumptions

JEE Squad helps Class 11, Class 12 and dropper students build consistent JEE Main + Advanced preparation through a mastery gate and a small squad of 4–6 peers. It is an accountability and retrieval-practice layer, not a replacement for coaching, NCERT, or full mock-test platforms.

**Promise:** one focused topic a day, seven fresh questions, useful feedback, weekly revision and a squad that notices when you need help.

Assumptions and decisions:
- Web MVP is the fastest low-cost validation route; responsive PWA makes it installable on Android.
- Students choose Balanced (Physics/Chemistry/Maths rotation) or Focus (one weak subject for the week).
- A topic requires at least 30 active questions before it can be scheduled. The daily picker uses 3 easy, 3 medium, 1 hard; the hard item is tagged Advanced-style.
- If a bank cannot supply unseen questions, the app does not repeat old questions silently. It shows a content-shortage state and alerts admins.
- Saturday revision is compulsory content but has no scored test. Sunday exam is 25 questions and requires 20 correct.
- Daily pass unlocks the next scheduled topic. Failure repeats the same topic on the next study day with a fresh set.
- Missed days pause the schedule; they do not count as a failed test. One pause token/month protects a planned skip. During declared board/JEE mock weeks, a light-revision calendar replaces the normal gate.
- Three failed attempts trigger Easy Revision Mode suggestion; it never locks the learner out of help.
- No public ranks, public profiles, open DMs, likes, or social feed.
- OTP, push notifications, video meeting links, moderation operations and payment collection require provider credentials and operational setup before production.

## 2. User flow

1. Splash → phone number → OTP verification.
2. Consent gate: age band; if under 18, guardian contact and verifiable consent before social features and persistent progress activation. Do not collect date of birth unless legally necessary; store age band and consent evidence minimally.
3. Onboarding: class (11/12/dropper), target (Main / Main + Advanced), confidence per subject, available hours, preferred daily time, language, timezone, optional city/coaching.
4. Placement: short diagnostic (not used to rank students) estimates level and recommends chapter starting points.
5. Matching queue: rule-based squad assignment; learner can study solo while waiting.
6. Home: today’s topic, progress gate, squad check-in, streak, upcoming Saturday/Sunday.
7. Topic → notes/formulas/video link → start daily test.
8. Test: 7 questions, timer, shuffled options; submit once; instant score and worked solutions.
9. Result: pass unlocks next scheduled topic; fail repeats topic next study day. Incorrect answers enter Mistake Notebook.
10. Saturday: revision pack and self-checklist, no score.
11. Sunday: weekly exam, 25 questions; pass unlocks next week; fail repeats same week with supportive recovery plan.
12. Squad: member progress states (not detailed answers), weekly challenge, check-in, structured Doubt Cards.
13. Progress: personal improvement graph, subject accuracy, weak chapters, average time/question.
14. Settings: notification window, privacy, language, accessibility, report/block, consent withdrawal and account deletion.

## 3. Detailed feature spec and business rules

### 3.1 Curriculum and weekly track
Hierarchy: Subject → Chapter → Topic. Subjects are Physics, Chemistry, Mathematics. Chemistry topics carry branch tag PHYSICAL / ORGANIC / INORGANIC. Curriculum records map to NCERT chapter references and JEE Main/Advanced syllabus versions; store syllabus_version to handle revisions.

Balanced schedule example: Mon Physics, Tue Chemistry, Wed Maths, Thu Physics, Fri Chemistry. Maths appears in next week’s first slots to maintain rotation. Focus schedule uses the learner's selected weak subject for all five weekdays. Admin can curate topic sequence; user can choose among approved tracks.

### 3.2 Daily learning gate
- Daily test has exactly 7 unique question IDs, never previously served to that learner for that topic.
- Mix is exactly 3 EASY, 3 MEDIUM, 1 HARD. Hard question must be Advanced-style; all questions still carry Main/Advanced level tags.
- Pass threshold: 5/7. Passing marks the topic PASSED and unlocks the next scheduled topic.
- Failure increments topic attempt count and schedules the same topic next study day with a fresh set.
- At attempt 3, offer Easy Revision Mode: simplified explanation, worked example, NCERT-level practice, then return to normal difficulty. No punitive lockout.
- A test set is single-use. Submission must contain exactly the issued question IDs. Server-side timer and attempt state are authoritative.
- Practice mode has no negative marking. Exam-mode marking is +4/-1 for single-correct and multiple-correct only when configured to JEE scheme; numerical has no negative marking. Advanced multi-correct marking can be configured per question; default MVP scoring is all-or-nothing and must be labelled clearly.

### 3.3 Saturday revision
Generate one revision pack for the week's topics: formula sheet, concept map, key points, common mistakes, and Mistake Notebook items. No scored test, no streak penalty for not completing every card. A short completion acknowledgement is optional.

### 3.4 Sunday weekly exam
Exactly 25 unseen questions distributed across topics covered that week, mixed MCQ and numerical. Pass at 20/25 correct. Exam mode toggle controls negative marking; show score as both correct count and marks. Failure repeats the same week's topic plan next cycle and applies a motivational recovery state: no bonus challenge unlock and squad bonus reduced by a small capped amount. Never remove previously earned progress or shame the student.

### 3.5 Calendar, streaks and pauses
- Store timestamps in UTC; store user timezone as IANA ID. Compute study-day boundaries in the user's timezone.
- Daily study day is the learner's configured reminder window, not midnight; late-night usage does not create accidental missed days.
- One pause token per calendar month. Redeeming it marks a scheduled day as PAUSED and preserves streak; it cannot be sold or transferred.
- Missed day without token: mark MISSED, pause progression and offer catch-up; do not fabricate a fail attempt. Resume same pending topic.
- Board/JEE mock pause: admin or learner can declare a date range; normal gates switch to light revision, no new unlock is consumed, and streak is protected. Admin declarations require a reason and audit log.
- Streak counts completed learning days; pause days are neutral. No competitive streak comparison.

### 3.6 Squad matching and lifecycle
Squad size 4–6. Hard filters: class, target exam compatibility, timezone overlap, daily slot. Soft score: level proximity, complementary subject strengths/weaknesses, optional city/coaching only when opted in. Do not expose phone numbers or exact location to peers.
- Create squad only when at least 4 compatible learners are waiting. If no match, solo mode remains available.
- Match complementary strengths using profile subject confidence; avoid placing all learners with identical weak subjects.
- Inactive member: 7 days inactive → mark at-risk and nudge privately; 14 days → offer squad merge/replacement. Preserve historic attempts. Never reveal private absence reasons.
- Squad check-in: weekly 20-minute slot; prompt “What did I learn? Where am I stuck? Who can help?” Provide offline meetup suggestion or trusted meeting link; no open video room in MVP.

### 3.7 Weekly challenge engine
Rotate by week number:
1. Solo + Squad Streak: personal completion + squad participation bonus.
2. Partner Challenge: paired learners create one original question each for the other's weak chapter; peer submissions are moderated.
3. Group Challenge: squad average accuracy ≥80%; only participating members count, minimum 4 attempts.
4. Squad vs Squad: friendly private match; compare aggregate improvement/participation, never publish global ranks.
5+. Rotate Teach-Back, PYQ Hunt, Speed Round, Mistake Notebook Swap, Revision Relay.
Rewards are badges and bonus revision packs, not cash or public rank.

### 3.8 Doubt Cards
Fields: topic, question text or optional image, what I tried, status, replies. Available only to squad members. No open DM. Report, block and moderator review. Image uploads must strip EXIF metadata, scan for malware, enforce size/type limits and have retention limits. For minor safety, prevent images of faces/IDs and provide text-first use.

### 3.9 Mistake Notebook
Every incorrect response is saved with question, learner response, correct answer, detailed solution, common mistake, topic and attempt timestamp. Learner can mark reviewed; do not delete automatically. Revision suggestions use spaced intervals (e.g. 1, 3, 7, 14 days) but never create a mandatory extra test.

### 3.10 Dashboard and notifications
Personal metrics: weekly correct %, subject accuracy, chapter weakness, time/question, topics passed, consistency trend. Show improvement relative to the learner's own prior weeks, not other students.
Notifications: one daily reminder in chosen window; result; squad nudge; Sunday exam reminder; weekly summary. Quiet hours default 22:00–07:00 local. No repeated guilt-based notifications. Push provider: FCM.

### 3.11 Admin panel
- CRUD syllabus, chapters, topics and revision resources.
- CSV question import with validation and preview; reject missing solution, invalid answer schema, unsupported license, difficulty mismatch, duplicate key and insufficient bank coverage.
- Manage squads, challenge templates, pause windows, reports and moderation queue.
- Stats: active learners, day-7 retention, topic pass rate, question exposure, bank coverage, squad match wait time, Sunday completion.
- Role-based access: content editor, moderator, institute admin, platform admin. Audit every sensitive action.

### 3.12 Safety, privacy and wellbeing
- No public ranks, profiles, photos, open DMs or unmoderated feed.
- Under-18 accounts require guardian consent before social/community features and data processing that requires it. Provide guardian notice, consent timestamp/version, withdrawal and deletion request flow. Obtain legal review for applicable Indian child-data rules before launch.
- Data minimisation, encryption in transit/at rest, hashed phone identifiers, least-privilege access, audit logs, backups and retention schedule.
- Report/block on every user-generated surface. Moderation SLA target: urgent safety report within 4 hours; other reports within 48 hours.
- Detect patterns such as repeated failed attempts or very late-night use only to offer gentle breaks and support—not to diagnose. Show “You can pause; progress over perfection.” If a student expresses distress, show trusted adult/counsellor guidance and verified local support resources; never infer diagnosis.
- Daily test suggested cap 20 minutes; allow accessibility accommodations and extra time. Repeated failure triggers break reminder, not forced lockout.

### 3.13 Commercial feature flags
- Commitment deposit: OFF, not in MVP. Do not activate for minors. Any future version requires legal/payment review and transparent refund rules.
- Premium: ₹99–299/month, subject to pilot willingness-to-pay. Core loop remains usable free for one subject track.
- Mentor sessions only with verified, safeguarded mentors and guardian-aware scheduling for minors.

## 4. Database schema

Use PostgreSQL. Core tables (PKs are UUID in production; integer IDs in starter scaffold are local-only):

| Table | Important columns |
|---|---|
| users | id, phone_hash UNIQUE, display_name, class_level, target_exam, language, timezone, daily_hours, consent_status, created_at, deleted_at |
| guardian_consents | id, user_id, guardian_contact_hash, status, notice_version, verified_at, withdrawn_at |
| profiles | user_id, physics_confidence, chemistry_confidence, maths_confidence, daily_slot, city_opt_in, coaching_opt_in |
| subjects | id, code UNIQUE, name |
| chapters | id, subject_id, syllabus_version, name, ncert_reference, sequence_no |
| topics | id, chapter_id, name, chemistry_branch, sequence_no, notes_md, video_url, formulas_json, key_points_json, active |
| questions | id, topic_id, type, difficulty, exam_level, prompt_md, options_json, answer_json, solution_md, common_mistake, concept_tags, pyq_year, source_license, source_reference, active |
| question_exposures | id, user_id, question_id, attempt_id, exposed_at; UNIQUE(user_id, question_id) |
| study_tracks | id, user_id, mode, focus_subject, start_date, syllabus_version, status |
| track_days | id, track_id, local_date, weekday, topic_id, state, attempt_count |
| topic_progress | id, user_id, topic_id, status, attempts, passed_at, easy_revision_suggested; UNIQUE(user_id, topic_id) |
| test_attempts | id, user_id, topic_id, track_day_id, attempt_no, question_ids, started_at, submitted_at, score, passed, mode, expires_at |
| attempt_answers | id, attempt_id, question_id, response_json, is_correct, time_seconds |
| weekly_exams | id, user_id, track_id, week_start, question_ids, submitted_at, correct_count, marks, passed, mode |
| mistake_notebook | id, user_id, question_id, attempt_id, response_json, reviewed_at |
| pause_tokens | id, user_id, month_key, used_at; UNIQUE(user_id, month_key) |
| mock_pause_windows | id, start_date, end_date, reason, created_by, approved_at |
| squads | id, name, class_level, target_exam, timezone, status, created_at |
| squad_members | id, squad_id, user_id, role, active, joined_at; UNIQUE(squad_id,user_id) |
| squad_challenges | id, squad_id, week_no, challenge_type, config_json, state, result_json |
| checkins | id, squad_id, starts_at, meeting_url, agenda_json |
| doubt_cards | id, squad_id, author_id, topic_id, question_text, attempt_summary, image_key, status, created_at |
| doubt_replies | id, doubt_card_id, author_id, body, moderation_status |
| reports | id, reporter_id, target_type, target_id, reason, status, moderator_id, created_at |
| blocks | blocker_id, blocked_id, created_at; UNIQUE(blocker_id,blocked_id) |
| notifications | id, user_id, type, payload_json, scheduled_at, sent_at, status |
| audit_logs | id, actor_id, action, entity_type, entity_id, metadata_json, created_at |

Indexes: question(topic_id,difficulty,active); attempt(user_id,topic_id,started_at); exposure(user_id,question_id) unique; squad_members(squad_id,active); notifications(user_id,status,scheduled_at). Use DB transactions and row-level locking when issuing tests to prevent duplicate sets from concurrent requests.

## 5. API endpoints

All routes versioned under /api/v1. Auth uses short-lived access tokens + rotating refresh tokens; OTP provider integration is mandatory before public release.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /auth/otp/request | Send OTP; rate-limited |
| POST | /auth/otp/verify | Verify OTP and create session |
| POST | /consents/guardian | Create guardian consent request |
| POST | /consents/guardian/verify | Confirm guardian consent |
| GET/PATCH | /me | Profile read/update |
| POST | /onboarding/complete | Save preferences and diagnostic |
| GET | /curriculum | Subjects/chapters/topics |
| GET | /tracks/current | Current weekly track |
| POST | /tracks | Create Balanced/Focus track |
| GET | /today | Today’s topic and state |
| GET | /topics/{id} | Notes, formula, key points, resource |
| POST | /topics/{id}/daily-tests | Issue unseen 7-question set |
| POST | /attempts/{id}/submit | Submit exactly 7 answers |
| GET | /attempts/{id}/result | Solutions and result |
| GET | /revision/current | Saturday revision pack |
| POST | /weekly-exams | Issue 25-question exam |
| POST | /weekly-exams/{id}/submit | Submit exam |
| GET | /mistakes | Mistake Notebook |
| PATCH | /mistakes/{id} | Mark reviewed |
| POST | /pause-tokens/redeem | Redeem monthly token |
| GET | /progress | Personal metrics |
| GET | /squads/current | Squad and member status |
| POST | /squads/match | Enter matching queue |
| POST | /doubt-cards | Create structured doubt |
| POST | /doubt-cards/{id}/replies | Reply in squad |
| POST | /reports | Report content/user |
| POST | /blocks | Block member |
| GET | /challenges/current | Weekly challenge |
| POST | /checkins | Schedule squad check-in |
| GET | /notifications | Notification preferences/history |
| POST | /admin/questions/import | CSV validation/import |
| CRUD | /admin/curriculum | Manage syllabus |
| CRUD | /admin/squads | Manage squad lifecycle |
| GET | /admin/metrics | Aggregate product metrics |
| GET/PATCH | /admin/reports | Moderation queue |

Never return answer_json or solution_md before the attempt is submitted. Use opaque attempt IDs and validate ownership on every route.

## 6. Core logic pseudocode

### Daily test issue
```text
assert learner consent is approved
assert track day is today's pending topic (or permitted catch-up)
lock learner+topic progression row
seen = all question IDs previously exposed to learner for topic
pool = active, licensed questions where topic_id and id not in seen
select 3 EASY + 3 MEDIUM + 1 HARD (Advanced-style)
if any difficulty pool insufficient: return CONTENT_BANK_LOW; notify admin; do not reuse
shuffle question order and option order; persist immutable issued set + expiry
persist exposure records in same transaction
return prompt/options only
```

### Daily submission
```text
load attempt FOR UPDATE; verify owner, not submitted, not expired
assert submitted question IDs exactly equal issued IDs
score server-side from canonical answer JSON
save answers; save every incorrect response to Mistake Notebook
if correct_count >= 5: mark topic PASSED; unlock next scheduled topic
else: increment attempt; keep same topic pending; next attempt must use unseen set
if attempts >= 3: set easy_revision_suggested = true
mark attempt submitted; commit once (idempotency key prevents double-submit)
```

### Unlock / missed day / Sunday failure
```text
if day is declared mock/board pause: show light revision; don't consume topic
elif day missed: if pause token redeemed, preserve streak; else mark MISSED and hold pending topic
elif daily test passed: next topic becomes eligible
elif failed: same topic repeats next study day
on Sunday:
  if correct >= 20: close week; unlock next week
  else: repeat same weekly topic plan; set recovery mode; cap squad penalty
  never delete mastered topics or reduce personal historical progress
```

### Squad matching
```text
candidates = waiting learners
partition by class, compatible target, timezone overlap, preferred slot
for each candidate group:
  build squads of 4..6
  score combinations:
    + level proximity
    + complementary subject strengths/weaknesses
    + optional opted-in city/coaching compatibility
    - duplicate weak-subject clusters
  choose highest balanced combination; persist match reason codes
if fewer than 4 compatible learners: keep queue; offer solo track
```

### Challenge engine
```text
challenge_type = rotation[(week_number - 1) mod 4] for weeks 1..4
for week >= 5 rotate teach-back, PYQ hunt, speed round, mistake swap, revision relay
calculate only from verified activity; minimum participation threshold applies
show squad-only outcome and personal contribution; no public/global rank
```

### Edge-case policies
- Timezone change: future study days recomputed; already issued tests retain their original expiry and timezone snapshot.
- Question exhaustion: block issue and admin-alert; do not lower mix or recycle.
- Concurrent start: transaction lock + one active attempt per user/topic/day.
- Cheating: timer, shuffled options, server-side scoring, one submission, randomized bank. Do not use invasive surveillance or webcam proctoring.
- Offline: cache notes and issued question prompts; queue answers locally with signed attempt token; submit when connected before expiry. If server never received issue token, do not accept guessed question IDs.
- Inactive squad: 7-day nudge, 14-day review, replace/merge with consent; preserve all learning history.
- Repeated Sunday failure: supportive repeat week, recovery plan, optional mentor/counsellor guidance; no escalating punishment.
- Duplicate question: content fingerprint + normalized prompt check during import.

## 7. Screen-by-screen UI description

Global design: calm dark navy/charcoal option, high-contrast light mode, large tap targets, no infinite feed, no ads in test flow. KaTeX for math; MathJax fallback for complex expressions. Use SVG/PNG/WebP diagrams and chemistry structure images with alt text. Low-bandwidth default: text-first notes, compressed images, video is external optional link.

1. Splash: logo, “Progress over perfection”, sign-in.
2. OTP: phone input, resend cooldown, accessible error.
3. Consent: age band, guardian consent status and explanation.
4. Onboarding: class, exam target, confidence sliders, daily hours, slot, language.
5. Home: today’s topic card, gate status, seven-question CTA, streak, squad check-in.
6. Topic: short notes, formula blocks, key points, one video link, “Start 7-question test”.
7. Daily Test: one question per view, progress 1/7, timer, flag-for-review, autosave, submit confirmation.
8. Result: score /7, pass state, each answer with solution and common mistake, next action.
9. Weekly Revision: tabs for formulas, concept map, key points, common mistakes, saved mistakes; no test CTA.
10. Weekly Exam: 25-question progress, exam-mode toggle and marking preview, timer, submit.
11. Mistake Notebook: filters by subject/chapter/date, review solution, mark reviewed.
12. Squad: 4–6 initials/avatars (generated abstract icons only), member progress states, check-in, challenge, no likes or chat feed.
13. Doubt Card: topic, text/image optional, “what I tried”, report action, threaded answers.
14. Challenge: weekly type, rules, participation and squad-only progress.
15. Progress: personal trend chart, subject accuracy, weak chapters, time/question.
16. Profile: class, target, schedule, preferences; no public profile or profile photo.
17. Settings: quiet hours, timezone, language, privacy, consent, block/report, export/delete account.
18. Admin: curriculum editor, CSV preview/validation, question bank coverage, squad manager, moderation, analytics.

## 8. Sample 1-week JEE content plan + sample question bank (CSV)

Class 11 sample Balanced track:
- Monday Physics — Kinematics: displacement, velocity, acceleration, equations of motion.
- Tuesday Chemistry (Physical) — Mole Concept: mole, molar mass, Avogadro constant, empirical composition.
- Wednesday Mathematics — Sets and Relations: set operations, subsets, Cartesian product, relation basics.
- Thursday Physics — Kinematics: graphs and relative motion (topic depends on Monday mastery; if Monday failed, repeat Monday topic).
- Friday Chemistry (Physical) — Mole Concept: limiting reagent and concentration (topic depends on Tuesday mastery).
- Saturday — revise all completed topics: formula sheet, concept map, key mistakes; no test.
- Sunday — 25-question weekly exam across completed topics; 20/25 to pass.

Important scheduling note: the sample bank below contains 7 original Kinematics questions to demonstrate the CSV shape. It is NOT production-ready: each schedulable topic must have at least 30 active questions and enough unseen items per learner.

CSV schema:
```csv
question_key,subject,chapter,topic,difficulty,exam_level,question_type,prompt,option_a,option_b,option_c,option_d,answer,solution,common_mistake,pyq_year,concept_tags,source_license
```
Allowed question_type: SINGLE_CORRECT, MULTIPLE_CORRECT, NUMERICAL. For MULTIPLE_CORRECT, answer is a semicolon-separated canonical option key list; production import should store it as JSON array. For NUMERICAL, answer stores a numeric tolerance rule in JSON in production. Blank PYQ year means original/non-PYQ. Never label an original question as a PYQ.

Sample CSV is stored at `content/sample_questions.csv`. All sample items are original illustrative content, not official PYQs. It includes 7 Kinematics questions, including a numerical item. Admin import should reject the file until the schema includes exam_level and canonical answer JSON; the sample file is a human-readable example and needs normalization before import.

## 9. Tech stack and architecture

**Recommended stack**
- Student app: Next.js responsive PWA + TypeScript; installable, fast iteration, shared components with admin.
- API: FastAPI + SQLAlchemy; concise Python implementation, easy content tooling and analytics.
- Data: PostgreSQL + Redis + Firebase Cloud Messaging; durable relational progression, caching/queues and push delivery.

For the first working prototype SQLite is permitted locally; production must use PostgreSQL. Use object storage (S3-compatible) for doubt images, with private signed URLs. Use KaTeX for math rendering.

Architecture:
```text
Next.js PWA (student + admin)
   | HTTPS / JWT
FastAPI API
   |-- Auth/Consent
   |-- Curriculum/Content
   |-- Test & Progression Engine
   |-- Squad/Challenge
   |-- Moderation/Notifications
   |
PostgreSQL ---- Redis queue/cache
   |                 |
Object storage     FCM worker
```

Production essentials: HTTPS, secrets manager, migrations (Alembic), structured logs, error monitoring, rate limits, backups, restore drills, audit logs, CI tests and staging environment. Do not ship the development OTP endpoint as real authentication.

## 10. Revenue model and projection

Free: one squad, core loop for one subject track, basic Mistake Notebook and personal progress.
Premium: ₹99–299/month for all three subjects, advanced analytics, Advanced question sets, premium challenges and safeguarded mentor sessions.
B2B: institute license per active student with cohort dashboard, curriculum mapping and parent reports only with appropriate consent.

Illustrative institute model (not a forecast):
- 500 enrolled students.
- Assume 70% paid/active licensed seats = 350 billable seats.
- Assumed negotiated rate = ₹120/student/month.
- Monthly gross revenue = 350 × ₹120 = ₹42,000.
- Annual gross revenue = ₹5,04,000.
- If 15% is reserved for payment/tax/support/hosting and service costs, illustrative contribution before salaries/sales = ₹35,700/month.
- At 500 paid seats the same rate yields ₹60,000/month gross.
These figures are planning assumptions only; validate willingness-to-pay, taxes, institute procurement and mentor costs before pricing.

## 11. 3-week pilot plan and metrics

Pilot: 15–20 learners, ideally Class 11 or droppers. Use Google Forms for question delivery, a simple spreadsheet for progression and WhatsApp only as a temporary squad coordination channel. Avoid sharing minors' phone numbers or adding them to groups without guardian-aware consent; use moderated groups and no private adult-minor DMs.

Week 1 — baseline and habit:
- Day 0: consent, onboarding, diagnostic, squad formation.
- Days 1–5: one topic/day, 7 questions/day, track completion and reasons for misses.
- Saturday revision pack; Sunday 25-question exam.
Week 2 — repeatability:
- Run second track; introduce challenge rotation and Mistake Notebook.
- Conduct 20-minute check-in; interview learners about pressure and usefulness.
Week 3 — willingness to continue:
- Repeat loop; test premium price cards (₹99/₹199/₹299) without collecting money.
- Interview students and guardians; audit safety and moderation.

Metrics and go/no-go:
- Day-7 retention: GO ≥50%; iterate 30–49%; NO-GO <30%.
- Sunday exam completion: GO ≥65%; iterate 40–64%; NO-GO <40%.
- Squad check-in attendance: GO ≥60% of active members; iterate 35–59%; NO-GO <35%.
- Willingness to pay: GO ≥25% choose ₹99+; iterate 10–24%; NO-GO <10%.
- Also monitor median test completion time, topic pass rate, question-quality flags, squad match wait time and wellbeing feedback. Any serious safety/privacy incident pauses the pilot regardless of engagement.

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Cold start / small cohorts | Start one class + one timezone + one slot; solo mode while waiting; manually curate first squads. |
| Content workload | Start with one topic per subject; author 30+ questions/topic; question templates, review workflow, versioning and licensing metadata. |
| Burnout / exam stress | One topic/day, quiet hours, optional pauses, gentle retry, light mock weeks, no public ranks or escalating financial penalty. |
| Minors' privacy | Guardian consent, minimal data, no profile photos/open DMs, private squads, block/report, retention and deletion workflow; legal review before launch. |
| Cheating | Unique unseen sets, server-side scoring, timer, shuffled options, one submission, audit anomalies; no invasive webcam monitoring. |
| Repeated failure dropout | Easy Revision Mode after 3 fails, worked examples, smaller steps, optional human support and non-shaming copy. |
| Copyright | Original/licensed question bank only, source/license field, upload attestation, takedown process, no copied coaching sheets or textbook solutions. |
| Competition from PW/Allen/Unacademy | Do not compete on lecture volume. Differentiate on mastery gates, squad accountability, personal mistake loops and small weekly commitments. |
| Squad inactivity/toxicity | Activity thresholds, moderation, block/report, merge/replace workflow and no open feed. |
| Poor network | Text-first pages, compressed diagrams, cached notes, offline answer queue and graceful retry. |

## 13. 30/60/90-day roadmap

**Days 1–30 — validate the loop**
- Build auth/consent shell, onboarding, curriculum admin, daily topic, seven-question test, result and Mistake Notebook.
- Seed 3 topics with 30+ reviewed questions each before opening those topics.
- Run 15–20 learner pilot; instrument retention, test completion and failure recovery.
- Exit: no critical safety issues; day-7 retention ≥50%; Sunday completion ≥65%.

**Days 31–60 — squads and weekly progression**
- Add squad matching, check-ins, Doubt Cards, challenge rotation, Saturday revision, Sunday exam and pause token.
- Add admin moderation and CSV import validation.
- Exit: squads average 4 active members, check-in attendance ≥60%, repeat-attempt question freshness verified.

**Days 61–90 — controlled institute beta**
- PostgreSQL production, FCM, analytics, institute admin, consent operations, security review and backup restore drill.
- Pilot with one institute cohort; test B2B pricing and guardian reporting.
- Exit: reliable test issuance, no question repeats per learner/topic, clear willingness-to-pay and signed institute pilot intent.

## 14. Starter code: backend models + unlock logic + daily test submit API

A runnable starter is in `backend/app/`. It includes SQLAlchemy models for users, topics, questions, topic progress, attempts, answer records, Mistake Notebook, pause tokens, squads and Doubt Cards; question selection; and daily test issue/submit endpoints.

Run locally:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Before public deployment, complete these blockers:**
1. Replace dev user creation with verified OTP + rate limiting + abuse controls.
2. Implement guardian consent verification and consent withdrawal.
3. Add Alembic migrations, PostgreSQL, row locks, idempotency keys and test expiry enforcement.
4. Add weekly exam issue/submit, schedule/calendar, pause token, squad matching, challenge, notifications and admin APIs.
5. Add proper canonical answer schemas for multi-correct/numerical tolerance and JEE exam marking.
6. Add automated tests for pass/fail, exact 7/25 count, unseen selection, exhaustion, timezone and concurrent issuance.
7. Add moderation, report/block, deletion/export and operational safety workflows.

The scaffold is an MVP foundation, not a production-ready release. The API intentionally refuses to issue tests until consent_status is APPROVED.
