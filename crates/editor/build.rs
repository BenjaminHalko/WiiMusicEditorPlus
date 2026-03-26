fn main() {
    let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    let workspace = std::path::Path::new(&manifest_dir)
        .parent()
        .expect("crates/core has a parent (crates/)")
        .parent()
        .expect("crates/ has a parent (workspace root)");

    let tools_dir = workspace.join("tools");
    let res_dir = workspace.join("res");

    println!("cargo:rustc-env=WME_TOOLS_DIR={}", tools_dir.display());
    println!("cargo:rustc-env=WME_RES_DIR={}", res_dir.display());
    println!("cargo:rerun-if-changed=../../tools");
    println!("cargo:rerun-if-changed=../../res");
}
