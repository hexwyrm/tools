use reqwest::Client;
use serde::Serialize;

#[derive(Serialize)]
pub struct ProbeResult {
    pub url: String,
    pub status: Option<u16>,
    pub server: Option<String>,
    pub powered_by: Option<String>,
    pub content_type: Option<String>,
    pub tech_stack: Vec<String>,
}

pub async fn probe_url(url: String) -> ProbeResult {
    let client = Client::new();

    let resp = client.get(&url).send().await;

    match resp {
        Ok(r) => {
            let status = r.status().as_u16();

            let server = r.headers()
                .get("server")
                .map(|v| v.to_str().unwrap_or("").to_string());

            let powered_by = r.headers()
                .get("x-powered-by")
                .map(|v| v.to_str().unwrap_or("").to_string());

            let content_type = r.headers()
                .get("content-type")
                .map(|v| v.to_str().unwrap_or("").to_string());

            let tech_stack = fingerprint(&server, &powered_by, &content_type);

            ProbeResult {
                url,
                status: Some(status),
                server,
                powered_by,
                content_type,
                tech_stack,
            }
        }
        Err(_) => ProbeResult {
            url,
            status: None,
            server: None,
            powered_by: None,
            content_type: None,
            tech_stack: vec![],
        },
    }
}

fn fingerprint(server: &Option<String>, powered_by: &Option<String>, content_type: &Option<String>) -> Vec<String> {
    let mut tech = Vec::new();

    if let Some(s) = server {
        let s_lower = s.to_lowercase();
        if s_lower.contains("nginx") { tech.push("nginx".into()); }
        if s_lower.contains("apache") { tech.push("apache".into()); }
        if s_lower.contains("iis") { tech.push("microsoft iis".into()); }
    }

    if let Some(p) = powered_by {
        let p_lower = p.to_lowercase();
        if p_lower.contains("php") { tech.push("php".into()); }
        if p_lower.contains("express") { tech.push("node.js (express)".into()); }
        if p_lower.contains("asp") { tech.push("asp.net".into()); }
    }

    if let Some(ct) = content_type {
        let ct_lower = ct.to_lowercase();
        if ct_lower.contains("json") { tech.push("json api".into()); }
        if ct_lower.contains("html") { tech.push("html".into()); }
    }

    tech
}
