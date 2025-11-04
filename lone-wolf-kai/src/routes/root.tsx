import { Outlet } from "react-router";
import { Provider as JotaiProvider } from "jotai";
import Navigation from "../components/Navigation";
import { useTheme } from "../hooks/useTheme";

function RootContent() {
  useTheme(); // Initialize theme

  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}

export default function Root() {
  return (
    <JotaiProvider>
      <RootContent />
    </JotaiProvider>
  );
}
