pub mod http;
pub mod report;

use http::probe_url;
use report::print_report;

use tokio::fs::File;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::task;
use futures::stream::{FuturesUnordered, StreamExt};

pub async fn run(input_path: &str, concurrency: usize) {
    let file = File::open(input_path)
        .await
        .expect("Failed to open input file");

    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    let mut tasks = FuturesUnordered::new();

    while let Ok(Some(url)) = lines.next_line().await {
        let url = url.trim().to_string();
        if url.is_empty() {
            continue;
        }

        // Limit concurrency
        while tasks.len() >= concurrency {
            tasks.next().await;
        }

        tasks.push(task::spawn(probe_url(url)));
    }

    let mut results = Vec::new();
    while let Some(Ok(result)) = tasks.next().await {
        results.push(result);
    }

    print_report(&results);
}
