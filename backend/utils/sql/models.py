from dataclasses import dataclass

@dataclass
class JobPosting:
    id: int
    job_title: str
    description: str
    category: str
    company_name: str
    salary: str
    tags: str
    job_type: str
    source_url: str
    publish_date: str