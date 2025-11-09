use configurator_service::create_app;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    let server = create_app().await?;
    server.await
}
