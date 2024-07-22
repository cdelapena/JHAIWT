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
} from "@mui/material";
import { JobInterface } from "../../../shared/interfaces";
import { sampleJsonResponse } from "../../../shared/constants"; // Import the mock data
import "./BrowseResults.css";

type Order = 'asc' | 'desc';

const columnWidths = {
  title: '25%',
  company_name: '20%',
  candidate_required_location: '20%',
  category: '15%',
  salary: '10%',
  action: '10%'
};

const BrowseResults: FC = () => {
  const [jobs, setJobs] = useState<JobInterface[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [orderBy, setOrderBy] = useState<keyof JobInterface>('title');
  const [order, setOrder] = useState<Order>('asc');

  useEffect(() => {
    // Use the mock data instead of fetching from the API
    const fetchJobs = async () => {
      try {
        setLoading(true);
        // Simulate an API call delay
        setTimeout(() => {
          setJobs(sampleJsonResponse.jobs); // Set jobs from the mock data
          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching jobs:', error);
        setError('Failed to fetch jobs. Please try again later.');
      }
    };

    fetchJobs();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSort = (property: keyof JobInterface) => () => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const sortedJobs = React.useMemo(() => {
    const comparator = (a: JobInterface, b: JobInterface) => {
      if (b[orderBy] < a[orderBy]) {
        return order === 'asc' ? 1 : -1;
      }
      if (b[orderBy] > a[orderBy]) {
        return order === 'asc' ? -1 : 1;
      }
      return 0;
    };
    return [...jobs].sort(comparator);
  }, [jobs, order, orderBy]);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Paper className="browse-results-container">
      <TableContainer style={{ height: '400px', overflow: 'auto' }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {['title', 'company_name', 'candidate_required_location', 'category', 'salary'].map((column) => (
                <TableCell key={column} style={{ width: columnWidths[column as keyof typeof columnWidths] }}>
                  <TableSortLabel
                    active={orderBy === column}
                    direction={orderBy === column ? order : 'asc'}
                    onClick={handleSort(column as keyof JobInterface)}
                  >
                    {column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </TableSortLabel>
                </TableCell>
              ))}
              <TableCell style={{ width: columnWidths.action }}>ACTION</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedJobs
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((job: JobInterface) => (
                <TableRow key={job.id}>
                  <TableCell style={{ width: columnWidths.title }}>{job.title}</TableCell>
                  <TableCell style={{ width: columnWidths.company_name }}>{job.company_name}</TableCell>
                  <TableCell style={{ width: columnWidths.candidate_required_location }}>{job.candidate_required_location}</TableCell>
                  <TableCell style={{ width: columnWidths.category }}>{job.category}</TableCell>
                  <TableCell style={{ width: columnWidths.salary }}>{job.salary || "Not Listed"}</TableCell>
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
