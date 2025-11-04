import { useRouteError, Link } from "react-router";

export default function ErrorPage() {
  const error = useRouteError() as any;

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="card text-center max-w-lg">
        <h1 className="text-4xl font-display font-bold mb-4 text-kai-700 dark:text-kai-400">
          Oops!
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Sorry, an unexpected error has occurred.
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mb-6">
          {error?.statusText || error?.message || "Unknown error"}
        </p>
        <Link to="/" className="btn btn-primary">
          Return Home
        </Link>
      </div>
    </div>
  );
}
