# CS238 Peer Reviews
Repo that contains all the files for handling the peer reviews for the CS238 final project.

## Setup

First, download the submissions from Gradescope by selecting the "Export submissions" button at the bottom of the screen from the "Review Grades" tab for the assignment. **Note:** If you are running this for a large class, make sure you have enough storage to download all of the assignments from Gradescope.

Then unzip the downloaded file. You'll see a bunch of folders for each submission and a `submission_metadata.csv` file.

## Step 1: Run Peer Review Assignment (Pass 1)

Run `parse_data.py` with run number `1` to assign peer reviews:

```bash
uv run parse_data.py [csv file path] [submissions folder path] [peer review folder 1] [peer review folder 2] [run number]
```

Example:
```bash
uv run parse_data.py ./assignment_export/submission_metadata.csv ./assignment_export/ pr_1/ pr_2/ 1
```

**Pass 1** assigns each student two projects to peer review while avoiding:
- Students reviewing their own projects
- Students reviewing the same project twice

The script will:
- Prompt you to select a file when a student has multiple submissions
- Display the total number of assignments
- Show which projects are exempt from review
- Alert you if any students are assigned to review the same project twice

**Important:** Verify the summary matches Gradescope for the number of projects submitted and make any manual adjustments if students submitted wrong information.

This pass generates:
- `Peer_review_assignments.csv` - Assignments for students
- `Publishable_Projects.csv` - Projects with permission to publish
- `processed_project_files/` - Renamed project files

## Step 2: Generate Master Assignments (Pass 2)

Run `parse_data.py` with run number `2` to create the master assignment list:

```bash
uv run parse_data.py ./assignment_export/submission_metadata.csv ./assignment_export/ pr_1/ pr_2/ 2
```

**Pass 2** generates `Peer_review_assignments_master.csv` containing detailed information about all peer review assignments including student IDs, names, emails, and their assigned projects.

## Step 3: Return Peer Reviews (Pass 3)

After collecting peer review submissions from Gradescope, run `parse_data.py` with run number `3` to compile and return reviews:

```bash
uv run parse_data.py ./assignment_export/submission_metadata.csv ./assignment_export/ pr_1/ pr_2/ 3
```

**Pass 3** collects all peer review submissions and combines them into individual PDFs for each project. This script:
- Reads peer review metadata from both peer review folders
- Combines all reviews for each project into a single PDF
- Generates `Peer_Reviews_Returned.csv` with filenames for distribution
- Creates `processed_peer_reviews/` folder with combined review PDFs

Students receive a single PDF containing all peer reviews of their project.
