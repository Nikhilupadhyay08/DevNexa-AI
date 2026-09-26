"use client";

import { FormEvent, useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("access_token", data.access_token);

      window.location.href = "/dashboard";
    } catch (error) {
      console.error(error);
      setMessage("Unable to connect to the backend");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#0a0a0a] px-6 text-white">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-white text-lg font-bold text-black">
            D
          </div>

          <h1 className="text-2xl font-semibold tracking-tight">
            Welcome back
          </h1>

          <p className="mt-2 text-sm text-zinc-500">
            Sign in to DevNexa AI
          </p>
        </div>

        <form
          onSubmit={handleLogin}
          className="rounded-xl border border-white/10 bg-white/[0.02] p-6"
        >
          <div className="space-y-5">
            <div>
              <label
                htmlFor="email"
                className="mb-2 block text-sm text-zinc-400"
              >
                Email
              </label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                required
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-white/30"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-2 block text-sm text-zinc-400"
              >
                Password
              </label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter your password"
                required
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-white/30"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="h-12 w-full rounded-lg bg-white px-6 text-sm font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </div>

          {message && (
            <p className="mt-5 text-center text-sm text-zinc-400">
              {message}
            </p>
          )}
        </form>
      </div>
    </main>
  );
}