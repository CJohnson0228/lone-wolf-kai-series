import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router";
import "./index.css";

// Routes
import Root from "./routes/root";
import Home from "./routes/home";
import CharacterCreation from "./routes/character-creation";
import Game from "./routes/game";
import Characters from "./routes/characters";
import Settings from "./routes/settings";
import ErrorPage from "./routes/error-page";

// Create router with data mode
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "character/new",
        element: <CharacterCreation />,
      },
      {
        path: "characters",
        element: <Characters />,
      },
      {
        path: "game/:bookId/:sectionId",
        element: <Game />,
      },
      {
        path: "settings",
        element: <Settings />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
