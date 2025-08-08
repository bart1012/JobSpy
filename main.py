import gspread
import pandas as pd
from jobspy import scrape_jobs  # or adjust import if needed
from jobspy.model import JobCategory, LocationCode, Job_short
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from jobspy.util import connect_spreadsheet
from jobspy.util import add_to_spreadsheet
from jobspy import user_search_input
from google import genai
from jobspy import user_cv
import os
from pydantic import BaseModel
import json

# Integrate AI for easy scanning and removal
# set up automated calls
# add post scanning and verification for google to filter shit stuff
# add looping to something like google to iterate over towns

# make temp dataframe
# each loop adds to df
# at the end filter the df through gemini
# add to spreadsheet

f = open("./jobspy/secrets.json")
data = json.load(f)
sheet_id = data["spreadsheet_id"]

spreadsheet = connect_spreadsheet("./jobspy/gspread_cred.json", sheet_id)
worksheet = spreadsheet.get_worksheet(0)

genAI_client = genai.Client()

temp_df = None


# Scrape Govuk for all job categories defined by user
# for job_category in user_search_input.target_job_categories:

#     jobs_df = scrape_jobs(
#         site_name=["govuk"],
#         govuk_job_category=job_category,
#         govuk_location=LocationCode.NORTHWEST,
#         avoid_keywords='senior Fundraiser Scientist Executive Transport Steward head Painter "Teaching Assistant" "Self Employed" "Store Assistant" "self-employed" "Team Member" Lecturer Associate Officer Lead Estimator Teaching principal Coach ITOL beBeeSoftware milk waiter retail chef mechanic van manager therapist nurse bar care housekeeper MOT Recruitment Shift Factory Warehouse',
#         results_wanted=5,
#     )

#     temp_df = jobs_df if temp_df is None else pd.concat([temp_df, jobs_df])

for job_title in user_search_input.job_titles:

    jobs_df = scrape_jobs(
        site_name=["indeed", "linkedin"],
        search_term=f'"{job_title}"',
        avoid_keywords='Sr. Care Finance "VITA CV" Lecturer Warehouse Dentist Manager Accountant Operator Childcare Security Leader Kitchen Teaching DataAnnotation Painter TieTalent Senior "Bending Spoons" Surveyor Teaching Joiner Lead Executive',
        location="Liverpool, Merseyside",
        linkedin_fetch_description=True,
        distance=50,
        results_wanted=10,
        hours_old=24 * 7,
        country_indeed="UK",
    )
    if len(jobs_df) > 0:
        cleaned_df = jobs_df[
            ["title", "company", "location", "date_posted", "site", "job_url", "id"]
        ]
        add_to_spreadsheet(cleaned_df, worksheet)


# temp_df = jobs_df if temp_df is None else pd.concat([temp_df, jobs_df])

# cleaned_df = jobs_df[
#     ["title", "company", "location", "date_posted", "site", "job_url", "id"]
# ]
# print(f"Length prior to AI filtering: {len(cleaned_df)}")

# response = genAI_client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=f"I have a number of scraped jobs. Despite best efforts to filter out irrelevant entries, some still persist. Your task is to filter out all irrelevant jobs based on the CV provided; The jobs you should omit include all irrelevant jobs to my education, skills, and experience, as well as any role with a high seniority level such as manager or executive. My CV: {user_cv.user_cv}. Jobs: {cleaned_df}",
#     config={
#         "response_mime_type": "application/json",
#         "response_schema": list[Job_short],
#     },
# )

# filtered_df = pd.read_json(response.text)
# add_to_spreadsheet(cleaned_df, worksheet)
#
