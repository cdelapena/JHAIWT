import { FC, Fragment } from "react";

import {
  Button,
  Card,
  CardActions,
  CardContent,
  Typography,
} from "@mui/material";

import { JobInterface } from "../../../../shared/Interfaces";

interface ResultProps {
  job: JobInterface;
}

const SingleResult: FC<ResultProps> = ({ job }) => {
  const handleClick = () => {
    window.open(job.url, "_blank");
  };

  const card = (
    <Fragment>
      <CardContent sx={{ padding: "25px 50px 0px" }}>
        <Typography sx={{ fontSize: 18 }} color="text.secondary" gutterBottom>
          {job.title}
        </Typography>
        <p>
          <strong>Company Name: </strong>
          {job.company_name ? job.company_name : "Not Listed"}
          <br />
          <strong>Job Industry: </strong>
          {job.category ? job.category : "Not Listed"}
          <br />
          <strong>Salary: </strong>
          {job.salary ? job.salary : "Not Listed"}
          <br />
          <strong>Location: </strong>
          {job.candidate_required_location
            ? job.candidate_required_location
            : "Not Listed"}
          <br />
          <br />
          {job.description.substring(0, 300)}...
        </p>
      </CardContent>
      <CardActions>
        <Button
          size="small"
          variant="outlined"
          sx={{ marginLeft: "40px", marginBottom: "20px" }}
          onClick={handleClick}
        >
          See Listing
        </Button>
      </CardActions>
    </Fragment>
  );
  return (
    <Card
      variant="outlined"
      sx={{
        marginTop: "1rem",
        marginBottom: "1rem",
      }}
    >
      {card}
    </Card>
  );
};

export default SingleResult;
