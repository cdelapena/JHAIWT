import React, { FC, useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  CircularProgress,
  Typography,
  TablePagination,
  TableSortLabel,
  TextField,
  Chip,
  Autocomplete,
  useTheme,
} from "@mui/material";
import { JobInterface } from "../../../shared/interfaces";
import "./BrowseResults.css";
import axios from "axios";
import { baseBackendUrl } from "../../../shared/urls";

type Order = "asc" | "desc";

const columnWidths = {
  title: "20%",
  company_name: "10%",
  candidate_required_location: "10%",
  category: "10%",
  salary: "10%",
  action: "10%",
};

const BrowseResults: FC = () => {
  const [jobs, setJobs] = useState<JobInterface[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [orderBy, setOrderBy] = useState<keyof JobInterface>("title");
  const [order, setOrder] = useState<Order>("asc");

  const theme = useTheme();

  const [filters, setFilters] = useState({
    title: [] as string[],
    companyName: [] as string[],
    location: [] as string[],
    category: [] as string[],
    salary: [] as string[],
  });

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        await axios({
          method: "GET",
          url: `/api/job`,
          baseURL: baseBackendUrl,
        })
          .then((response) => {
            const res = response.data;
            setJobs(res);
            setLoading(false);
          })
          .catch((error) => {
            if (error.response) {
              console.log(error.response);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          });
      } catch (error) {
        console.error("Error fetching jobs:", error);
        setError("Failed to fetch jobs. Please try again later.");
      }
    };

    fetchJobs();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSort = (property: keyof JobInterface) => () => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleFilterChange = (name: keyof typeof filters, value: string[]) => {
    setFilters({
      ...filters,
      [name]: value,
    });
  };

  const filteredJobs = React.useMemo(() => {
    return jobs.filter(
      (job) =>
        filters.title.every((filter) =>
          job.title.toLowerCase().includes(filter.toLowerCase())
        ) &&
        filters.companyName.every((filter) =>
          job.company_name.toLowerCase().includes(filter.toLowerCase())
        ) &&
        filters.location.every((filter) =>
          job.candidate_required_location
            .toLowerCase()
            .includes(filter.toLowerCase())
        ) &&
        filters.category.every((filter) =>
          job.category.toLowerCase().includes(filter.toLowerCase())
        ) &&
        filters.salary.every((filter) =>
          job.salary
            ? job.salary.toLowerCase().includes(filter.toLowerCase())
            : true
        )
    );
  }, [jobs, filters]);

  const sortedJobs = React.useMemo(() => {
    const comparator = (a: JobInterface, b: JobInterface) => {
      if (b[orderBy] < a[orderBy]) {
        return order === "asc" ? 1 : -1;
      }
      if (b[orderBy] > a[orderBy]) {
        return order === "asc" ? -1 : 1;
      }
      return 0;
    };
    return [...filteredJobs].sort(comparator);
  }, [filteredJobs, order, orderBy]);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Paper className="browse-results-container">
      <div
        className="filter-container"
        style={{
          backgroundColor:
            theme.palette.mode === "dark" ? "#666666" : "#dfebf7",
        }}
      >
        <Autocomplete
          multiple
          options={[]}
          freeSolo
          value={filters.title}
          onChange={(event: React.ChangeEvent<{}>, newValue: string[]) =>
            handleFilterChange("title", newValue)
          }
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip label={option} {...getTagProps({ index })} />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Filter by Title"
              variant="outlined"
              margin="normal"
            />
          )}
        />

        <Autocomplete
          multiple
          options={[]}
          freeSolo
          value={filters.companyName}
          onChange={(event: React.ChangeEvent<{}>, newValue: string[]) =>
            handleFilterChange("companyName", newValue)
          }
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip label={option} {...getTagProps({ index })} />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Filter by Company"
              variant="outlined"
              margin="normal"
            />
          )}
        />

        <Autocomplete
          multiple
          options={[]}
          freeSolo
          value={filters.location}
          onChange={(event: React.ChangeEvent<{}>, newValue: string[]) =>
            handleFilterChange("location", newValue)
          }
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip label={option} {...getTagProps({ index })} />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Filter by Location"
              variant="outlined"
              margin="normal"
            />
          )}
        />

        <Autocomplete
          multiple
          options={[]}
          freeSolo
          value={filters.category}
          onChange={(event: React.ChangeEvent<{}>, newValue: string[]) =>
            handleFilterChange("category", newValue)
          }
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip label={option} {...getTagProps({ index })} />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Filter by Category"
              variant="outlined"
              margin="normal"
            />
          )}
        />

        <Autocomplete
          multiple
          options={[]}
          freeSolo
          value={filters.salary}
          onChange={(event: React.ChangeEvent<{}>, newValue: string[]) =>
            handleFilterChange("salary", newValue)
          }
          renderTags={(value: readonly string[], getTagProps) =>
            value.map((option: string, index: number) => (
              <Chip label={option} {...getTagProps({ index })} />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Filter by Salary"
              variant="outlined"
              margin="normal"
            />
          )}
        />
      </div>

      <TableContainer style={{ height: "70vh", overflow: "auto" }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {[
                "title",
                "company_name",
                "location",
                "category",
                "salary",
                "job_listing",
              ].map((column) => (
                <TableCell
                  key={column}
                  sx={{
                    width: columnWidths[column as keyof typeof columnWidths],
                    backgroundColor:
                      theme.palette.mode === "dark" ? "#666666" : "#dfebf7",
                  }}
                >
                  <TableSortLabel
                    active={orderBy === column}
                    direction={orderBy === column ? order : "asc"}
                    onClick={handleSort(column as keyof JobInterface)}
                  >
                    {column
                      .split("_")
                      .map(
                        (word) => word.charAt(0).toUpperCase() + word.slice(1)
                      )
                      .join(" ")}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedJobs
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((job: JobInterface) => (
                <TableRow key={job.id}>
                  <TableCell style={{ width: columnWidths.title }}>
                    {job.title}
                  </TableCell>
                  <TableCell style={{ width: columnWidths.company_name }}>
                    {job.company_name}
                  </TableCell>
                  <TableCell
                    style={{ width: columnWidths.candidate_required_location }}
                  >
                    {job.candidate_required_location}
                  </TableCell>
                  <TableCell style={{ width: columnWidths.category }}>
                    {job.category}
                  </TableCell>
                  <TableCell style={{ width: columnWidths.salary }}>
                    {job.salary || "Not Listed"}
                  </TableCell>
                  <TableCell style={{ width: columnWidths.action }}>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => window.open(job.url, "_blank")}
                    >
                      See Listing
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 50, 100]}
        component="div"
        count={jobs.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
};

export default BrowseResults;
