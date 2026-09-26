"use client";

import { FormEvent, useEffect, useState } from "react";

type User = {
  id: number;
  email: string;
  username: string;
};

type Repository = {
  name: string;
  full_name: string;
  owner: string;
  description: string | null;
  default_branch: string;
  private: boolean;
  html_url: string;
  stars: number;
  forks: number;
};

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [repositoryUrl, setRepositoryUrl] = useState("");
  const [repository, setRepository] = useState<Repository | null>(null);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadUser() {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setMessage("You are not logged in.");
        setLoading(false);
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();

        if (!response.ok) {
          localStorage.removeItem("access_token");
          setMessage("Your session is invalid or expired.");
          return;
        }

        setUser(data);
      } catch (error) {
        console.error(error);
        setMessage("Unable to connect to the backend.");
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, []);

  async function handleConnectRepository(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setConnecting(true);
    setMessage("");
    setRepository(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/github/repository",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: repositoryUrl,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Unable to connect repository.");
        return;
      }

      setRepository(data);
    } catch (error) {
      console.error(error);
      setMessage("Unable to connect to the backend.");
    } finally {
      setConnecting(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#0a0a0a] text-white">
        <p className="text-sm text-zinc-500">Loading dashboard...</p>
      </main>
    );
  }

  if (message && !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#0a0a0a] px-6 text-white">
        <div className="text-center">
          <p className="text-sm text-zinc-400">{message}</p>

          <button
            onClick={() => {
              window.location.href = "/login";
            }}
            className="mt-5 rounded-lg bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-zinc-200"
          >
            Go to Login
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">
      <div className="mx-auto min-h-screen max-w-7xl px-6 py-6">
        <header className="flex items-center justify-between border-b border-white/10 pb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white text-sm font-bold text-black">
              D
            </div>

            <div>
              <h1 className="text-lg font-semibold tracking-tight">
                DevNexa AI
              </h1>

              <p className="text-xs text-zinc-500">
                AI-powered software engineering
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-sm text-zinc-400">
              {user?.username}
            </span>

            <button
              onClick={handleLogout}
              className="rounded-lg border border-white/10 px-4 py-2 text-sm text-zinc-300 transition hover:bg-white/5"
            >
              Logout
            </button>
          </div>
        </header>

        <section className="py-12">
          <div>
            <p className="text-sm font-medium text-zinc-500">
              SOFTWARE ENGINEERING WORKSPACE
            </p>

            <h2 className="mt-3 text-4xl font-semibold tracking-tight">
              Welcome, {user?.username}
            </h2>

            <p className="mt-4 max-w-2xl text-zinc-500">
              Connect a GitHub repository and let DevNexa AI understand,
              analyze, test, and work with your codebase.
            </p>
          </div>

          <div className="mt-10 max-w-3xl rounded-xl border border-white/10 bg-white/[0.02] p-6">
            <div>
              <h3 className="text-lg font-medium">
                Connect Repository
              </h3>

              <p className="mt-2 text-sm text-zinc-500">
                Enter the URL of a public GitHub repository to get started.
              </p>
            </div>

            <form
              onSubmit={handleConnectRepository}
              className="mt-6 flex flex-col gap-3 sm:flex-row"
            >
              <input
                type="url"
                value={repositoryUrl}
                onChange={(event) =>
                  setRepositoryUrl(event.target.value)
                }
                placeholder="https://github.com/username/repository"
                required
                className="h-12 flex-1 rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-white/30"
              />

              <button
                type="submit"
                disabled={connecting}
                className="h-12 rounded-lg bg-white px-6 text-sm font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {connecting ? "Connecting..." : "Connect"}
              </button>
            </form>

            {message && (
              <p className="mt-4 text-sm text-red-400">
                {message}
              </p>
            )}
          </div>

          {repository && (
            <div className="mt-6 max-w-3xl rounded-xl border border-white/10 bg-white/[0.02] p-6">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs text-zinc-600">
                    CONNECTED REPOSITORY
                  </p>

                  <h3 className="mt-2 text-xl font-medium">
                    {repository.name}
                  </h3>

                  <p className="mt-1 text-sm text-zinc-500">
                    {repository.full_name}
                  </p>
                </div>

                <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                  Connected
                </span>
              </div>

              <p className="mt-5 text-sm leading-6 text-zinc-400">
                {repository.description ||
                  "No repository description available."}
              </p>

              <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
                <RepositoryInfo
                  label="Branch"
                  value={repository.default_branch}
                />

                <RepositoryInfo
                  label="Visibility"
                  value={repository.private ? "Private" : "Public"}
                />

                <RepositoryInfo
                  label="Stars"
                  value={String(repository.stars)}
                />

                <RepositoryInfo
                  label="Forks"
                  value={String(repository.forks)}
                />
              </div>

              <a
                href={repository.html_url}
                target="_blank"
                rel="noreferrer"
                className="mt-6 inline-block text-sm text-zinc-300 underline underline-offset-4 transition hover:text-white"
              >
                Open repository on GitHub
              </a>
            </div>
          )}

          <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
            <DashboardCard
              title="Code Intelligence"
              description="Understand files, functions, dependencies, and repository structure."
            />

            <DashboardCard
              title="AI Agents"
              description="Analyze code, investigate issues, and reason about software changes."
            />

            <DashboardCard
              title="Safe Execution"
              description="Run tests and validate proposed changes in isolated environments."
            />
          </div>
        </section>
      </div>
    </main>
  );
}

function RepositoryInfo({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/[0.02] p-4">
      <p className="text-xs text-zinc-600">{label}</p>
      <p className="mt-2 text-sm text-zinc-300">{value}</p>
    </div>
  );
}

function DashboardCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6">
      <h3 className="text-lg font-medium">{title}</h3>

      <p className="mt-3 text-sm leading-6 text-zinc-500">
        {description}
      </p>

      <span className="mt-6 inline-block rounded-full border border-white/10 px-3 py-1 text-xs text-zinc-600">
        Coming soon
      </span>
    </div>
  );
}