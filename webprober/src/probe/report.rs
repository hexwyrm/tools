use super::http::ProbeResult;

pub fn print_report(results: &Vec<ProbeResult>) {
    let json = serde_json::to_string_pretty(results).unwrap();
    println!("{}", json);
}
