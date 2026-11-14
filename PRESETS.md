# Anime presets — 0.17

18 editable, costume-led designs. Thumbnails, editor, theme demo and standalone customer HTML use the same Canvas vector painter. No downloaded character illustrations or generated image sheets are shipped.

| Preset | Shell and Home | Activation |
|---|---|---|
| Ninja Way | Orange/black jacket; Leaf spiral | Compact inward Rasengan |
| Grand Line | Red vest, blue shorts, straw sash; red-band hat | Elastic punch |
| Limit Break | Orange gi, blue collar/sash; 1–4 star Dragon Balls | Rising ki |
| Soul Reaper | Black robe/white collar; Hell Butterfly | Blue-white blade sweep |
| Water Breath | Even green/black checks; water crests | Layered water/foam |
| Domain | Indigo-black field; white-violet core | Converge, then expand |
| Plus Ultra | Green panels, white gloves, red belt; respirator | Contour Cowling arcs |
| Devil Hunter | Cream shirt/black tie; starter handle | Toothed sweep/sparks |
| Hunter License | License panels; double-X | Narrow scanner |
| Grimoire | Dark grimoire; five-leaf clover | Black/crimson anti-magic |
| Duelist | Card panels; inverted Millennium triangle/eye | Card draw |
| Golden Wind | Magenta suit/heart opening; gold-green ladybugs | Brooch pulse |
| Twilight | Green suit, cream shirt/red tie; WISE pin and small Chimera | Dossier stamp |
| Occult Signal | Cream/red cat accents; Turbo Granny cat | Outward signal rings |
| Defense Force | Charcoal armor/cyan seams; horned jaw | Brief seam flash |
| Off Duty | Green apron, cream shirt; glasses/moustache | Single motion line |
| Scarlet Eye | Charcoal/fan accent; three curved rotating tomoe | Restrained eye/fan pulse |
| Flame Heart | White cape, layered flame edge; flame guard | Curved yellow/orange/red swing |

## Editing and compatibility

- **Include preset wordmark** uses the existing text layer. Disable it to keep your own text/logo. Gallery thumbnails intentionally omit wordmarks.
- **Keep my shell & button colors** preserves palette fields and individual button overrides. Costume art and emblems keep their identifying illustration colors. Per-part resting colors override face-plate colors.
- Customer job names, controller placement and shell texture survive preset changes.
- **Signature input effects** independently enables the themed ability. Normal pressed highlights remain immediate. Still mode suppresses abilities; reduced mode lowers their intensity.
- Abilities trigger on a new press; holding does not repeat. Analog triggers use activation/release hysteresis. Sparse neutral states, long pauses and style changes clear stale activations. At most four effects overlap.
- Existing v1 jobs load with their saved settings; the new signature-effect flag defaults off until a preset is applied or the option is enabled. Existing style names remain supported.
- **Play theme demo** simulates the editor only; physical input forwarding to OBS is unchanged.
- Native G7 Home artwork uses an inset circular face inside the original chrome rim. Original input mapping, housing geometry, stick components and trigger travel are retained.

## Visual review

Matched G7 Pro CE / White, 1672 × 1241, neutral state, wordmarks off, no breathing/glow; dark #111820 presentation background. Captures are rendered from the app, with no compositing inside the controller.
- [All 18 before/after](docs/anime-0.17/comparison.jpg)
- [Wordmark-off thumbnails at 280px](docs/anime-0.17/thumbnails.jpg)
- [OBS-sized previews at 418px](docs/anime-0.17/obs.jpg)
- [Enlarged native Home emblems](docs/anime-0.17/home-emblems.jpg)
- [Required side-by-side theme pairs](docs/anime-0.17/theme-pairs.jpg)
- [Simultaneous input/ability frames](docs/anime-0.17/effects.jpg)

## Verification and limits

`anime-identity-test.cjs` checks all 18 editor applications, demos and self-contained transparent exports, exact 1–4 Dragon Ball star counts, three tomoe, native Home selection, neutral cleanup, bounded rapid effects, pause/rearm, 30/60/144Hz time equality, still-mode input, palette/layout/name preservation and saved-setting migration. Existing input/lifecycle suites cover trigger depth, simultaneous directions, stick travel/rims and disconnected cleanup.
Visual paths are authored interpretations scaled for an overlay, not frame-extracted animation. Physical controller input, OBS/Streamlabs on the customer machine, target GPU frame rate and franchise approval remain manual acceptance checks. Do not describe these fan-inspired designs as officially licensed.

## Reference audit

These official/publisher sources were used to check costume colors and principal silhouettes. Reference images stayed outside shipped assets. Details not visible in the selected illustrations (license-card layout, five-leaf cover, sword-guard close-up, exact ability choreography and the tiny Chimera plush) remain simplified interpretations of the supplied art direction, not source-matched reproductions.
- Naruto jacket/headband: https://naruto-official.com/common/ogp/NTOS_OG-main.png
- Luffy vest/shorts/hat: https://www.viz.com/one-piece (publisher series header).
- Dragon Ball orange/red-star material: https://en.dragon-ball-official.com/assets/img/intro/icon_ball.png
- Ichigo robe/collar: https://bleach-anime.com/assets/img/character/chara_01.png
- Tanjiro haori/water palette: https://kimetsu.com/anime/risshihen/ogp.jpg
- Denji shirt/tie: https://chainsawman.dog/tvseries/assets/img/chara/chara_1_stand.png
- Hunter Association double-X: official title artwork at https://www.ntv.co.jp/hunterhunter/
- Asta character: https://bclover.jp/assets/img/character/full/main/asta.png
- Millennium Puzzle silhouette: https://www.yugioh.com/characters/yugi-muto
- Giorno suit/brooch: https://jojo-animation.com/character/img/01/img_chara.png
- Loid character context: https://spy-family.net/tvseries/
- Turbo Granny cat face/collar/bib: https://anime-dandadan.com/_assets/images/char/detail/turbo-granny_pc.png
- Kafka armor: https://kaiju-no8.net/assets/img/character/c0_main.png ; horned monster/seams: https://www.viz.com/kaiju-no-8 (publisher header).
- Sakamoto face/glasses: https://sakamotodays.jp/c/themes/sd/assets/img/character/chara1_main1.png
- Rengoku cape/flame palette: https://kimetsu.com/anime/mugenresshahen_tv/assets/img/character/img_cha_05.jpg
- Gojo ability, Deku suit, Uchiha eye counts and remaining fine motifs follow the user’s specific brief; exact frame choreography has not been independently certified.
