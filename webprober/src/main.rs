// webprober - HTTP service scanner
// Author: Hexwyrm
// License: Apache-2.0

mod probe;

use clap::Parser;

#[derive(Parser)]
#[command(name = "webprober")]
#[command(about = "A concurrent HTTP service scanner written in Rust.")]
struct Cli {
    /// Path to a file containing URLs (one per line)
    #[arg(short, long)]
    input: String,

    /// Number of concurrent workers
    #[arg(short, long, default_value_t = 10)]
    concurrency: usize,
}

#[tokio::main]
async fn main() {
    let args = Cli::parse();
    probe::run(&args.input, args.concurrency).await;
}
