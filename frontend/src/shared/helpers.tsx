import { PaletteMode } from "@mui/material";
import { amber, deepOrange, grey } from "@mui/material/colors";

export const getDesignTokens = (mode: PaletteMode) => ({
  palette: {
    mode,
    ...(mode === "light"
      ? {
          // palette values for light mode
          text: {
            primary: grey[900],
            secondary: grey[900],
          },
        }
      : {
          // palette values for dark mode
          main: grey[900],
          background: {
            default: grey[900],
          },
          text: {
            primary: "#fff",
            secondary: grey[500],
          },
        }),
  },
});
