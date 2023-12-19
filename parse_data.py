import pandas as pd
from glob import glob
from copy import copy
import shutil
import numpy as np
import random
import pickle
import sys
import yaml
from PyPDF2 import PdfWriter, PdfReader
sys.setrecursionlimit(300000)
random.seed(227)

roster_filename = "updated_AA228_Fall_2023_roster.csv" #TODO: remember to change
projects_filename = "/Users/jennyyang/Downloads/organized_submissions/real_updated_csvfile.csv"

class Student(object):
    def __init__(self,first_name,last_name,sid,email,section) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.sid = sid
        self.email = email
        self.section = section
        self.peer_review_1 = None
        self.peer_review_2 = None

    def __str__(self):
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"sid: {self.sid}")
        print(f"Email: {self.email}")
        # print(f"Peer Review 1: {self.peer_review_1}")
        # print(f"Peer Review 2: {self.peer_review_2}")
        return ""

class Project(object):
    def __init__(self,project_id, filename, title, auth_1, auth_2, auth_3, auth_4, permission_to_publish, pr_exemption) -> None:
        self.project_id = project_id
        self.filename = filename
        self.title = title
        self.auth_1 = auth_1
        self.auth_2 = auth_2
        self.auth_3 = auth_3
        self.auth_4 = auth_4
        self.permission_to_publish = permission_to_publish
        self.pr_exemption = pr_exemption
    
    def __str__(self):
        print(f"Project ID: {self.project_id}")
        print(f"filename: {self.filename}")
        print(f"Author 1: {self.auth_1.first_name} {self.auth_1.last_name}")
        if self.auth_2 is not None:
            print(f"Author 2: {self.auth_2.first_name} {self.auth_2.last_name}")
        if self.auth_3 is not None:
            print(f"Author 3: {self.auth_3.first_name} {self.auth_3.last_name}")
        if self.auth_4 is not None:
            print(f"Author 4: {self.auth_4.first_name} {self.auth_4.last_name}")
        print(f"Permission to publish: {self.permission_to_publish}")
        print(f"Peer Review Exemption: {self.pr_exemption}")
        return ""

class PeerReview(object):
    def __init__(self,filename, auth, project) -> None:
        self.filename = filename
        self.auth = auth
        self.project = project
    
    def __str__(self):
        print(f"filename: {self.filename}")
        print(f"Project: {self.project.title}")
        print(f"Author: {self.auth.first_name} {self.auth.last_name}")
        return ""


def get_student_list():
    student_list = []
    df = pd.read_csv(roster_filename)
    for i in range(len(df)):
        first_name = df.iloc[i]["First Name"]
        last_name = df.iloc[i]["Last Name"]
        sid = str(int(df.iloc[i]["SID"]))
        email = df.iloc[i]["Email"]
        section = df.iloc[i]["Section"]
        student_list.append(Student(first_name,last_name,sid,email,section))
    
    return student_list

def find_student_by_email(email,student_list):
    student = None
    if pd.isna(email):
        return None

    # print('all emails',email)
    email = email.rstrip()

    for s in student_list:
        # print(s.email)
        if s.email==email:
            student = s
            return student

    if student is None:
        # TODO: FIGURE OUT WHAT'S GOING ON HERE.
        print("email", email)
        # raise NotImplementedError

# def find_student_by_sid(sid,student_list):
#     student = None
#     stripped_sid = str(int(sid))
#     for s in student_list:
#         if s.sid==stripped_sid:
#             student = s
#             return student

#     if student is None:
#         raise NotImplementedError
    
        

def get_projects_list(students_list):
    projects_list = []
    seen_projects = set()
    # TODO: REMOVE SEEN PROJECTS?
    df = pd.read_csv(projects_filename)
    df.rename(columns={'Question 1 Response': 'project_title'}, inplace=True)
    df.rename(columns={'Question 3 Response': 'publish'}, inplace=True)
    df.rename(columns={'Question 4 Response': 'pr_exemption'}, inplace=True)
    df.rename(columns={'Question 2.1 Response': 'auth_1_email'}, inplace=True)
    df.rename(columns={'Question 2.2 Response': 'auth_2_email'}, inplace=True)
    df.rename(columns={'Question 2.3 Response': 'auth_3_email'}, inplace=True)
    df.rename(columns={'Question 2.4 Response': 'auth_4_email'}, inplace=True)

    for i in range(len(df)):
        if pd.isna(df.iloc[i]["project_id"]):
            continue

        project_id = str(int(df.iloc[i]["project_id"])).zfill(3)
        if project_id in seen_projects:
            continue
        project_title = df.iloc[i]["project_title"]
        if df.iloc[i]["publish"] == "Yes":
            permission_publish = True
        else:
            permission_publish = False
        if df.iloc[i]["pr_exemption"] == "Yes":
            pr_exemption = True
        else:
            pr_exemption = False

        #find_author 1
        auth_1_email = df.iloc[i]["auth_1_email"]
        s1 = find_student_by_email(auth_1_email,students_list)

        #find_author 2
        auth_2_email = df.iloc[i]["auth_2_email"]
        s2 = find_student_by_email(auth_2_email,students_list)

        #find_author 3
        auth_3_email = df.iloc[i]["auth_3_email"]
        s3 = find_student_by_email(auth_3_email,students_list)

        #find_author 4
        auth_4_email = df.iloc[i]["auth_4_email"]
        s4 = find_student_by_email(auth_4_email,students_list)

        #find file
        res = glob("/Users/jennyyang/Downloads/organized_submissions/"+project_id+"*")
        
        # if project_id=="136":
        #     filename = None
        if len(res) != 1:
            raise NotImplementedError
        else:
            filename = res[0].split("/")[-1]
        
        seen_projects.add(project_id)
        projects_list.append(Project(project_id,filename,project_title,s1,s2,s3,s4,permission_publish,pr_exemption))

    return projects_list

def get_peer_review_list(student_list, projects_list, pr_metadata,peer_review_number):
    files = list(pr_metadata.keys())
    pr_list = []
    for f in files:
        """Need filename, author, and project"""
        #get author from email
        submission_email = pr_metadata[f][":submitters"][0][":email"]
        student = find_student_by_email(submission_email,student_list)
        if peer_review_number == 1:
            project = student.peer_review_1
        elif peer_review_number ==2:
            project = student.peer_review_2
        else:
            raise NotImplementedError
        pr_list.append(PeerReview(f,student,project))
    
    return pr_list

def assign_peer_reviews(student_list,projects_list):
    """
    Avoid:
    - not same assignemnt twice
    - not own project
    """
    print("pre filter length of projects", len(projects_list))
    #ONLY CONSIDER PROJECTS THAT ARE OK WITH PEER REVIEW
    filtered_projects_list = []
    for p in projects_list:
        if not p.pr_exemption:
            filtered_projects_list.append(p)
    projects_list = list(set(filtered_projects_list))
    # if len(projects_list) <= 3:
    #     raise NotImplementedError
    
    print("length of projects", len(projects_list))
    current_projects_list = copy(projects_list)
    next_projects_list = copy(projects_list)
    # last_projects_list = copy(projects_list)

    for s in student_list:
        # print(len(current_projects_list))
        # print(len(next_projects_list))

        #peer review 1
        #check authorship 
        if len(current_projects_list) > 1:
            assigned = False
            while not assigned:
                random.shuffle(current_projects_list)

                if not np.any([current_projects_list[0].auth_1 == s, current_projects_list[0].auth_2 == s, current_projects_list[0].auth_3 == s, current_projects_list[0].auth_4 == s]):
                    project = current_projects_list.pop(0)
                    s.peer_review_1 = project
                    assigned = True

        elif not np.any([current_projects_list[0].auth_1 == s, current_projects_list[0].auth_2 == s, current_projects_list[0].auth_3 == s, current_projects_list[0].auth_4 == s]):
            project = current_projects_list.pop(0)
            s.peer_review_1 = project
            assigned = True
        
        else:
            assigned = False
            while not assigned:
                random.shuffle(next_projects_list)

                if not np.any([next_projects_list[0].auth_1 == s, next_projects_list[0].auth_2 == s, next_projects_list[0].auth_3 == s, next_projects_list[0].auth_4 == s]):
                    project = next_projects_list.pop(0)
                    s.peer_review_1 = project
                    assigned = True
        
        # elif not np.any([next_projects_list[0].auth_1 == s, next_projects_list[0].auth_2 == s, next_projects_list[0].auth_3 == s, next_projects_list[0].auth_4 == s]):
        #     project = next_projects_list.pop(0)
        #     s.peer_review_1 = project
        #     assigned = True
        
        # else:
        #     assigned = False
        #     while not assigned:
        #         random.shuffle(last_projects_list)

        #         if not np.any([last_projects_list[0].auth_1 == s, last_projects_list[0].auth_2 == s, last_projects_list[0].auth_3 == s, last_projects_list[0].auth_4 == s]):
        #             project = last_projects_list.pop(0)
        #             s.peer_review_1 = project
        #             assigned = True
        
        if len(current_projects_list) == 0:
            current_projects_list = next_projects_list
            next_projects_list = copy(projects_list)
        
        #peer review 2
        #check authorship and no double assignments (only necessary if switching to new list)
        check_case_b2 = False
        if len(current_projects_list)==2:
            if np.logical_not(np.any([current_projects_list[1].auth_1 == s, current_projects_list[1].auth_2 == s, current_projects_list[1].auth_3 == s, current_projects_list[1].auth_4 == s, current_projects_list[1] == s.peer_review_1])):
                check_case_b2 = True

        if len(current_projects_list) > 2:
            assigned = False
            while not assigned:
                random.shuffle(current_projects_list)

                if not np.any([current_projects_list[0].auth_1 == s, current_projects_list[0].auth_2 == s, current_projects_list[0].auth_3 == s, current_projects_list[0].auth_4 == s]):
                    project = current_projects_list.pop(0)
                    s.peer_review_2 = project
                    assigned = True

        elif not np.any([current_projects_list[0].auth_1 == s, current_projects_list[0].auth_2 == s, current_projects_list[0].auth_3 == s, current_projects_list[0].auth_4 == s, current_projects_list[0] == s.peer_review_1]):
            project = current_projects_list.pop(0)
            s.peer_review_2 = project
            assigned = True
        
        elif check_case_b2:
            project = current_projects_list.pop(1)
            s.peer_review_2 = project
            assigned = True
        
        else:
            assigned = False
            while not assigned:
                random.shuffle(next_projects_list)

                if not np.any([next_projects_list[0].auth_1 == s, next_projects_list[0].auth_2 == s, next_projects_list[0].auth_3 == s, next_projects_list[0].auth_4 == s, next_projects_list[0] == s.peer_review_1]):
                    project = next_projects_list.pop(0)
                    s.peer_review_2 = project
                    assigned = True
        
        if len(current_projects_list) == 0:
            current_projects_list = next_projects_list
            next_projects_list = copy(projects_list)

def helper_check_not_self_assigned(student_list, projects_list):
    for s in student_list:
        s_peer_review_1 = s.peer_review_1.project_id
        s_peer_review_2 = s.peer_review_2.project_id
        for p in projects_list:
            if np.any([p.auth_1 == s, p.auth_2 == s, p.auth_3 == s, p.auth_4 == s]):
                s_project = p.project_id
        
        if s_project == s_peer_review_1 or s_project == s_peer_review_2:
            print(f'{s.id} is reviewing their own project. {s_project} {s_peer_review_1} {s_peer_review_2}')
        if s_peer_review_1 == s_peer_review_2:
            print(f'{s.sid} is reviewing the same project twice...')
        # print(f"{s.sid} {s_project} {s_peer_review_1} {s_peer_review_2}")

def write_peer_review_assignments(student_list):
    sids = [s.sid for s in student_list]
    peer_review_1_title = [s.peer_review_1.title for s in student_list]
    peer_review_1_filename = [s.peer_review_1.filename for s in student_list]
    peer_review_2_title = [s.peer_review_2.title for s in student_list]
    peer_review_2_filename = [s.peer_review_2.filename for s in student_list]
    dict = {"Student ID":sids, 
            "Peer Review 1 Title":peer_review_1_title, 
            "Peer Review 1 Filename":peer_review_1_filename,
            "Peer Review 2 Title": peer_review_2_title,
            "Peer Review 2 Filename": peer_review_2_filename}
    df = pd.DataFrame(dict)
    df.to_csv("Peer_review_assignemnts.csv",index=False)

def write_peer_review_projects(pr1_list,pr2_list,projects_list):
    project_titles = []
    project_ids = []
    peer_review_filenames = []
    peer_review_list =  []

    for p in projects_list:
        if p.pr_exemption:
            continue
        # if p.project_id == "121":
        #     print("stop")
        title  = p.title
        id = p.project_id
        project_titles.append(title)
        project_ids.append(id)
        peer_review_filenames.append(id+"_peer_reviews.pdf")

        peer_review_files = []
        for pr in pr1_list:
            if pr.project == p:
                peer_review_files.append("/Users/jennyyang/Downloads/assignment_3790759_export_PR1/"+pr.filename)
                peer_review_list.append(pr)

        for pr in pr2_list:
            if pr.project == p:
                peer_review_files.append("/Users/jennyyang/Downloads/assignment_3790761_export_PR2/"+pr.filename)
                peer_review_list.append(pr)
        
        #write pdf
        output = PdfWriter()
        for prf in peer_review_files:
            infile = PdfReader(prf, 'rb')
            for i in range(1,len(infile.pages)-1):
                page = infile.pages[i]
                output.add_page(page)
        
        with open("./processed_peer_reviews/"+id+"_peer_reviews.pdf","wb") as f:
            output.write(f)

        #write csv
        dict = {"Project Title":project_titles, 
            "Peer Reviews Filename":peer_review_filenames}
        df = pd.DataFrame(dict).sort_values("Project Title")
        df.to_csv("Peer_Reviews_Returned.csv",index=False)     

def write_permission_to_publish(projects_list):
    project_titles = []
    project_ids = []
    project_filenames = []
    project_set = set(projects_list)
    for p in project_set:
        if p.permission_to_publish:
            
            #copy files
            f = glob("/Users/jennyyang/Downloads/organized_submissions/"+p.project_id+"*")
            if len(f) == 0:
                #cannot publish if not part of peer review
                continue
            elif len(f) == 1:
                project_titles.append(p.title)
                project_ids.append(p.project_id)
                f = f[0]
                f_name = f.split("/")[-1]
                project_filenames.append(f_name)
                shutil.copy(f,"./publishable_projects/"+f_name)
            else:
                raise NotImplementedError
    dict = {"Title":project_titles,
            "Filenames": project_filenames}
    
    df = pd.DataFrame(dict)
    df.to_csv("Publishable_Projects.csv",index=False)

def search_pr_by_filename(filename,pr_list,student_list):
    for pr in pr_list:
        if pr.filename == filename:
            for i,s in enumerate(student_list):
                if s==pr.auth:
                    print(i)
            print(pr)
            print(pr.auth.peer_review_1)
            print(pr.auth.peer_review_2)

def write_master_peer_review_assignments(student_list):
    sids = [s.sid for s in student_list]
    names = [s.first_name+" "+s.last_name for s in student_list]
    emails = [s.email for s in student_list]
    peer_review_1_title = [s.peer_review_1.title for s in student_list]
    peer_review_1_filename = [s.peer_review_1.filename for s in student_list]
    peer_review_2_title = [s.peer_review_2.title for s in student_list]
    peer_review_2_filename = [s.peer_review_2.filename for s in student_list]
    dict = {"Student ID":sids, 
            "Name": names,
            "Student Email":emails,
            "Peer Review 1 Title":peer_review_1_title, 
            "Peer Review 1 Filename":peer_review_1_filename,
            "Peer Review 2 Title": peer_review_2_title,
            "Peer Review 2 Filename": peer_review_2_filename}
    df = pd.DataFrame(dict)
    df.to_csv("Peer_review_assignemnts_master.csv",index=False)

def save_assignments(student_list, projects_list,filename):
    dict = {"student_list":student_list, "projects_list":projects_list}
    with open(filename,"wb") as f:
        pickle.dump(dict,f)

def load_assignments(filename):
    with open(filename,"rb") as f:
        dict = pickle.load(f)
    return dict["student_list"], dict["projects_list"]           

def check_equal_dist(student_list,projects_list):
    for p in set(projects_list):
        counter = 0
        for s in student_list:
            if s.peer_review_1 == p:
                counter += 1
            if s.peer_review_2 == p:
                counter += 1

        # print(counter)
        if counter == 0:
            print("zero", p.project_id)
        if counter == 1:
            print("one", p.project_id)
        if counter >= 4:
            print(">=4", p.project_id, counter)
        # if counter<=3:
        #     print(p.project_id)


student_list = []
projects_list = []
def run_first():
    student_list = get_student_list()
    projects_list = get_projects_list(student_list)
    assign_peer_reviews(student_list,projects_list)
    save_assignments(student_list,projects_list,"master_assignments2.pkl")
    write_peer_review_assignments(student_list)

    write_permission_to_publish(projects_list)
    print("stop")

# run_first()


def run_second():
    student_list, projects_list = load_assignments("master_assignments2.pkl")
    for p in projects_list:
        print(p.auth_1)
    print(len(projects_list))

    write_master_peer_review_assignments(student_list)
    # check_equal_dist(student_list, projects_list)

    helper_check_not_self_assigned(student_list, projects_list)

    write_permission_to_publish(projects_list)
    print("stop")

# run_second()




# ######WRONG UPLOAD ORDER SWAP PROCEDURE#########
# student_idx = 353
# print("Peer Review 1: ",student_list[student_idx].peer_review_1.title)
# print("Peer Review 2: ",student_list[student_idx].peer_review_2.title)

# old_pr1 = student_list[student_idx].peer_review_1
# old_pr2 = student_list[student_idx].peer_review_2

# student_list[student_idx].peer_review_1 = old_pr2
# student_list[student_idx].peer_review_2 = old_pr1
# save_assignments(student_list,projects_list,"master_assignments.pkl")
# student_list, projects_list = load_assignments("master_assignments.pkl")

# print("Peer Review 1: ",student_list[student_idx].peer_review_1.title)
# print("Peer Review 2: ",student_list[student_idx].peer_review_2.title)
# ################################################

# ###########CHANGE PERMISSION TO PUBLISH###########
# project_id = '161'
# for p in projects_list:
#     if p.project_id == project_id:
#         print(p.title)
#         p.permission_to_publish = 1
# ##################################################


def run_third():
    student_list, projects_list = load_assignments("master_assignments2.pkl")
    with open("submission_metadata_PR1.yml","r") as f:
        pr1_metadata = yaml.safe_load(f)
    pr1_list = get_peer_review_list(student_list,projects_list,pr1_metadata,1)

    with open("submission_metadata_PR2.yml","r") as f:
        pr2_metadata = yaml.safe_load(f)
    pr2_list = get_peer_review_list(student_list,projects_list,pr2_metadata,2)
    write_peer_review_projects(pr1_list, pr2_list, projects_list)

run_third()

# write_permission_to_publish(projects_list)
# print("stop")


# helper_check_not_self_assigned(student_list, projects_list)
