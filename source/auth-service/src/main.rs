use auth_service::Application;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize and run the application
    let app = Application::new().await
        .expect("Failed to create application");
    
    app.run().await
}