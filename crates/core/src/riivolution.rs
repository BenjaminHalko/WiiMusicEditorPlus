use std::path::PathBuf;

use sysinfo::Disks;

#[derive(Debug, Clone)]
pub struct DriveInfo {
    pub path: PathBuf,
    pub device: String,
}

#[must_use]
pub fn generate_xml(
    mod_name: &str,
    mod_path: &str,
    message_region: &str,
    include_save: bool,
) -> String {
    let save_line = if include_save {
        format!("\n        <savegame external = \"{mod_path}/save\" clone = \"false\" />")
    } else {
        String::new()
    };

    format!(
        r#"
<wiidisc version="1" root="">
    <id game="R64" />
    <options>
        <section name="{mod_name}">
            <option name="Load Mod">
                <choice name="Enabled">
                    <patch id="TheMod" />
                </choice>
            </option>
        </section>
    </options>
    <patch id="TheMod">
        <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="{mod_path}/rp_Music_sound.brsar" offset=""/>
        <file disc="/{message_region}/Message/message.carc" external="{mod_path}/message.carc" offset=""/>
        <file disc="main.dol" external="{mod_path}/main.dol" offset="" />{save_line}
    </patch>
</wiidisc>"#
    )
}

#[must_use]
pub fn list_removable_drives() -> Vec<DriveInfo> {
    let disks = Disks::new_with_refreshed_list();
    disks
        .list()
        .iter()
        .filter(|disk| disk.is_removable())
        .map(|disk| DriveInfo {
            path: disk.mount_point().to_path_buf(),
            device: disk.name().to_string_lossy().into_owned(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn xml_without_save() {
        let xml = generate_xml("My Mod", "/MyMod", "US", false);
        let expected = r#"
<wiidisc version="1" root="">
    <id game="R64" />
    <options>
        <section name="My Mod">
            <option name="Load Mod">
                <choice name="Enabled">
                    <patch id="TheMod" />
                </choice>
            </option>
        </section>
    </options>
    <patch id="TheMod">
        <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/MyMod/rp_Music_sound.brsar" offset=""/>
        <file disc="/US/Message/message.carc" external="/MyMod/message.carc" offset=""/>
        <file disc="main.dol" external="/MyMod/main.dol" offset="" />
    </patch>
</wiidisc>"#;
        assert_eq!(xml, expected);
    }

    #[test]
    fn xml_with_save() {
        let xml = generate_xml("My Mod", "/MyMod", "US", true);
        let expected = r#"
<wiidisc version="1" root="">
    <id game="R64" />
    <options>
        <section name="My Mod">
            <option name="Load Mod">
                <choice name="Enabled">
                    <patch id="TheMod" />
                </choice>
            </option>
        </section>
    </options>
    <patch id="TheMod">
        <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/MyMod/rp_Music_sound.brsar" offset=""/>
        <file disc="/US/Message/message.carc" external="/MyMod/message.carc" offset=""/>
        <file disc="main.dol" external="/MyMod/main.dol" offset="" />
        <savegame external = "/MyMod/save" clone = "false" />
    </patch>
</wiidisc>"#;
        assert_eq!(xml, expected);
    }

    #[test]
    fn xml_different_region() {
        let xml = generate_xml("Test", "/Test", "JP", false);
        assert!(xml.contains(r#"disc="/JP/Message/message.carc""#));
        assert!(xml.contains(r#"<section name="Test">"#));
        assert!(xml.contains(r#"external="/Test/rp_Music_sound.brsar""#));
    }

    #[test]
    fn list_removable_drives_does_not_panic() {
        let drives = list_removable_drives();
        let _ = drives;
    }
}
