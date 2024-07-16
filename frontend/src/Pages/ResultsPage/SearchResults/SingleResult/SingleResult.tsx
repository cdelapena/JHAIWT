import { FC } from "react";

import { useTheme } from "@mui/material";

import { JobInterface } from "../../../../shared/interfaces";

const SingleResult: FC<any> = ({ job }) => {
  const theme = useTheme();
  console.log(job);

  return (
    <div data-theme={theme.palette.mode}>
      <h2
        className="title"
        style={{ color: theme.palette.mode === "dark" ? "white" : "" }}
      >
        Job Title
      </h2>
      <p>Job Description</p>
    </div>
  );
};

export default SingleResult;
