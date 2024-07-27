from dataclasses import dataclass


@dataclass
class JobPosting:
    id: int
    title: str
    description: str
    category: str
    company_name: str
    salary: str
    tags: str
    job_type: str
    source_url: str
    publish_date: str
    candidate_required_location: str


@dataclass
class ModelData:
    id: int
    title: str
    preprocessed_description: str
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
