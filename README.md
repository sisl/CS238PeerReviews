# CS238 / AA222 Peer Reviews

Repo that contains all the files for handling the peer reviews for the CS238/AA222 final project.

## AA222 2026 updates

This branch was updated for the Spring 2026 Gradescope assignment layout. Key changes from earlier versions:

- **Question mapping** — uses Q1 (title), Q7 (publish), and Q8 (peer review opt-out); see table below. Q2–Q5 author emails are not used.
- **Student roster** — reads the `Name` column from Gradescope exports (not `First Name` / `Last Name`).
- **Group members** — authorship comes from Gradescope tagging (one CSV row per tagged student, grouped by `Submission ID`), not from author email fields.
- **Pass 3 PDF extraction** — current Gradescope peer review exports put the grade summary on page 0 and the uploaded review on pages 1+ (as images). The script skips the grade page and extracts only the submitted review pages.
- **Peer review folders** — point args 3 and 4 at the unzipped Gradescope export folder (the one containing `submission_metadata.yml`), not the outer wrapper folder.

## Gradescope final project questions

The script reads these questions from `submission_metadata.csv`:

HIGHLY recommend you make students answer a tagging question, or else untagged teammates will not receive peer review submissions. 


| Question | Prompt                                | Used by script                              |
| -------- | ------------------------------------- | ------------------------------------------- |
| Q1       | Project Title                         | Yes — project title                         |
| Q2       | Author 1 Stanford Email               | No — tagging used instead                   |
| Q3       | Author 2 Stanford Email               | No                                          |
| Q4       | Author 3 Stanford Email               | No                                          |
| Q5       | Author 4 Stanford Email               | No                                          |
| Q6       | Tagging Group Members                 | No (students must tag on Gradescope)        |
| Q7       | Permission to Share on Course Website | Yes — `Publishable_Projects.csv`            |
| Q8       | Peer Review Exclusion                 | Yes — exempt projects skip peer review      |
| Q9       | File Upload (.pdf or .mp4)            | No — files read from `submission_`* folders |
| Q10      | Group Contributions                   | No                                          |
| Q11      | Tagging Group Members (again)         | No                                          |


## Setup

### Python environment

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy pypdf2 pyyaml
```

(`uv run` also works if you have [uv](https://docs.astral.sh/uv/) installed.)

### Final project export

Download submissions from Gradescope via **Review Grades → Export submissions** at the bottom of the page. Unzip the download — you should see `submission_metadata.csv` and a `submission_`* folder for each submission.

Suggested layout:

```
CS238PeerReviews/
├── assignment_export/
│   ├── submission_metadata.csv
│   └── submission_*/
├── pr_1/                          # peer review round 1 export (after reviews collected)
├── pr_2/                          # peer review round 2 export
└── parse_data.py
```

## Step 1: Run Peer Review Assignment (Pass 1)

```bash
python parse_data.py [csv file path] [submissions folder path] [peer review folder 1] [peer review folder 2] [run number]
```

Example:

```bash
python parse_data.py ./assignment_8024588_export/submission_metadata.csv ./assignment_8024588_export/ pr_1/ pr_2/ 1
```

**Pass 1** assigns each student two projects to peer review while avoiding:

- Students reviewing their own projects
- Students reviewing the same project twice

The script will:

- Prompt you to select a file when a submission folder has multiple files
- Display the total number of projects and how many are exempt
- Alert you if any students are assigned to review the same project twice

**Important:** Verify the summary matches Gradescope for the number of projects submitted and make any manual adjustments if students submitted wrong information.

**Generates:**

- `Peer_review_assignments.csv` — assignments for students (for Gradescope upload)
- `Publishable_Projects.csv` — projects with Q7 = Yes
- `processed_project_files/` — renamed project files (`001.pdf`, `002.mp4`, …)
- `master_assignments.pkl` — saved assignments (required for Pass 2 and 3)
- `filtered_roster_for_finalprojects.csv` — intermediate filtered export

## Step 2: Generate Master Assignments (Pass 2)

Requires `master_assignments.pkl` from Pass 1.

```bash
python parse_data.py ./assignment_8024588_export/submission_metadata.csv ./assignment_8024588_export/ pr_1/ pr_2/ 2
```

**Generates:** `Peer_review_assignments_master.csv` with student IDs, names, emails, and assigned project titles/paths.

Pass 3 does not depend on Pass 2.

## Step 3: Return Peer Reviews (Pass 3)

After both peer review rounds close, export each peer review assignment from Gradescope and place the unzipped exports in `pr_1/` and `pr_2/`. Each folder must contain `submission_metadata.yml` and the review PDFs.

Requires `master_assignments.pkl` from Pass 1.

```bash
python parse_data.py ./assignment_8024588_export/submission_metadata.csv ./assignment_8024588_export/ ./pr_1/assignment_export/ ./pr_2/assignment_export/ 3
```

Adjust the `pr_1` and `pr_2` paths to wherever your Gradescope export folders live (the directory that directly contains `submission_metadata.yml`).

**Pass 3:**

- Matches each review submitter's email to their Pass 1 assignment
- Extracts uploaded review pages from each Gradescope PDF (skips the grade summary on page 0)
- Combines all reviews for each project into one PDF

**Generates:**

- `processed_peer_reviews/` — one PDF per project, e.g. `5_peer_reviews.pdf`
- `Peer_Reviews_Returned.csv` — project title → filename mapping for distribution

Students receive a single PDF containing all peer reviews of their project. Exempt projects (Q8 = Yes) are not included.

## Troubleshooting

### `uv: command not found`

The README examples work with a regular venv. Use:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy pypdf2 pyyaml
python parse_data.py ...
```

### `KeyError: 'First Name'` or wrong publish/exempt counts

The script expects the **2026 Gradescope export format** (`Name` column; Q7 = publish, Q8 = opt-out). If you see publish permissions or exemptions that don't match Gradescope, check that you're on the updated `parse_data.py` and the question mapping table above.

### `FileNotFoundError: submission_metadata.yml` (Pass 3)

Gradescope exports are often nested one level deep. Point args 3 and 4 at the folder that **directly contains** `submission_metadata.yml`, not the outer wrapper:

```bash
# Wrong
./pr_1/

# Right (example)
./pr_1/assignment_8204190_export/
```

Check with:

```bash
ls ./pr_1/*/submission_metadata.yml
```

### Pass 3 PDFs are blank

Older versions of the script extracted the wrong pages from Gradescope peer review PDFs. In the 2026 export format:

- **Page 0** — Gradescope grade summary (not the student's review)
- **Pages 1+** — uploaded review content (usually as page images)

If combined PDFs are blank or only show grades, make sure you're on the current `parse_data.py` and re-run Pass 3.

### Pass 3 PDFs show grades but not submitted reviews

Same root cause as above — page 0 was extracted instead of pages 1+. Re-run Pass 3 after updating the script.

### `master_assignments.pkl` not found (Pass 2 or 3)

Run Pass 1 first from the repo root. Pass 2 and 3 load saved assignments from `master_assignments.pkl`; they do not recompute assignments from scratch.

### Multiple files in submission folder (Pass 1)

If a `submission_*` folder contains more than one file, the script pauses and asks you to pick one. Choose the actual project report/video, not a duplicate or draft.

### Project count doesn't match Gradescope

Compare Pass 1 output (`125 total`, `121 part of peer review`, `4 exempt`) against Gradescope. Common causes:

- **Q8 = Yes** — project is exempt from receiving reviews (but authors still review others)
- **Missing submission file** — script prints `Submission {id} has no files`
- **Untagged group members** — each tagged student gets a CSV row; untagged teammates won't appear as authors

### Group member not getting assignments / could review own project

The script identifies authors from **Gradescope tagging**, not Q2–Q5 emails. If a teammate wasn't tagged on the submission, they won't be linked to the project for self-review avoidance. Strongly encourage tagging (Q6/Q11).

### Email warnings during Pass 3

```
Warning: no roster match for peer review submitter ...
```

The reviewer's Gradescope email must match their email in the original project export. Check for typos, alias addresses, or students who submitted under a different account.

### Missing reviews in a combined PDF

If a student didn't submit one or both peer reviews, their review simply won't appear in that project's PDF. The CSV and filenames are still correct — the combined PDF just has fewer pages.

### Exempt project not in `Peer_Reviews_Returned.csv`

Expected. Projects with Q8 = Yes are excluded from peer review distribution (typically 4 out of 125 in 2026). Those students still complete their own assigned reviews.

### `Peer_Reviews_Returned.csv` vs `processed_peer_reviews/`

These should match 1:1 — each CSV row's `Peer Reviews Filename` should exist in `processed_peer_reviews/`. Filenames use the Pass 1 project number: `{id}_peer_reviews.pdf` (e.g. project 5 → `5_peer_reviews.pdf`).
