import { FC } from "react";

import SingleResult from "./SingleResult/SingleResult";
<<<<<<< HEAD
import { sampleJsonResponse } from "../../../shared/constants";
=======
import { sampleJsonResponse } from "../../../shared/Constants";
>>>>>>> b384ea4 (Update SearchResults and SingleResult components)
import { JobInterface } from "../../../shared/interfaces";

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
