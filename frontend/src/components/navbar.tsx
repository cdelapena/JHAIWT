import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { blue } from "@mui/material/colors";

const Navbar: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <RouterLink
            to="/"
            style={{
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <Typography
              sx={{
                display: "inline-block",
                "&:hover": {
                  color: "text.secondary",
                },
              }}
            >
              Job Hunting AI Web Tool
            </Typography>
          </RouterLink>
        </Typography>
        <Box sx={{ marginLeft: "auto" }}>
          <Button color="inherit" component={RouterLink} to="/browse">
            Browse All
          </Button>
          <Button color="inherit" component={RouterLink} to="/features">
            Features
          </Button>
          <Button color="inherit" component={RouterLink} to="/about">
            About
          </Button>
          <Button color="inherit" component={RouterLink} to="/sources">
            Sources
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
