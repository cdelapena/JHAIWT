import { FC } from "react";

import { useTheme } from "@mui/material";

import SingleResult from "./SingleResult/SingleResult";

const SearchResults: FC = () => {
  const theme = useTheme();

  return (
    <>
      <h1 className="title" style={{color: theme.palette.mode === "dark" ? "white" : ""}}>
        <SingleResult job="hello"></SingleResult>
      </h1>
    </>
  );
};

export default SearchResults;
