import { FC } from "react";
import { IconButton } from "@mui/material";
import { useTheme } from "next-themes";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";

const ThemeToggle: FC<{}> = () => {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <IconButton sx={{ fontSize: '24px' }} onClick={() => setTheme(resolvedTheme === "light" ? "dark" : "light")} color="inherit">
        {resolvedTheme === "light" ? <DarkModeIcon /> : <LightModeIcon />}
    </IconButton>
  );
};

export default ThemeToggle;