import { useNavigate } from "react-router-dom";

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
} from "@mui/material";

import { useFormik } from "formik";
import * as yup from "yup";

import "./InputForm.css";
import { NumberOfSearchResultsOptions, jobs } from "./InputFormHelper";
import { useContext } from "react";
import { SearchContext } from "../../../shared/contexts";

// schema: https://github.com/jquense/yup?tab=readme-ov-file#stringurlmessage-string--function-schema

const validationSchema = yup.object({
  industryCategory: yup.string().required("Industry Category is required"),
  yearsOfExperience: yup
    .number()
    .integer("Please enter a number")
    .required("Years of experience is required"),
  city: yup.string().required("City is required"),
  relevantSkills: yup.string().required("Relevant skills are required"),
  academicCredentials: yup
    .string()
    .required("Academic credentials are required"),
  numberOfSearchResults: yup
    .number()
    .required("Number of Search Results is required"),
});

const InputForm = () => {
  const navigate = useNavigate();
  const { setSearchValues } = useContext(SearchContext);

  const formik = useFormik({
    initialValues: {
      industryCategory: "",
      yearsOfExperience: "",
      city: "",
      relevantSkills: "",
      academicCredentials: "",
      numberOfSearchResults: NumberOfSearchResultsOptions.Option1,
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      alert(JSON.stringify(values, null, 2));
      setSearchValues({
        industryCategory: formik.values.industryCategory,
        yearsOfExperience: formik.values.yearsOfExperience,
        city: formik.values.city,
        relevantSkills: formik.values.relevantSkills,
        academicCredentials: formik.values.academicCredentials,
        numberOfSearchResults: `${formik.values.numberOfSearchResults.toString()}`,
      });
      navigate("/results");
    },
  });

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
            onBlur={formik.handleBlur}
            error={
              formik.touched.industryCategory &&
              Boolean(formik.errors.industryCategory)
            }
            sx={{ textAlign: "left" }}
          >
            {jobs.map((job) => (
              <MenuItem key={job.id.toString()} value={job.slug}>
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
          onBlur={formik.handleBlur}
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
          onBlur={formik.handleBlur}
          error={formik.touched.city && Boolean(formik.errors.city)}
          helperText={formik.touched.city && formik.errors.city}
        />
        <TextField
          id="relevantSkills"
          className="input-form"
          name="relevantSkills"
          label="Relevant Skills"
          value={formik.values.relevantSkills}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={
            formik.touched.relevantSkills &&
            Boolean(formik.errors.relevantSkills)
          }
          helperText={
            formik.touched.relevantSkills && formik.errors.relevantSkills
          }
        />
        <TextField
          id="academicCredentials"
          className="input-form"
          name="academicCredentials"
          label="Academic Credentials"
          value={formik.values.academicCredentials}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          error={
            formik.touched.academicCredentials &&
            Boolean(formik.errors.academicCredentials)
          }
          helperText={
            formik.touched.academicCredentials &&
            formik.errors.academicCredentials
          }
        />

        <FormControl component="fieldset" className="input-form">
          <FormLabel component="legend">Number of Search Results</FormLabel>
          <RadioGroup
            row
            id="numberOfSearchResults"
            name="numberOfSearchResults"
            sx={{ justifyContent: "center" }}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
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
