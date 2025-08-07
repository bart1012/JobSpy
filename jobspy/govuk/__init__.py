from datetime import datetime
import math

from bs4 import BeautifulSoup, PageElement, Tag
from jobspy.model import (
    Scraper,
    ScraperInput,
    Site,
    JobPost,
    Location,
    JobResponse,
    JobType,
    DescriptionFormat,
)

from typing import Tuple

from jobspy.util import (
    extract_emails_from_text,
    markdown_converter,
    create_session,
    create_logger,
    _should_omit,
)

from jobspy.govuk.constant import api_headers

log = create_logger("Govuk")


class Govuk(Scraper):
    def __init__(
        self, proxies: list[str] | str | None = None, ca_cert: str | None = None
    ):
        super().__init__(Site.GOVUK, proxies=proxies)
        self.session = create_session(
            proxies=self.proxies, ca_cert=ca_cert, is_tls=False
        )

        self.scraper_input = None
        self.jobs_per_page = 100
        self.num_workers = 10
        self.seen_urls = set()
        self.location_code = None
        self.job_category_code = None
        self.headers = None
        self.base_url = None
        self.filter_keywords = None

    # def scrape(self, scraper_input: ScraperInput):
    #     print("calling govuk scraper")
    #     location_code = scraper_input.govuk_location.value
    #     job_category = scraper_input.govuk_job_category.value
    #     self.base_url = f"https://findajob.dwp.gov.uk/search?pp=50&loc={location_code}"
    #     if job_category is not None:
    #         self.base_url += f"&cat={job_category}"
    #     target_page_URL = self.base_url + f"&p={1}"
    #     print(f"govuk target URL: {target_page_URL}")
    #     self.headers = api_headers.copy()
    #     response = self.session.get(
    #         target_page_URL,
    #         headers=self.headers,
    #         timeout=10,
    #         verify=True,
    #     )
    #     print(response.text)

    def scrape(self, scraper_input: ScraperInput) -> JobResponse:
        """
        Scrapes govuk for jobs according to location, jobtype and keywords
        :param scraper_input:
        :return: job_response
        """
        self.filter_keywords = scraper_input.avoid_keywords
        self.scraper_input = scraper_input
        location_code = scraper_input.govuk_location.value
        job_category = scraper_input.govuk_job_category
        self.base_url = f"https://findajob.dwp.gov.uk/search?pp=50&loc={location_code}"
        if job_category is not None:
            category_code = job_category.value
            self.base_url += f"&cat={category_code}"
        self.headers = api_headers.copy()
        job_list = []
        page = 1

        while len(self.seen_urls) < scraper_input.results_wanted + scraper_input.offset:
            log.info(
                f"search page: {page} / {math.ceil(scraper_input.results_wanted / self.jobs_per_page)}"
            )
            jobs = self._scrape_page(page)
            if not jobs:
                log.info(f"found no jobs on page: {page}")
                break
            job_list += jobs
            page += 1
        return JobResponse(
            jobs=job_list[
                scraper_input.offset : scraper_input.offset
                + scraper_input.results_wanted
            ]
        )

    def _scrape_page(self, page_num: int | None) -> list[JobPost]:
        """
        Scrapes a page of Govuk for jobs with scraper_input criteria
        :param cursor:
        :return: jobs found on page, next page cursor
        """
        jobs = []

        if self.base_url is None:
            log.info(f"Invalid base URL for gov.uk")
            return jobs
        else:
            target_page_URL = self.base_url + f"&p={page_num}"

        response = self.session.get(
            target_page_URL,
            headers=self.headers,
            timeout=10,
            verify=True,
        )

        if not response.ok:
            log.info(
                f"responded with status code: {response.status_code} (submit GitHub issue if this appears to be a bug)"
            )
            return jobs
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("div", class_="search-result")

        job_list = []
        for job in jobs:
            processed_job = self._process_job(job)
            if processed_job:
                job_list.append(processed_job)

        return job_list

    def _process_job(self, job: Tag) -> JobPost | None:
        """
        Parses the job Tag object into JobPost model
        :param job: Tag to parse
        :return: JobPost if it's a new job
        """

        job_id = job["data-aid"]
        title_tag = job.find("h3").find("a")
        title = title_tag.text.strip()
        link = title_tag["href"]

        if link in self.seen_urls:
            return
        self.seen_urls.add(link)

        details = job.find("ul", class_="search-result-details")
        detail_items = details.find_all("li")
        post_date = detail_items[0].text.strip()
        employer_info = detail_items[1]
        company = employer_info.find("strong").text.strip()
        full_location = employer_info.find("span").text.strip().split(",")
        if len(full_location) <= 1:
            return
        salary = detail_items[2].text.strip() if len(detail_items) > 2 else None

        # Contract types like "Full time", "Contract", etc.
        tags = [li.text.strip() for li in detail_items[3:]]

        description = job.find("p", class_="search-result-description").text.strip()
        if _should_omit(title, company, self.scraper_input.avoid_keywords):
            return None

        return JobPost(
            id=f"govuk-{job_id}",
            title=title,
            description=description,
            company_name=company,
            company_url=None,
            company_url_direct=None,
            location=Location(
                city=full_location[0].strip(),
                state=(
                    full_location[1].strip()
                    if full_location[1] is not " "
                    else "North West"
                ),
                country="United Kingdom",
            ),
            job_type=None,  # fetch actual type if needed
            compensation=None,
            date_posted=datetime.strptime(post_date, "%d %B %Y").date(),
            job_url=f"{link}",
            job_url_direct=None,
            emails=None,
            is_remote=None,
            company_addresses=None,
        )
