use configurator_service::run;

#[actix_web::main]
async fn main() -> anyhow::Result<()> {
    run().await
}
