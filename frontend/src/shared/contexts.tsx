import { createContext } from "react";
import { SearchContextInterface } from "./interfaces";
import { initialSearchValues } from "./constants";

export const ThemeContext = createContext({
  toggleColorMode: () => {},
});

export const SearchContext = createContext<SearchContextInterface>({
  searchValues: initialSearchValues,
  setSearchValues: () => {},
});
