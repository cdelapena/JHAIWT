import { FC, useContext, useEffect, useState } from "react";

import SingleResult from "./SingleResult/SingleResult";
import { JobInterface } from "../../../shared/interfaces";
import { baseBackendUrl } from "../../../shared/urls";

import "./SearchResults.css";
import axios from "axios";
import { SearchContext } from "../../../shared/contexts";
import { Typography } from "@mui/material";

const SearchResults: FC = () => {
  const { searchValues } = useContext(SearchContext);

  const [jobs, setJobs] = useState<JobInterface[]>([]);
  const [isError, setIsError] = useState<Boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      await axios({
        method: "POST",
        url: `/api/job/results/${searchValues.numberOfSearchResults}`,
        baseURL: baseBackendUrl,
        data: { searchValues },
      })
        .then((response) => {
          const res = response.data;
          setJobs(res);
        })
        .catch((error: any) => {
          setIsError(true);
          if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
          }
        });
    };
    fetchData();
  }, [searchValues]);

  return (
    <div className="search-results-container">
      {jobs.map((job: JobInterface) => {
        return <SingleResult job={job} key={job.id}></SingleResult>;
      })}
      {isError && (
        <>
          <Typography
            sx={{ fontSize: "2rem", textAlign: "center", marginTop: "10rem" }}
          >
            Error! :( Please retry search query
          </Typography>
        </>
      )}
    </div>
  );
};

export default SearchResults;
