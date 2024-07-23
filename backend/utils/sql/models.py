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

@dataclass
class ModelData:
    id: int
    job_title: str
    description: str
    category: str
    tags: str

@dataclass
class JobCategory:
    id: int
    name: str

@dataclass
class JobTag:
    id: int
    name: str