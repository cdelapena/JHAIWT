import { Dispatch, SetStateAction } from "react";

export interface JobInterface {
  id: number;
  url: string;
  title: string;
  company_name: string;
  company_logo: string;
  category: string;
  tags: string[];
  job_type: string;
  publication_date: string;
  candidate_required_location: string;
  salary: string;
  description: string;
}

export interface SearchInterface {
  industryCategory: string;
  yearsOfExperience: string;
  city: string;
  relevantSkills: string;
  academicCredentials: string;
  numberOfSearchResults: string;
}

export interface SearchContextInterface {
  searchValues: SearchInterface;
  setSearchValues: Dispatch<SetStateAction<SearchInterface>>;
}
