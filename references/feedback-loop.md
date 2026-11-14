# Feedback loop (ফিডব্যাক ও দ্বিতীয় রাউন্ড)

## Scoring

- **MCQ:** 1 mark per correct answer, no negative marking unless the student's exam has it (ask).
- **CQ:** the student self-marks each part against the model answer and marking note, or pastes their answer and you mark it part by part. Be honest and specific: say which mark was lost and why.

## Topic status

| Topic score | Status | Meaning |
|---|---|---|
| below 60% | দুর্বল (weak) | Needs re-teaching, then more practice |
| 60% to 80% | মোটামুটি (okay) | A little more practice |
| above 80% | ভালো (strong) | Light revision only |

If a topic has only one or two questions, call the result "early signal", not a verdict.

## Error types (ask or infer, then name them)

1. জ্ঞানের ঘাটতি: did not know the concept
2. প্রশ্ন ভুল পড়া: misread the question
3. হিসাব ভুল: arithmetic or unit slip
4. সূত্র ভুল: wrong formula
5. সময়ের চাপ: ran out of time
6. উদ্দীপক ব্যবহার করেনি: answered ঘ without using the stimulus

Give a one-line fix for the main error type (for example: "ঘ লেখার আগে উদ্দীপক থেকে দুটি তথ্য আগে লিখে নাও").

## Cognitive-level view (CQ)

Report marks by level (জ্ঞান, অনুধাবন, প্রয়োগ, উচ্চতর দক্ষতা). Typical pattern: strong on জ্ঞান, weak on প্রয়োগ. Say so, and tell the student what to practise.

## Round 2 composition

| Share | From |
|---|---|
| 60% | Weak topics |
| 25% | Okay topics |
| 15% | Strong topics (confidence builders) |

- Use **new** questions on the same concepts, not repeats of the wrong ones.
- Keep it short: 10 MCQs and 1 CQ, or less if time is tight.
- After round 2, show the change: "প্রথম রাউন্ডে ৫০%, এখন ৭০%".
- Stop at two rounds late at night. Encourage sleep.

## Report template

```
ফলাফল: MCQ ১৪/২০ | CQ ২১/৩০ | মোট ৩৫/৫০ (৭০%)

অধ্যায়/টপিক অনুযায়ী:
- <topic>: ৩/৫ (দুর্বল)
- ...

সবচেয়ে দুর্বল ৩টি: ১) ... ২) ... ৩) ...

যা ভুল হয়েছে (সংক্ষেপে): ...

পরের রাউন্ড: দুর্বল টপিক থেকে ১০টি MCQ + ১টি CQ। শুরু করব?
```

`scripts/score_quiz.py` produces this report for JSON quizzes.
