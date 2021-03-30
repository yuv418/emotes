#[derive(Deserialize, Seralize)]
struct Namespace {
    id: u32,
    slug: String,
    global: bool,
}

#[derive(Deserialize)]
struct Emote {
    name: String,
    emote_type: u32,
    slug: String,
    namespace_id: u32,
}

struct Client {
    api_key: String,
}
