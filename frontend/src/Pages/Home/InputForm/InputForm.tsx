import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import {
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";

import { useFormik } from "formik";
import * as yup from "yup";

import "./InputForm.css";
import { jobs } from "./InputFormHelper";

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
});

const InputForm = () => {
  const formik = useFormik({
    initialValues: {
      industryCategory: "",
      yearsOfExperience: "",
      city: "",
      relevantSkills: "",
      academicCredentials: "",
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      alert(JSON.stringify(values, null, 2));
    },
  });

  return (
    <div className="input-form-container">
      <form onSubmit={formik.handleSubmit}>
        <FormControl className="input-form" id="industryCategoryFormControl">
          <InputLabel
            id="industryCategoryLabel"
            sx={{ color: formik.values.industryCategory === "" && formik.touched.industryCategory ? "#d32f2f" : "" }}
          >
            Industry Category
          </InputLabel>
          <Select
            name="industryCategory"
            labelId="industryCategoryLabel"
            id="industryCategorySelect"
            value={formik.values.industryCategory}
            label="Job Industry"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={
              formik.touched.industryCategory && Boolean(formik.errors.industryCategory)
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
