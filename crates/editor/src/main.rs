slint::include_modules!();

#[allow(dead_code)]
mod discord;
#[allow(dead_code)]
mod external_editor;
mod settings;
#[allow(dead_code)]
mod updater;

fn main() -> Result<(), slint::PlatformError> {
    slint::init_translations!(concat!(env!("CARGO_MANIFEST_DIR"), "/i18n/"));

    let app = AppWindow::new()?;
    app.run()
}
