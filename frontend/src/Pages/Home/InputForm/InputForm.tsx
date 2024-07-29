import { useNavigate } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import {
  Button,
  FormControl,
  FormControlLabel,
  FormHelperText,
  FormLabel,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  TextField,
  Chip,
  Box,
  IconButton,
} from "@mui/material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import { useFormik } from "formik";
import * as yup from "yup";
import axios from "axios";
import "./InputForm.css";
import {
  NumberOfSearchResultsOptions,
  JobCategoryInterface,
} from "./InputFormHelper";
import { SearchContext } from "../../../shared/contexts";
import { baseBackendUrl } from "../../../shared/urls";

const validationSchema = yup.object({
  industryCategory: yup.string().required("Industry Category is required"),
  yearsOfExperience: yup
    .number()
    .integer("Please enter a number")
    .required("Years of experience is required"),
  city: yup.string().required("City is required"),
  relevantSkills: yup
    .array()
    .of(yup.string())
    .min(1, "Relevant skills are required")
    .required("Relevant skills are required"),
  academicCredentials: yup
    .string()
    .required("Academic credentials are required"),
  userText: yup
    .string()
    .required("User Text is required")
    .test(
      "word-length",
      "Must be less than or equal to 300 words",
      (text) => text.split(" ").length <= 300
    ),
  numberOfSearchResults: yup
    .number()
    .required("Number of Search Results is required"),
});

const InputForm = () => {
  const navigate = useNavigate();
  const { setSearchValues } = useContext(SearchContext);
  const [jobs, setJobs] = useState<JobCategoryInterface[]>([
    { id: 0, name: "API Unavailable" },
  ]);
  const [skills, setSkills] = useState<string[]>([]);

  const formik = useFormik({
    initialValues: {
      industryCategory: "",
      yearsOfExperience: "",
      city: "",
      relevantSkills: [] as string[],
      academicCredentials: "",
      userText: "",
      numberOfSearchResults: NumberOfSearchResultsOptions.Option1,
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
    onSubmit: async (values) => {
      setSearchValues({
        industryCategory: formik.values.industryCategory,
        yearsOfExperience: formik.values.yearsOfExperience,
        city: formik.values.city,
        relevantSkills: formik.values.relevantSkills.join(", "),
        academicCredentials: formik.values.academicCredentials,
        userText: formik.values.userText,
        numberOfSearchResults: `${formik.values.numberOfSearchResults.toString()}`,
      });
  try {
        await axios.post(`${baseBackendUrl}/api/job/results`, values);
        try {
        await axios.post(`${baseBackendUrl}/api/job/results`, values);
        navigate("/results");
      } catch (error) {
        console.error("Error submitting form data", error);
      }
      } catch (error) {
        console.error("Error submitting form data", error);
      }
    },
  });

  const fetchData = async () => {
    await axios({
      method: "GET",
      url: `/api/category`,
      baseURL: baseBackendUrl,
    })
      .then((response) => {
        const res = response.data;
        setJobs(res);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  };

  useEffect(() => {
    fetchData();
    fetchTags();
  }, []);

  const fetchTags = async () => {
    await axios({
      method: "GET",
      url: `/api/tag`,
      baseURL: baseBackendUrl,
    })
      .then((response) => {
        const res = response.data.map((tag: { name: string }) => tag.name);
        setSkills(res);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  };

  useEffect(() => {
    fetchTags();
  }, []);

  useEffect(() => {
    fetchTags();
  }, []);

  const handleRelevantSkillsChange = (event: any) => {
    const {
      target: { value },
    } = event;
    formik.setFieldValue("relevantSkills", typeof value === "string" ? value.split(",") : value);
    setOpen(false);
  };


  const handleDropdownIconClick = (event: any) => {
    event.stopPropagation();
    setOpen(!open);
  };

  const handleDropdownIconClick = (event: any) => {
    event.stopPropagation();
    setOpen(!open);
  };

  return (
    <div className="input-form-container">
      <form onSubmit={formik.handleSubmit}>
        <FormControl className="input-form" id="industryCategoryFormControl">
          <InputLabel
            id="industryCategoryLabel"
            sx={{
              color:
                formik.values.industryCategory === "" &&
                formik.touched.industryCategory
                  ? "#d32f2f"
                  : "",
            }}
          >
            Industry Category
          </InputLabel>
          <Select
            name="industryCategory"
            labelId="industryCategoryLabel"
            id="industryCategorySelect"
            value={formik.values.industryCategory}
            label="Industry Category"
            onChange={formik.handleChange}
            error={
              formik.touched.industryCategory &&
              Boolean(formik.errors.industryCategory)
            }
            sx={{ textAlign: "left" }}
          >
            {jobs.map((job) => (
              <MenuItem key={job.id.toString()} value={job.id}>
                {job.name}
              </MenuItem>
            ))}
          </Select>
          <FormHelperText sx={{ color: "#d32f2f" }}>
            {formik.touched.industryCategory && formik.errors.industryCategory}
          </FormHelperText>
        </FormControl>
        <TextField
          id="yearsOfExperience"
          className="input-form"
          name="yearsOfExperience"
          label="Years of Experience"
          type="number"
          value={formik.values.yearsOfExperience}
          onChange={formik.handleChange}
          error={
            formik.touched.yearsOfExperience &&
            Boolean(formik.errors.yearsOfExperience)
          }
          helperText={
            formik.touched.yearsOfExperience && formik.errors.yearsOfExperience
          }
        />
        <TextField
          id="city"
          className="input-form"
          name="city"
          label="City"
          value={formik.values.city}
          onChange={formik.handleChange}
          error={formik.touched.city && Boolean(formik.errors.city)}
          helperText={formik.touched.city && formik.errors.city}
        />
        <FormControl
          className="input-form hide-arrow"
          error={
            formik.touched.relevantSkills &&
            Boolean(formik.errors.relevantSkills)
          }
        >
          <InputLabel id="relevantSkillsLabel">Relevant Skills</InputLabel>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Select
              labelId="relevantSkillsLabel"
              id="relevantSkillsSelect"
              multiple
              open={open}
              onClose={() => setOpen(false)}
              value={formik.values.relevantSkills}
              onChange={handleRelevantSkillsChange}
              onBlur={formik.handleBlur}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {(selected as string[]).map((value) => (
                    <Chip
                      key={value}
                      label={value}
                      onDelete={(event) => {
                        event.stopPropagation();
                        formik.setFieldValue(
                          "relevantSkills",
                          formik.values.relevantSkills.filter((skill) => skill !== value)
                        );
                      }}
                      sx={{ margin: 0.5 }}
                    />
                  ))}
                </Box>
              )}
              IconComponent={() => (
                <IconButton onClick={handleDropdownIconClick} sx={{ padding: 0 }}>
                  <ArrowDropDownIcon />
                </IconButton>
              )}
              sx={{ flex: 1 }}
            >
              {skills.map((skill) => (
                <MenuItem key={skill} value={skill}>
                  {skill}
                </MenuItem>
              ))}
            </Select>
          </Box>
          <FormHelperText>
            {formik.touched.relevantSkills && formik.errors.relevantSkills}
          </FormHelperText>
        </FormControl>
        <TextField
          id="academicCredentials"
          className="input-form"
          name="academicCredentials"
          label="Academic Credentials"
          value={formik.values.academicCredentials}
          onChange={formik.handleChange}
          error={
            formik.touched.academicCredentials &&
            Boolean(formik.errors.academicCredentials)
          }
          helperText={
            formik.touched.academicCredentials &&
            formik.errors.academicCredentials
          }
        />

        <TextField
          id="userText"
          className="input-form"
          multiline
          name="userText"
          label="Tell Us About Yourself (300 words or less)"
          rows={4}
          value={formik.values.userText}
          onChange={formik.handleChange}
          error={formik.touched.userText && Boolean(formik.errors.userText)}
          helperText={formik.touched.userText && formik.errors.userText}
        />

        <FormControl component="fieldset" className="input-form">
          <FormLabel component="legend">Number of Search Results</FormLabel>
          <RadioGroup
            row
            id="numberOfSearchResults"
            name="numberOfSearchResults"
            sx={{ justifyContent: "center" }}
            onChange={formik.handleChange}
            value={formik.values.numberOfSearchResults}
          >
            <FormControlLabel
              name="numberOfSearchResults"
              value={NumberOfSearchResultsOptions.Option1}
              control={<Radio />}
              label="5"
            />
            <FormControlLabel
              name="numberOfSearchResults"
              value={NumberOfSearchResultsOptions.Option2}
              control={<Radio />}
              label="10"
            />
            <FormControlLabel
              name="numberOfSearchResults"
              value={NumberOfSearchResultsOptions.Option3}
              control={<Radio />}
              label="15"
            />
          </RadioGroup>
        </FormControl>

        <Button
          color="primary"
          disabled={!formik.dirty}
          variant="contained"
          type="submit"
          sx={{ display: "flex", marginLeft: "auto", marginRight: "auto" }}
        >
          Search
        </Button>
      </form>
    </div>
  );
};

export default InputForm;