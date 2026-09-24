export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-6">
        {/* Header */}
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

          <div className="flex items-center gap-3">
            <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
              System Online
            </span>

            <button className="rounded-lg border border-white/10 px-4 py-2 text-sm text-zinc-300 transition hover:bg-white/5">
              GitHub
            </button>
          </div>
        </header>

        {/* Hero */}
        <section className="flex flex-1 flex-col justify-center py-20">
          <div className="max-w-3xl">
            <p className="mb-4 text-sm font-medium text-zinc-500">
              AI SOFTWARE ENGINEERING PLATFORM
            </p>

            <h2 className="text-5xl font-semibold leading-tight tracking-tight sm:text-6xl">
              Understand.
              <br />
              Analyze.
              <br />
              <span className="text-zinc-500">Build with AI.</span>
            </h2>

            <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-400">
              DevNexa AI connects your codebase with intelligent agents that
              can understand repositories, search code, analyze problems,
              propose changes, and validate solutions.
            </p>

            {/* Repository Input */}
            <div className="mt-10 flex max-w-2xl flex-col gap-3 sm:flex-row">
              <input
                type="text"
                placeholder="https://github.com/username/repository"
                className="h-12 flex-1 rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white outline-none placeholder:text-zinc-600 focus:border-white/30"
              />

              <button className="h-12 rounded-lg bg-white px-6 text-sm font-medium text-black transition hover:bg-zinc-200">
                Connect Repository
              </button>
            </div>
          </div>

          {/* Capabilities */}
          <div className="mt-20 grid grid-cols-1 gap-4 md:grid-cols-3">
            <Feature
              number="01"
              title="Code Intelligence"
              description="Understand files, functions, dependencies, and relationships across your repository."
            />

            <Feature
              number="02"
              title="AI Agents"
              description="Use specialized agents to investigate issues, review code, search repositories, and reason about changes."
            />

            <Feature
              number="03"
              title="Safe Execution"
              description="Validate proposed changes through automated tests and isolated execution environments."
            />
          </div>
        </section>

        {/* Footer */}
        <footer className="flex flex-col gap-2 border-t border-white/10 pt-5 text-xs text-zinc-600 sm:flex-row sm:items-center sm:justify-between">
          <span>DevNexa AI</span>
          <span>AI-powered developer infrastructure</span>
        </footer>
      </div>
    </main>
  );
}

function Feature({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6 transition hover:border-white/20 hover:bg-white/[0.04]">
      <span className="text-xs text-zinc-600">{number}</span>

      <h3 className="mt-6 text-lg font-medium">{title}</h3>

      <p className="mt-3 text-sm leading-6 text-zinc-500">{description}</p>
    </div>
  );
}