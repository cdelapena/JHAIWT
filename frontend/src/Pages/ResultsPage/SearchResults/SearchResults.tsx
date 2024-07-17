import { FC } from "react";

import SingleResult from "./SingleResult/SingleResult";
import { sampleJsonResponse } from "../../../shared/Constants";
import { JobInterface } from "../../../shared/Interfaces";

import "./SearchResults.css";

const SearchResults: FC = () => {
  return (
    <div className="search-results-container">
      {sampleJsonResponse.jobs.map((job: JobInterface) => {
        return <SingleResult job={job} key={job.id}></SingleResult>;
      })}
    </div>
  );
};

export default SearchResults;
