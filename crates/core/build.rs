fn main() {
    // Bake the workspace res/ directory path into the binary at compile time.
    // In dev builds, wm_core uses this to find tools and assets in the source tree.
    // In release builds, the path is resolved relative to the executable instead.
    let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    let workspace_res = std::path::Path::new(&manifest_dir)
        .parent()
        .expect("crates/core has a parent (crates/)")
        .parent()
        .expect("crates/ has a parent (workspace root)")
        .join("res");
    println!("cargo:rustc-env=WME_RES_DIR={}", workspace_res.display());
    // Re-run if the res directory changes
    println!("cargo:rerun-if-changed=../../res");
}
