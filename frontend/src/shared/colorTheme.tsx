import { PaletteMode } from "@mui/material";
import { blue, grey, indigo } from "@mui/material/colors";

export const getDesignTokens = (mode: PaletteMode) => ({
  palette: {
    mode,
    ...(mode === "light"
      ? {
          // palette values for light mode
          background: { paper: blue[100] },
          text: {
            primary: grey[900],
            secondary: grey[700],
          },
        }
      : {
          // palette values for dark mode
          main: indigo[600],
          background: {
            default: grey[900],
            paper: grey[800],
          },
          text: {
            primary: "#fff",
            secondary: grey[200],
          },
        }),
  },
});
