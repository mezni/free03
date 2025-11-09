use my_crate::run; // replace `my_crate` with your crate name

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    run().await
}
